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
from . import action
from . import logger
from . import dds
from . import util
import struct


__all__ = ['RoboticArm']


class ArmSubject(dds.Subject):
    name = dds.DDS_ARM
    uid = dds.SUB_UID_MAP[name]
    type = dds.DDS_SUB_TYPE_PERIOD

    def __init__(self):
        self._x_limit = 0
        self._y_limit = 0
        self._main_servo_lock = 0
        self._sub_servo_lock = 0
        self._pos_x = 0
        self._pos_y = 0

    def arm_data(self):
        """ 获取机械臂信息

        :return: tuple: (x, y), 机械臂的坐标
        """
        return self._pos_x, self._pos_y

    def data_info(self):
        return self._pos_x, self._pos_y

    def decode(self, buf):
        self._pos_x, self._pos_y = struct.unpack('<II', buf[1:])


class RoboticArmMoveAction(action.Action):
    _action_proto_cls = protocol.ProtoRoboticArmMoveCtrl
    _push_proto_cls = protocol.ProtoRoboticArmMovePush
    _target = protocol.host2byte(3, 6)

    def __init__(self, x=0, y=0, z=0, mode=0, **kw):
        super().__init__(**kw)
        self._x = x
        self._y = y
        self._z = z
        self._mode = mode

    def __repr__(self):
        return "action_id:{0}, state:{1}, percent:{2}, x:{3}, y:{4}, z:{5}".format(
            self._action_id, self._state, self._percent, self._x, self._y, self._z)

    def encode(self):
        proto = protocol.ProtoRoboticArmMoveCtrl()
        proto._x = util.ROBOTIC_ARM_POS_CHECK.val2proto(self._x)
        proto._y = util.ROBOTIC_ARM_POS_CHECK.val2proto(self._y)
        proto._z = util.ROBOTIC_ARM_POS_CHECK.val2proto(self._z)
        proto._mode = self._mode
        proto._mask = 0x03
        return proto

    def update_from_push(self, proto):
        if proto.__class__ is not self._push_proto_cls:
            return

        self._percent = proto._percent
        self._update_action_state(proto._action_state)

        self._x = proto._x
        self._y = proto._y
        self._z = proto._z
        logger.info("{0} update_from_push: {1}".format(self.__class__.__name__, self))


class RoboticArm(module.Module):
    """ EP 机械臂 模块 """

    _host = protocol.host2byte(27, 2)

    def __init__(self, robot):
        super().__init__(robot)
        self._action_dispatcher = robot.action_dispatcher

    def reset(self):
        pass

    def recenter(self):
        """ 控制机械臂回中

        :return: action对象
        """
        return self.moveto(x=0, y=0)

    def move(self, x=0, y=0):
        """ 机械臂相对位置移动

        :param x: float, x轴运动距离，向前移动为正方向，单位 mm
        :param y: float, y轴运动距离，向上移动为正方向，单位 mm
        :return: action对象
        """
        action = RoboticArmMoveAction(x, y, z=0, mode=0)
        self._action_dispatcher.send_action(action)
        return action

    def moveto(self, x=0, y=0):
        """ 机械臂绝对位置移动

        :param x: float, x轴运动距离，向前移动为正方向，单位 mm
        :param y: float, y轴运动距离，向上移动为正方向，单位 mm
        :return: action对象
        """
        action = RoboticArmMoveAction(x, y, z=0, mode=1)
        self._action_dispatcher.send_action(action)
        return action

    def sub_position(self, freq=5, callback=None, *args, **kw):
        """ 订阅机械臂的位置信息

        :param freq: enum:(1,5,10,20,50) 设置数据订阅数据的推送频率，单位 Hz
        :param callback: 回调函数，返回数据 (pos_x, pos_y)：

                        :pos_x: 机械臂x轴位置信息
                        :pos_y: 机械臂y轴位置信息

        :param args: 可变参数
        :param kw: 关键字参数
        :return: bool: 数据订阅结果
        """
        sub = self._robot.dds
        subject = ArmSubject()
        subject.freq = freq
        return sub.add_subject_info(subject, callback, args, kw)

    def unsub_position(self):
        """ 取消机械臂位置信息订阅

        :return: bool: 取消订阅结果
        """
        sub_dds = self._robot.dds
        return sub_dds.del_subject_info(dds.DDS_ARM)
