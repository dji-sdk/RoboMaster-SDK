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


import time
import collections
import threading
from queue import Queue
from abc import abstractmethod
from . import logger
from . import module
from . import protocol
from concurrent.futures import ThreadPoolExecutor


SDK_FIRST_DDS_ID = 20
SDK_LAST_DDS_ID = 255

DDS_BATTERY = "battery"
DDS_GIMBAL_BASE = "gimbal_base"
DDS_VELOCITY = "velocity"
DDS_ESC = "esc"
DDS_ATTITUDE = "attitude"
DDS_IMU = "imu"
DDS_POSITION = "position"
DDS_SA_STATUS = "sa_status"
DDS_CHASSIS_MODE = "chassis_mode"
DDS_SBUS = "sbus"
DDS_SERVO = "servo"
DDS_ARM = "arm"
DDS_GRIPPER = "gripper"
DDS_GIMBAL_POS = "gimbal_pos"
DDS_STICK = "stick"
DDS_MOVE_MODE = "move_mode"
DDS_TOF = "tof"
DDS_PINBOARD = "pinboard"

DDS_TELLO_ATTITUDE = "tello_attitude"
DDS_TELLO_BATTERY = "tello_battery"
DDS_TELLO_AI = "tello_ai"
DDS_TELLO_TEMP = "tello_temperature"
DDS_TELLO_IMU = "tello_imu"
DDS_TELLO_TOF = "tello_tof"
DDS_TELLO_DRONE = "tello_drone"
DDS_TELLO_ALL = "tello_all"
IS_AI_FLAG = ";degree:"
TELLO_DDS_TIME_MAX = 666

SUB_UID_MAP = {
    DDS_BATTERY: 0x000200096862229f,
    DDS_GIMBAL_BASE: 0x00020009f5882874,
    DDS_VELOCITY: 0x0002000949a4009c,
    DDS_ESC: 0x00020009c14cb7c5,
    DDS_ATTITUDE: 0x000200096b986306,
    DDS_IMU: 0x00020009a7985b8d,
    DDS_POSITION: 0x00020009eeb7cece,
    DDS_SA_STATUS: 0x000200094a2c6d55,
    DDS_CHASSIS_MODE: 0x000200094fcb1146,
    DDS_SBUS: 0x0002000988223568,
    DDS_SERVO: 0x000200095f0059e7,
    DDS_ARM: 0x0002000926abd64d,
    DDS_GRIPPER: 0x00020009124d156a,
    DDS_GIMBAL_POS: 0x00020009f79b3c97,
    DDS_STICK: 0x0002000955e9a0fa,
    DDS_MOVE_MODE: 0x00020009784c7bfd,
    DDS_TOF: 0x0002000986e4c05a,
    DDS_PINBOARD: 0x00020009eebb9ffc,
}

DDS_SUB_TYPE_EVENT = 1
DDS_SUB_TYPE_PERIOD = 0

registered_subjects = {}
dds_cmd_filter = {(0x48, 0x08)}


class _AutoRegisterSubject(type):
    '''hepler to automatically register Proto Class whereever they're defined '''

    def __new__(mcs, name, bases, attrs, **kw):
        return super().__new__(mcs, name, bases, attrs, **kw)

    def __init__(cls, name, bases, attrs, **kw):
        super().__init__(name, bases, attrs, **kw)
        if name == 'Subject':
            return
        key = name
        if key in registered_subjects.keys():
            raise ValueError("Duplicate Subject class {0}".format(name))
        registered_subjects[key] = cls


class Subject(metaclass=_AutoRegisterSubject):
    name = "Subject"
    _push_proto_cls = protocol.ProtoPushPeriodMsg
    type = DDS_SUB_TYPE_PERIOD
    uid = 0
    freq = 1

    def __init__(self):
        self._task = None
        self._subject_id = 1
        self._callback = None
        self._cb_args = None
        self._cb_kw = None

    def __repr__(self):
        return "dds subject, name:{0}".format(self.name)

    def set_callback(self, callback, args, kw):
        self._callback = callback
        self._cb_args = args
        self._cb_kw = kw

    @abstractmethod
    def data_info(self):
        return None

    def exec(self):
        self._callback(self.data_info(), *self._cb_args, **self._cb_kw)


class SubHandler(collections.namedtuple("SubHandler", ("obj subject f"))):
    __slots__ = ()


