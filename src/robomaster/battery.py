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
import struct

__all__ = ['Battery', 'TelloBattery']


class TelloBatInfoSubject(dds.Subject):
    name = dds.DDS_TELLO_BATTERY

    def __init__(self):
        super().__init__()
        self._bat = 0
        self._info_num = 1
        self._freq = protocol.TelloDdsProto.DDS_FREQ

    def percent(self):
        return self._bat

    def data_info(self):
        return self._bat

    def decode(self, buf):
        push_info = buf.split(';')
        found_info_num = 0
        for info in push_info:
            if protocol.TelloDdsProto.DDS_BATTERY_FLAG in info:
                self._bat = int(info.split(':')[1])
                found_info_num += 1
        if found_info_num == self._info_num:
            return True
        else:
            logger.debug("TelloBatInfoSubject: decode, found_info_num {0} is not match self._info_num {1}".format(
                found_info_num, self._info_num))
            return False

    @property
    def freq(self):
        return self._freq

    @freq.setter
    def freq(self, in_freq):
        if in_freq == 1 or in_freq == 5 or in_freq == 10:
            self._freq = in_freq


class BatterySubject(dds.Subject):
    name = dds.DDS_BATTERY
    uid = dds.SUB_UID_MAP[name]

    def __init__(self):
        self._adc_value = 0
        self._temperature = 0
        self._current = 0
        self._percent = 0

    @property
    def percent(self):
        return self._percent

    def data_info(self):
        return self._percent

    def decode(self, buf):
        self._adc_value, self._temperature, self._current, self._percent, recv = struct.unpack('<HhiBB', buf)
        return self._percent


class TelloBattery(object):
    """ 教育无人机 电池模块"""

    def __init__(self, robot):
        self._client = robot.client
        self._robot = robot

    def get_battery(self):
        """ 获取电池电量信息

        :return: int: 电池的剩余电量百分比
        """
        cmd = "battery?"
        proto = protocol.TextProtoDrone()
        proto.text_cmd = cmd
        msg = protocol.TextMsg(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                if proto:
                    return int(proto.resp)
                else:
                    return None
            else:
                logger.warning("Drone: get_battery failed.")
        except Exception as e:
            logger.warning("Drone: get_battery, send_sync_msg exception {0}".format(str(e)))
            return None

    def sub_battery_info(self, freq=5, callback=None, *args, **kw):
        """ 订阅电池信息

        :param freq: enum:(1,5,10) 设置数据订阅数据的推送频率，单位 Hz
        :param callback: 回调函数，返回数据 percent:

                        :percent: 电池电量百分比

        :param args: 可变参数
        :param kw: 关键字参数
        :return: bool: 数据订阅结果
        """
        sub = self._robot.dds
        subject = TelloBatInfoSubject()
        subject.freq = freq
        return sub.add_subject_info(subject, callback, args, kw)

    def unsub_battery_info(self):
        """ 取消订阅飞机电池信息

        :return: 返回取消订阅结果
        """
        sub_dds = self._robot.dds
        return sub_dds.del_subject_info(dds.DDS_TELLO_BATTERY)


class Battery(module.Module):
    """ EP 电池模块"""

    _host = protocol.host2byte(11, 0)

    def __init__(self, robot):
        super().__init__(robot)

    def sub_battery_info(self, freq=5, callback=None, *args, **kw):
        """ 订阅电池信息

        :param freq: enum:(1,5,10,20,50) 设置数据订阅数据的推送频率，单位 Hz
        :param callback: 回调函数，返回数据 percent:

                        :percent: 电池电量百分比

        :param args: 可变参数
        :param kw: 关键字参数
        :return: bool: 数据订阅结果
        """
        sub = self._robot.dds
        subject = BatterySubject()
        subject.freq = freq
        return sub.add_subject_info(subject, callback, args, kw)

    def unsub_battery_info(self):
        """ 取消电池订阅

        :return: bool: 取消订阅结果
        """
        sub_dds = self._robot.dds
        return sub_dds.del_subject_info(dds.DDS_BATTERY)
