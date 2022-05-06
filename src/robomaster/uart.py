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


import collections
import threading
from queue import Queue
from . import module
from . import protocol
from . import logger


__all__ = ['Uart']


class Uart(module.Module):
    """ EP 串口模块 """

    _host = protocol.host2byte(3, 0)

    def __init__(self, robot):
        super().__init__(robot)
        self._robot = robot
        self._publisher = collections.defaultdict(list)
        self._msg_queue = Queue()
        self._dispatcher_running = False
        self._dispatcher_thread = None
        self._rec_data = []
        self._callback = None
        self._cb_args = None

    def __del__(self):
        self.stop()

    def start(self):
        self._client.add_handler(self, "Uart", self._msg_recv)
        self._dispatcher_thread = threading.Thread(target=self._dispatch_task)
        self._dispatcher_thread.start()

    def stop(self):
        self._dispatcher_running = False
        if self._dispatcher_thread:
            self._msg_queue.put(None)
            self._dispatcher_thread.join()
            self._dispatcher_thread = None

    @classmethod
    def _msg_recv(cls, self, msg):
        if msg.cmdset != 0x3f or msg.cmdid != 0xc1:
            return
        self._msg_queue.put(msg)
        pass

    def _dispatch_task(self):
        self._dispatcher_running = True
        logger.info("serial: dispatcher_task is running...")
        while self._dispatcher_running:
            msg = self._msg_queue.get(1)
            if msg is None:
                if not self._dispatcher_running:
                    break
                continue
            proto = msg.get_proto()
            if proto is None:
                logger.warning("Subscriber: _publish, msg.get_proto None, msg:{0}".format(msg))
            else:
                if self._callback:
                    self.serial_process_decode(proto._buf)
                    self.serial_process_exec()
                    pass
        pass

    def serial_process_decode(self, msg):
        buf_len = msg._buf[2] << 8 | msg._buf[3]
        if msg._buf[1] == 1 and msg._len == (buf_len+3):
            self._rec_data = msg._buf[4:]

    def sub_serial_msg(self, callback=None, *args):
        self._callback = callback
        self._cb_args = args[0]
        self._cb_kw = args[1]
        pass

    def unsub_serial_msg(self):
        self._callback = None

    def serial_process_exec(self):
        self._callback(self._rec_data, *self._cb_args, **self._cb_kw)

    def serial_read_data(self, msg_len):
        pass

    def serial_param_set(self, baud_rate=0, data_bit=1,
                         odd_even=0, stop_bit=0, rx_en=1,
                         tx_en=1, rx_size=50, tx_size=50):
        """ 底盘串口参数设置

        默认设置：'9600', 'bit8', 'none', '1'

        :param baud_rate: 串口波特率，设置范围：0~4映射‘9600’，‘19200’，‘38400’，‘57600’，‘115200’
        :param data_bit:  数据位设置，设置范围：0~3映射‘bit7’, 'bit8', 'bit9', 'bit10'
        :param odd_even:  数据校验位，设置范围：0~3映射‘none’, 'odd', 'even'
        :param stop_bit:  停止位，设置范围：1~2
        :param rx_en: 接收使能
        :param tx_en: 发送使能
        :param rx_size: 接收buff大小
        :param tx_size: 发送buff大小
        :return: 返回串口设置结果
        """
        proto = protocol.ProtoChassisSerialSet()
        proto._baud_rate = baud_rate
        proto._data_bit = data_bit
        proto._odd_even = odd_even
        proto._stop_bit = stop_bit
        proto._rx_en = rx_en
        proto._tx_en = tx_en
        proto._rx_size = rx_size
        proto._tx_size = tx_size
        return self._send_sync_proto(proto, protocol.host2byte(3, 6))

    def serial_send_msg(self, msg_buf):
        """
        底盘串口数据数据发送

        :param msg_buf: 发送的数据
        :param msg_len: 发送的数据长度
        :return: 返回串口数据发送结果
        """
        proto = protocol.ProtoChassisSerialMsgSend()
        # 字符串转字节流
        if type(msg_buf) == str:
            proto._msg_buf = msg_buf.encode()
        # 元祖转字节流
        elif type(msg_buf) == tuple:
            proto._msg_buf = (','.join('%s' % d for d in msg_buf)).encode()
        # 字典转字节流
        elif type(msg_buf) == dict:
            proto._msg_buf = str(msg_buf).encode()
        elif type(msg_buf) == bytearray:
            proto._msg_buf = msg_buf
        else:
            return False

        proto._msg_len = len(proto._msg_buf)
        return self._send_sync_proto(proto, protocol.host2byte(3, 6))
