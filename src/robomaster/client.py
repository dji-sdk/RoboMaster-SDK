# -*-coding:utf-8-*-
# Copyright (c) 2020 DJI.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the file LICENSE.txt or at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import threading
import binascii
from . import conn
from . import protocol
from . import logger
from . import event
from . import config


CLIENT_MAX_EVENT_NUM = 16


class EventIdentify(object):
    def __init__(self):
        self._valid = False
        self._ident = None
        self._event = threading.Event()


class MsgHandler:
    def __init__(self, proto_data=None, req_cb=None, ack_cb=None):
        self._proto_data = proto_data
        self._req_cb = req_cb
        self._ack_cb = ack_cb

    @property
    def proto_data(self):
        return self._proto_data

    @staticmethod
    def make_dict_key(cmd_set, cmd_id):
        return cmd_set * 256 + cmd_id

    def dict_key(self):
        logger.debug('MsgHandler: dict_key, isinstance:', isinstance(self._proto_data, protocol.ProtoData))
        if self._proto_data:
            return self.make_dict_key(self.proto_data._cmdset, self.proto_data._cmdid)
        return None


class Client(object):

    # host is int, index is int.
    def __init__(self, host=0, index=0, connect=None):
        self._host = host
        self._index = index
        self._conn = connect
        if connect is None:
            try:
                self._conn = conn.Connection(config.ROBOT_DEFAULT_LOCAL_WIFI_ADDR,
                                             config.ROBOT_DEFAULT_WIFI_ADDR,
                                             protocol=config.DEFAULT_CONN_PROTO)
            except Exception as e:
                logger.error('Client: __init__, create Connection, exception: {0}'.format(e))
                self._conn = None

        self._has_sent = 0
        self._has_recv = 0
        self._unpack_failed = 0
        self._dispatcher = event.Dispatcher()

        self._handler_dict = {}

        self._wait_ack_list = {}
        self._wait_ack_mutex = threading.Lock()
        self._event_list = []

        self._thread = None
        self._running = False

    def __del__(self):
        self.stop()

    @property
    def remote_addr(self):
        try:
            return self._conn.target_addr
        except Exception:
            raise print('Robot: Can not connect to robot, check connection please.')

    def add_handler(self, obj, name, f):
        self._dispatcher.add_handler(obj, name, f)

    def remove_handler(self, name):
        self._dispatcher.remove_handler(name)

    def initialize(self):
        if not self._conn:
            logger.warning("Client: initialize, no connections, init connections first.")
            return False
        for i in range(0, CLIENT_MAX_EVENT_NUM):
            ident = EventIdentify()
            self._event_list.append(ident)

        try:
            self._conn.create()
        except Exception as e:
            raise e
        return True

    @property
    def hostbyte(self):
        return protocol.host2byte(self._host, self._index)

    def start(self):
        try:
            result = self.initialize()
            if not result:
                return False
            self._thread = threading.Thread(target=self._recv_task)
            self._thread.start()
        except Exception as e:
            raise e

    def stop(self):
        if self._thread.is_alive():
            self._running = False
            proto = protocol.ProtoGetVersion()
            msg = protocol.Msg(self.hostbyte, self.hostbyte, proto)
            self._conn.send_self(msg.pack())
            self._thread.join()
        if self._conn:
            self._conn.close()

    def send_msg(self, msg):
        data = msg.pack()
        logger.debug("Client: send_msg, msg {0} {1}".format(self._has_sent, msg))

        logger.debug("Client: send_msg, cmset:{0:2x}, cmdid:{1:2x}, {2}".format(msg.cmdset, msg.cmdid,
                                                                                binascii.hexlify(data)))

        self._has_sent += 1
        self.send(data)

    def send_sync_msg(self, msg, callback=None, timeout=3.0):
        if not self._running:
            logger.error("Client: send_sync_msg, client recv_task is not running.")
            return None
        if msg._need_ack > 0:
            evt = self._ack_register_identify(msg)
            if evt is None:
                logger.error("Client: send_sync_msg, ack_register failed.")
                return None
            self.send_msg(msg)
            evt._event.wait(timeout)
            if not evt._event.isSet():
                logger.error("Client: send_sync_msg wait msg receiver:{0}, cmdset:0x{1:02x}, cmdid:0x{2:02x} \
timeout!".format(msg.receiver, msg.cmdset, msg.cmdid))
                evt._valid = False
                return None
            resp_msg = self._ack_unregister_identify(evt._ident)
            evt._valid = False
            if resp_msg is None:
                logger.error("Client, send_sync_msg, get resp msg failed.")
            else:
                if isinstance(resp_msg, protocol.Msg):
                    try:
                        resp_msg.unpack_protocol()
                        if callback:
                            callback(resp_msg)
                    except Exception as e:
                        self._unpack_failed += 1
                        logger.warning("Client: send_sync_msg, resp_msg {0:d} cmdset:0x{1:02x}, cmdid:0x{2:02x}, "
                                       "e {3}".format(self._has_sent, resp_msg.cmdset, resp_msg.cmdid, format(e)))
                        return None
                else:
                    logger.warning("Client: send_sync_msg, has_sent:{0} resp_msg:{1}.".format(
                        self._has_sent, resp_msg))
                    return None

            return resp_msg
        else:
            self.send_msg(msg)

    def resp_msg(self, msg):
        msg._sender, msg._receiver = msg._receiver, msg._sender
        msg._need_ack = 0
        msg._is_ack = True
        data = msg.pack(True)
        self._has_sent += 1
        self.send(data)

    def send(self, data):
        try:
            self._conn.send(data)
        except Exception as e:
            logger.warning("Client: send, exception {0}".format(str(e)))

    def send_async_msg(self, msg):
        if not self._running:
            logger.error("Client: send_async_msg, client recv_task is not running.")
            return None
        msg._need_ack = 0
        return self.send_msg(msg)

    def is_ready(self):
        return self._has_recv > 0

    def _recv_task(self):
        self._running = True
        logger.info("Client: recv_task, Start to Recving data...")
        while self._running:
            msg = self._conn.recv()
            if not self._running:
                break
            if msg is None:
                logger.warning("Client: _recv_task, recv msg is None, skip.")
                continue
            logger.info("Client: recv_msg, {0}".format(msg))
            self._has_recv += 1
            self._dispatch_to_send_sync(msg)
            self._dispatch_to_callback(msg)
            if self._dispatcher:
                self._dispatcher.dispatch(msg)
        self._running = False

    def _dispatch_to_send_sync(self, msg):
        if msg.is_ack:
            logger.debug("Client: dispatch_to_send_sync, {0} cmdset:{1} cmdid:{2}".format(
                self._has_recv, hex(msg._cmdset), hex(msg._cmdid)))
            ident = self._make_ack_identify(msg)
            self._wait_ack_mutex.acquire()
            if ident in self._wait_ack_list.keys():
                for i, evt in enumerate(self._event_list):
                    if evt._ident == ident and evt._valid:
                        self._wait_ack_list[ident] = msg
                        evt._event.set()
            else:
                logger.debug("Client: dispatch_to_send_sync, ident:{0} is not in wait_ack_list {1}".format(
                    ident, self._wait_ack_list))
            self._wait_ack_mutex.release()

    def _dispatch_to_callback(self, msg):
        if msg._is_ack:
            key = MsgHandler.make_dict_key(msg.cmdset, msg.cmdid)
            if key in self._handler_dict.keys():
                self._handler_dict[key]._ack_cb(self, msg)
            else:
                logger.debug("Client: dispatch_to_callback, msg cmdset:{0:2x}, cmdid:{1:2x} is not define ack \
handler".format(msg.cmdset, msg.cmdid))
        else:
            key = MsgHandler.make_dict_key(msg.cmdset, msg.cmdid)
            if key in self._handler_dict.keys():
                self._handler_dict[key]._req_cb(self, msg)
            else:
                logger.debug("Client: _dispatch_to_callback, cmdset:{0}, cmdid:{1} is not define req handler".format(
                    hex(msg.cmdset), hex(msg.cmdid)))

    @staticmethod
    def _make_ack_identify(msg):
        if msg.is_ack:
            return str(msg._sender) + str(hex(msg.cmdset)) + str(hex(msg.cmdid)) + str(msg._seq_id)
        else:
            return str(msg._receiver) + str(hex(msg.cmdset)) + str(hex(msg.cmdid)) + str(msg._seq_id)

    def _ack_register_identify(self, msg):
        self._wait_ack_mutex.acquire()
        ident = self._make_ack_identify(msg)
        self._wait_ack_list[ident] = 1
        self._wait_ack_mutex.release()
        evt = None

        for i, evt_ident in enumerate(self._event_list):
            if not evt_ident._valid:
                evt = evt_ident
                break
        if evt is None:
            logger.error("Client: event list is run out.")
            return None
        evt._valid = True
        evt._ident = ident
        evt._event.clear()
        return evt

    def _ack_unregister_identify(self, identify):
        try:
            self._wait_ack_mutex.acquire()
            if identify in self._wait_ack_list.keys():
                return self._wait_ack_list.pop(identify)
            else:
                logger.warning("can not find ident:{0} in wait_ack_list.".format(identify))
                return None
        finally:
            self._wait_ack_mutex.release()

    def add_msg_handler(self, handler):
        key = handler.dict_key()
        if key:
            self._handler_dict[key] = handler


