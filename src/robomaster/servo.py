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


from . import module
from . import protocol
from . import logger
from . import dds
from . import action
import struct

__all__ = ['Servo']


class ServoSubject(dds.Subject):
    name = dds.DDS_SERVO
    uid = dds.SUB_UID_MAP[name]

    def __init__(self):
        self._valid = [0] * 4
        self._recv = [0]
        self._speed = [0] * 4
        self._angle = [0] * 4

    def servo_data(self):
        return self._valid, self._speed, self._angle

    def data_info(self):
        return self._valid, self._speed, self._angle

    def decode(self, buf):
        self._valid[0] = buf[0] & 0x01
        self._valid[1] = (buf[0] >> 1) & 0x01
        self._valid[2] = (buf[0] >> 2) & 0x01
        self._valid[3] = (buf[0] >> 3) & 0x01
        [self._recv, self._speed[0], self._speed[1], self._speed[2], self._speed[3],
         self._angle[0], self._angle[1], self._angle[2], self._angle[3]] = struct.unpack('<Bhhhhhhhh', buf)


class ServoSetAngleAction(action.Action):
    _action_proto_cls = protocol.ProtoServoCtrlSet
    _push_proto_cls = protocol.ProtoServoCtrlPush
    _target = protocol.host2byte(3, 6)

    def __init__(self, index=0, angle=0, **kw):
        super().__init__(**kw)
        self._id = index
        self._value = angle
        self._angle = 0

    def __repr__(self):
        return "action_id:{0}, state:{1}, percent:{2}, value:{3}".format(
            self._action_id, self._state, self._percent, self._angle)

    def encode(self):
        proto = protocol.ProtoServoCtrlSet()
        proto._id = self._id
        proto._value = (self._value+180)*10
        return proto

    def update_from_push(self, proto):
        if proto.__class__ is not self._push_proto_cls:
            return

        self._percent = proto._percent
        self._update_action_state(proto._action_state)

        self._angle = proto._value
        logger.info("{0} update_from_push: {1}".format(self.__class__.__name__, self))


class Servo(module.Module):
    """ EP 舵机模块 """

    _host = protocol.host2byte(3, 5)

    def __init__(self, robot):
        super().__init__(robot)
        self._action_dispatcher = robot.action_dispatcher

    def moveto(self, index=0, angle=0):
        """ 舵机绝对位置移动

        :param index: int [1, 3]，舵机编号
        :param angle: int: [-180, 180]，舵机旋转角度，单位（°）
        :return: action对象
        """
        action = ServoSetAngleAction(index, angle)
        self._action_dispatcher.send_action(action)
        return action

    def drive_speed(self, index=0, speed=0):
        proto = protocol.ProtoServoModeSet()
        proto._id = (index << 5) + 0x19
        proto._mode = 1
        msg = protocol.Msg(self._client.hostbyte, self._host, proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                prot = resp_msg.get_proto()
                if prot._retcode == 0:
                    proto = protocol.ProtoServoControl()
                    proto._id = (index << 5) + 0x19
                    proto._enable = 1
                    proto._value = int(((speed + 49) * 900) / 98)
                    msg = protocol.Msg(self._client.hostbyte, self._host, proto)
                    try:
                        resp_msg = self._client.send_sync_msg(msg)
                        if resp_msg:
                            prot = resp_msg.get_proto()
                            if prot._retcode == 0:
                                return True
                            else:
                                return False
                        else:
                            return False
                    except Exception as e:
                        logger.warning("Servo: drive_speed, e {0}".format(e))
                        return False
                else:
                    return False
            else:
                return False
        except Exception as e:
            logger.warning("Servo: drive_speed, send_sync_msg e {0}".format(e))
            return False

    def pause(self, index=0):
        """ 停止

        :param index: int: [1, 3]，舵机编号
        :return bool: 调用结果
        """
        proto = protocol.ProtoServoControl()
        proto._id = (index << 5) + 0x19
        proto._enable = 0
        proto._value = 0
        msg = protocol.Msg(self._client.hostbyte, self._host, proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                prot = resp_msg.get_proto()
                if prot._retcode == 0:
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            logger.warning("Servo: pause, send_sync_msg e {0}".format(e))
            return False

    def get_angle(self, index=1):
        """ 获取舵机角度值

        :param index: int: [1，3]，舵机编号
        :return: int 舵机角度
        """
        proto = protocol.ProtoServoGetAngle()
        proto._id = (index << 5) + 0x19
        msg = protocol.Msg(self._client.hostbyte, self._host, proto)
        print(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                prot = resp_msg.get_proto()
                angle = prot._angle
                return angle
            else:
                return False
        except Exception as e:
            logger.warning("Servo: get_angle, send_sync_msg e {0}".format(e))
            return False

    def sub_servo_info(self, freq=5, callback=None, *args, **kw):
        """  订阅舵机角度信息

        :param freq: enum: (1, 5, 10, 20, 50) 设置数据订阅数据的推送频率，单位 Hz
        :param callback: 回调函数，返回数据 (valid[4], speed[4], angle[4]):

                        :valid[4]: 4个舵机在线状态
                        :speed[4]: 4个舵机的速度值
                        :angle[4]: 4个舵机的角度值

        :param args: 可变参数
        :param kw: 关键字参数
        :return: bool: 数据订阅结果
        """
        sub = self._robot.dds
        subject = ServoSubject()
        subject.freq = freq
        return sub.add_subject_info(subject, callback, args, kw)

    def unsub_servo_info(self):
        """ 取消订阅舵机的角度信息
        :return: bool: 调用结果
        """
        sub_dds = self._robot.dds
        return sub_dds.del_subject_info(dds.DDS_SERVO)