class Subscriber(module.Module):
    _host = protocol.host2byte(9, 0)
    _sub_msg_id = SDK_FIRST_DDS_ID

    def __init__(self, robot):
        super().__init__(robot)
        self._robot = robot

        self.msg_sub_dict = {}
        self._publisher = collections.defaultdict(list)
        self._msg_queue = Queue()
        self._dispatcher_running = False
        self._dispatcher_thread = None
        self.excutor = ThreadPoolExecutor(max_workers=15)

    def __del__(self):
        self.stop()

    def get_next_subject_id(self):
        if self._sub_msg_id > SDK_LAST_DDS_ID:
            self._sub_msg_id = SDK_FIRST_DDS_ID
        else:
            self._sub_msg_id += 1
        return self._sub_msg_id

    def start(self):
        self._dds_mutex = threading.Lock()
        self._client.add_handler(self, "Subscriber", self._msg_recv)
        self._dispatcher_thread = threading.Thread(target=self._dispatch_task)
        self._dispatcher_thread.start()

    def stop(self):
        self._dispatcher_running = False
        if self._dispatcher_thread:
            self._msg_queue.put(None)
            self._dispatcher_thread.join()
            self._dispatcher_thread = None
        self.excutor.shutdown(wait=False)

    @classmethod
    def _msg_recv(cls, self, msg):
        for cmd_set, cmd_id in list(dds_cmd_filter):
            if msg.cmdset == cmd_set and msg.cmdid == cmd_id:
                self._msg_queue.put(msg)

    def _dispatch_task(self):
        self._dispatcher_running = True
        logger.info("Subscriber: dispatcher_task is running...")
        while self._dispatcher_running:
            msg = self._msg_queue.get(1)
            if msg is None:
                if not self._dispatcher_running:
                    break
                continue
            self._dds_mutex.acquire()
            for name in self._publisher:
                handler = self._publisher[name]
                logger.debug("Subscriber: msg: {0}".format(msg))
                proto = msg.get_proto()
                if proto is None:
                    logger.warning("Subscriber: _publish, msg.get_proto None, msg:{0}".format(msg))
                    continue
                if handler.subject.type == DDS_SUB_TYPE_PERIOD and\
                        msg.cmdset == 0x48 and msg.cmdid == 0x08:
                    logger.debug("Subscriber: _publish: msg_id:{0}, subject_id:{1}".format(proto._msg_id,
                                                                                           handler.subject._subject_id))
                    if proto._msg_id == handler.subject._subject_id:
                        handler.subject.decode(proto._data_buf)
                        if handler.subject._task is None:
                            handler.subject._task = self.excutor.submit(handler.subject.exec)
                        if handler.subject._task.done() is True:
                            handler.subject._task = self.excutor.submit(handler.subject.exec)
                elif handler.subject.type == DDS_SUB_TYPE_EVENT:
                    if handler.subject.cmdset == msg.cmdset and handler.subject.cmdid == msg.cmdid:
                        handler.subject.decode(proto._data_buf)
                        if handler.subject._task is None:
                            handler.subject._task = self.excutor.submit(handler.subject.exec)
                        if handler.subject._task.done() is True:
                            handler.subject._task = self.excutor.submit(handler.subject.exec)
            self._dds_mutex.release()
            logger.info("Subscriber: _publish, msg is {0}".format(msg))

    def add_cmd_filter(self, cmd_set, cmd_id):
        dds_cmd_filter.add((cmd_set, cmd_id))

    def del_cmd_filter(self, cmd_set, cmd_id):
        dds_cmd_filter.remove((cmd_set, cmd_id))

    def add_subject_event_info(self, subject, callback=None, *args):
        """ 添加事件订阅

        :param subject: 事件订阅对应的subject
        :param callback: 事件订阅对应的解析函数
        """
        # 添加时间订阅仅 增加 Filter
        subject.set_callback(callback, args[0], args[1])
        handler = SubHandler(self, subject, callback)
        subject._task = None
        self._dds_mutex.acquire()
        self._publisher[subject.name] = handler
        self._dds_mutex.release()
        self.add_cmd_filter(subject.cmdset, subject.cmdid)
        return True

    def del_subject_event_info(self, subject):
        """ 删除事件订阅

        :param subject: 事件订阅对应的subject
        :param callback: 事件订阅对应的解析函数
        :return: bool: 调用结果
        """
        # 删除事件订阅仅从 Filter 中删除
        if self._publisher[subject.name].subject._task is None:
            pass
        elif self._publisher[subject.name].subject._task.done() is False:
            self._publisher[subject.name].subject._task.cancel()
        self.del_cmd_filter(subject.cmdset, subject.cmdid)
        return True

    def add_subject_info(self, subject, callback=None, *args):
        """ 请求数据订阅底层接口

        :param subject: 数据订阅对应subject
        :param callback: 订阅数据对应的解析函数
        :return: bool: 调用结果
        """
        # add handler to publisher.
        subject.set_callback(callback, args[0], args[1])
        handler = SubHandler(self, subject, callback)
        self._dds_mutex.acquire()
        self._publisher[subject.name] = handler
        self._dds_mutex.release()
        proto = protocol.ProtoAddSubMsg()
        proto._node_id = self.client.hostbyte
        proto._sub_freq = subject.freq
        proto._sub_data_num = 1
        proto._msg_id = self.get_next_subject_id()
        subject._subject_id = proto._msg_id
        subject._task = None
        proto._sub_uid_list.append(subject.uid)
        return self._send_sync_proto(proto, protocol.host2byte(9, 0))

    def del_subject_info(self, subject_name):
        """ 删除数据订阅消息

        :param subject_name: 要删除的订阅subject
        :return: bool: 删除数据订阅结果
        """
        logger.debug("Subscriber: del_subject_info: name:{0}, self._publisher:{1}".format(subject_name,
                     self._publisher))
        if subject_name in self._publisher:
            subject_id = self._publisher[subject_name].subject._subject_id
            if self._publisher[subject_name].subject._task.done() is False:
                self._publisher[subject_name].subject._task.cancel()
            self._dds_mutex.acquire()
            del self._publisher[subject_name]
            self._dds_mutex.release()
            proto = protocol.ProtoDelMsg()
            proto._msg_id = subject_id
            proto._node_id = self.client.hostbyte
            return self._send_sync_proto(proto, protocol.host2byte(9, 0))
        else:
            logger.warning("Subscriber: fail to del_subject_info", subject_name)