class TextClient(object):

    def __init__(self, conf):
        self._conn = conn.Connection(conf.default_sdk_addr, conf.default_robot_addr, conf.cmd_proto)
        self._thread = threading.Thread(target=self._recv_task)
        self._running = False
        self._event = threading.Event()
        self._dispatcher = event.Dispatcher()
        self._has_cmd_wait_ack = False
        self._has_sent = 0
        self._has_recv = 0
        self._wait_ack_mutex = threading.Lock()

    def initialize(self):
        try:
            self._conn.create()
        except Exception as e:
            raise e
        return True

    def start(self):
        self.initialize()
        self._thread.start()

    def stop(self):
        self._running = False
        self._thread.join()
        self._conn.close()

    def check_is_dds_msg(self, msg):
        return protocol.TextMsg.IS_DDS_FLAG in msg.get_buf()

    def _recv_task(self):
        self._running = True
        logger.info("TextClient: _recv_task, Start to Recving data...")
        while self._running:
            resp = self._conn.recv()
            if not self._running:
                break
            if resp is None:
                logger.warning("Client: _recv_task, recv resp is None, skip.")
                continue

            if not self.check_is_dds_msg(resp):
                logger.info("TextClient: _recv_task, resp: {0}".format(resp))
            else:
                logger.debug("TextClient: recv_resp, recv resp {0}".format(resp))
            self._wait_ack_mutex.acquire()
            if self._has_cmd_wait_ack and not self.check_is_dds_msg(resp):
                logger.debug("TexClient: call send_sync dispatcher: {0}".format(resp))
                self._dispatch_to_send_sync(resp)
            self._wait_ack_mutex.release()
            if self._dispatcher:
                self._dispatcher.dispatch(resp)
        logger.info("_recv_task: quit.")

    def send(self, text):
        logger.debug("Client: time delay test, send time")
        logger.info("TextClient: send_msg: {0}".format(text))
        try:
            self._conn.send(text.encode('utf-8'))
        except Exception as e:
            logger.warning("TexClient: send_async_text, exception {0}".format(str(e)))
            return False
        return True

    def send_sync_msg(self, msg, callback=None, timeout=10):
        if not self._running:
            logger.error("TextClient: send_sync_msg, client rescv_task is not runnint")
        self._wait_ack_mutex.acquire()
        self._has_cmd_wait_ack = True
        self.send_msg(msg)
        self._wait_ack_mutex.release()
        self._event.wait(timeout)
        if self._event.isSet():
            self._event.clear()
            self._wait_ack_mutex.acquire()
            self._has_cmd_wait_ack = False
            self._wait_ack_mutex.release()
            return self._resp
        else:
            logger.warning("TextClient: send_sync_text, failed, timeout.")
            return None

    def send_async_msg(self, msg):
        if not self._running:
            logger.error("TextClient: send_async_msg, client recv_task is not running.")
            return None
        return self.send_msg(msg)

    def send_msg(self, msg):
        data = msg.pack()
        self.send(data)
        self._has_sent += 1

    def add_handler(self, obj, name, f):
        self._dispatcher.add_handler(obj, name, f)

    def remove_handler(self, name):
        self._dispatcher.remove_handler(name)

    def _dispatch_to_send_sync(self, msg):
        logger.debug("TextClient: _dispatch_to_send_sync, msg {0}".format(msg))
        self._resp = msg
        self._event.set()

    def _make_ack_identify(self, msg):
        return msg
