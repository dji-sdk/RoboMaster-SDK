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
from . import util

__all__ = ['Gripper']


class GripperSubject(dds.Subject):
    name = dds.DDS_GRIPPER
    uid = dds.SUB_UID_MAP[name]
    cmdset = 0x48
    cmdid = 0x08

    def __init__(self):
        self._status = 0

    @property
    def status(self):
        if self._status == 1:
            return "opened"
        elif self._status == 2:
            return "closed"
        elif self._status == 0:
            return "normal"
        else:
            logger.warning("GripperSubject: unsupported status:{0}".format(self._status))
            return ""

    def data_info(self):
        return self.status

    def decode(self, buf):
        self._status = buf[0]


class Gripper(module.Module):
    """ EP 机械爪模块 """

    _host = protocol.host2byte(27, 1)

    def __init__(self, robot):
        super().__init__(robot)

    def reset(self):
        pass

    def open(self, power=50):
        """ 控制机械爪张开

        :param power: int: [1, 100]，控制出力
        :return: bool: 调用结果
        """
        proto = protocol.ProtoGripperCtrl()
        proto._control = 1
        proto._power = util.GRIPPER_POWER_CHECK.val2proto(power)
        return self._send_sync_proto(proto, protocol.host2byte(3, 6))

    def close(self, power=50):
        """ 控制机械爪关闭

        :param power: int: [1, 100]，控制出力
        :return: bool: 调用结果
        """
        proto = protocol.ProtoGripperCtrl()
        proto._control = 2
        proto._power = util.GRIPPER_POWER_CHECK.val2proto(power)
        return self._send_sync_proto(proto, protocol.host2byte(3, 6))

    def pause(self):
        """ 控制机械爪停止

        :return: bool: 调用结果
        """
        proto = protocol.ProtoGripperCtrl()
        proto._control = 0
        proto._power = 0
        return self._send_sync_proto(proto, protocol.host2byte(3, 6))

    def sub_status(self, freq=5, callback=None, *args, **kw):
        """ 订阅夹爪的状态信息

        :param freq: enum: (1, 5, 10, 20, 50)，设置数据订阅数据的推送频率，单位 Hz
        :param callback: 传入数据处理的回调函数,回调函数参数为：

                        :gripper_status: opened:夹爪打开 closed:夹爪闭合。
        :param callback: 回调函数，返回数据 (status):

                        :status: opened 夹爪完全打开，closed 夹爪完全闭合，normal 处在中间正常状态

        :param args: 可变参数
        :param kw: 关键字参数
        :return: bool: 数据订阅结果
        """
        sub = self._robot.dds
        subject = GripperSubject()
        subject.freq = freq
        return sub.add_subject_info(subject, callback, args, kw)

    def unsub_status(self):
        """ 取消夹爪状态信息订阅

        :return: 取消订阅结果
        """
        sub_dds = self._robot.dds
        return sub_dds.del_subject_info(dds.DDS_GRIPPER)