class TelloSubscriber(object):

    def __init__(self, robot):
        self._robot = robot
        self._publisher = collections.defaultdict(list)
        self._dispatcher_running = False
        self._dispatcher_thread = None
        self._client = self._robot.client
        self._msg = None
        self._freq = protocol.TelloDdsProto.DDS_FREQ

    def __del__(self):
        self.stop()

    def start(self):
        self._client.add_handler(self, "TelloSubscriber", self._msg_recv)
        self._dispatcher_thread = threading.Thread(target=self._dispatch_task)
        self._dispatcher_thread.start()

    def stop(self):
        self._dispatcher_running = False
        if self._dispatcher_thread:
            self._dispatcher_thread.join()
            self._dispatcher_thread = None

    @classmethod
    def _msg_recv(cls, self, msg):
        if protocol.TextMsg.IS_DDS_FLAG in msg.get_proto().resp or IS_AI_FLAG in msg.get_proto().resp:
            '''
            此处判断两个标志位，满足任意一个进入条件
            '''
            self._msg = msg

    def _dispatch_task(self):
        self._dispatcher_running = True
        logger.info("TelloSubscriber: dispatcher_task is running...")
        interval = 1 / protocol.TelloDdsProto.DDS_FREQ
        time_count = 0

        while self._dispatcher_running:
            msg = self._msg
            if msg is None:
                if not self._dispatcher_running:
                    break
                continue
            proto = msg.get_proto()
            if proto is None:
                logger.warning("TelloSubscirber: _publist, msg.get_proto None, msg: {0}".format(msg))
                continue
            for name in self._publisher:
                handler = self._publisher[name]
                need_time = protocol.TelloDdsProto.DDS_FREQ / handler.subject.freq
                if time_count % need_time == 0:
                    if handler.subject.decode(proto.resp):
                        handler.subject.exec()
            if time_count > TELLO_DDS_TIME_MAX:
                time_count = 0
            else:
                time_count += 1
            time.sleep(interval)

    def add_subject_info(self, subject, callback=None, *args):
        """ 请求数据订阅底层接口

        :param subject: 数据订阅对应subject
        :param callback: 订阅数据对应的解析函数
        :return: bool: 数据订阅结果
        """
        # add handler to publisher.
        subject.set_callback(callback, args[0], args[1])
        handler = SubHandler(self, subject, callback)
        self._publisher[subject.name] = handler
        logger.debug("TelloSubscriber: add_subject_info, add sub sucessfully")

    def del_subject_info(self, subject_name):
        """ 删除数据订阅消息

        :param subject_name: 要删除的订阅subject
        :return: bool: 删除数据订阅结果
        """
        logger.debug("TelloSubscriber: del_subject_info: name:{0}, self._publisher:{1}".format(subject_name,
                     self._publisher))
        if subject_name in self._publisher:
            del self._publisher[subject_name]
            logger.debug("TelloSubscriber: del_subject_info, del sub sucessfully")
            return True
        else:
            logger.warning("Subscriber: fail to del_subject_info", subject_name)
            return False

    @property
    def freq(self):
        return self._freq

    @freq.setter
    def freq(self, in_freq):
        if in_freq <= 0:
            self._freq = 0
        elif in_freq > protocol.TelloDdsProto.DDS_FREQ:
            self._freq = protocol.TelloDdsProto.DDS_FREQ
        else:
            self._freq = in_freq
