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
from . import dds
from . import logger

__all__ = ['DistanceSensor', 'SensorAdaptor']


class TofSubject(dds.Subject):
    name = dds.DDS_TOF
    uid = dds.SUB_UID_MAP[name]

    def __init__(self):
        self._cmd_id = [0] * 4
        self._direct = [0] * 4
        self._flag = [0] * 4
        self._distance = [0] * 4

    def tof(self):
        """ 距离传感器数据获取

        :return: 距离传感器的ID、对应的距离，单位为mm
        """
        return self._cmd_id, self._distance

    def data_info(self):
        return self._distance

    def decode(self, buf):
        for i in range(0, 4):
            self._cmd_id[i] = buf[i * 5]
            self._direct[i] = buf[i * 5 + 1]
            self._flag[i] = buf[i * 5 + 2]
            self._distance[i] = buf[i * 5 + 3] * 256 + buf[i * 5 + 4]


class AdapterSubject(dds.Subject):
    name = dds.DDS_PINBOARD
    uid = dds.SUB_UID_MAP[name]

    def __init__(self):
        self._io_value = [0] * 12
        self._ad_value = [0] * 12

    def adapter(self):
        """ 距离传感器转接板数据获取

        :return: i/o值、ad值
        """
        return self._io_value, self._ad_value

    def data_info(self):
        return self._io_value, self._ad_value

    def decode(self, buf):
        for i in range(0, 6):
            self._io_value[i * 2] = buf[i * 6]
            self._io_value[i * 2 + 1] = buf[i * 6 + 1]
            self._ad_value[i * 2] = buf[i * 6 + 2] + buf[i * 6 + 3] * 256
            self._ad_value[i * 2 + 1] = buf[i * 6 + 4] + 256 * buf[i * 6 + 5]


class DistanceSensor(module.Module):
    """ EP 距离传感器模块 """

    _host = protocol.host2byte(18, 1)

    def __init__(self, robot):
        super().__init__(robot)
        pass

    def sub_distance(self, freq=5, callback=None, *args, **kw):
        """
        订阅距离传感器测量的距离信息

        :param freq: 订阅数据的频率，支持的订阅频率为1、5、10、20、50hz
        :param callback: 传入数据处理的回调函数，回调函数的参数为：

                        :distance[4]: 4个tof的距离信息

        :param args: 传入参数。
        :return: 返回订阅结果。
        """
        sub = self._robot.dds
        subject = TofSubject()
        subject.freq = freq
        return sub.add_subject_info(subject, callback, args, kw)

    def unsub_distance(self):
        """ 取消距离传感器的信息订阅。"""
        sub_dds = self._robot.dds
        return sub_dds.del_subject_info(dds.DDS_TOF)


class SensorAdaptor(module.Module):
    """ EP 传感器板模块 """

    _host = protocol.host2byte(22, 0)

    def __init__(self, robot):
        super().__init__(robot)

    def get_adc(self, id=1, port=1):
        """ 传感器板adc值获取

        :param id: int[1,8]，传感器板编号
        :param port: int:[1,2]，传感器板端口号
        :return: adc值
        """
        proto = protocol.ProtoSensorGetData()
        proto._port = port
        msg = protocol.Msg(self._client.hostbyte, protocol.host2byte(22, id), proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                prot = resp_msg.get_proto()
                adc = prot._adc
                return adc
            else:
                return None
        except Exception as e:
            logger.warning("SensorAdaptor: get_adc, send_sync_msg exception {0}".format(str(e)))
            return None

    def get_io(self, id=1, port=1):
        """ 传感器板io电平值获取

        :param id: int[1,8], 传感器板编号
        :param port: int:[1,2], 传感器板端口号
        :return: io电平值
        """
        proto = protocol.ProtoSensorGetData()
        proto._port = port
        msg = protocol.Msg(self._client.hostbyte, protocol.host2byte(22, id), proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                prot = resp_msg.get_proto()
                io = prot._io
                return io
            else:
                return None
        except Exception as e:
            logger.warning("SensorAdaptor: get_io, send_sync_msg exception {0}".format(str(e)))
            return None

    def get_pulse_period(self, id=1, port=1):
        """ 传感器板电平持续时间获取

        :param id: int[1,8], 传感器板编号
        :param port: int:[1,2], 传感器板端口号
        :return: 电平持续时间,单位ms
        """
        proto = protocol.ProtoSensorGetData()
        proto._port = port
        msg = protocol.Msg(self._client.hostbyte, protocol.host2byte(22, id), proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                prot = resp_msg.get_proto()
                time = prot._time
                return time
            else:
                return None
        except Exception as e:
            logger.warning("SensorAdaptor: get_pulse_period, send_sync_msg exception {0}".format(str(e)))
            return None

    def sub_adapter(self, freq=5, callback=None, *args, **kw):
        """
        订阅传感器转接板信息

        :param freq: 订阅数据的频率，支持的订阅频率为1、5、10、20、50hz
        :param callback: 传入数据处理的回调函数，回调函数的参数为：

                        :adapter[6]: 6个adapter的io/ad信息

        :param args: 传入参数。
        :return: 返回订阅结果。
        """
        sub = self._robot.dds
        subject = AdapterSubject()
        subject.freq = freq
        return sub.add_subject_info(subject, callback, args, kw)

    def unsub_adapter(self):
        """ 取消传感器转接板的信息订阅。"""
        sub_dds = self._robot.dds
        return sub_dds.del_subject_info(dds.DDS_PINBOARD)


class TelloDistanceSensor(object):
    """ 教育无人机 距离传感器模块 """

    def __init__(self, robot):
        self._client = robot.client
        self._robot = robot

    def get_ext_tof(self):
        """ 获取扩展模块tof传感器的数值

        :return: float: 扩展模块tof传感器的值
        """
        cmd = "EXT tof?".format()
        proto = protocol.TextProtoDrone()
        proto.text_cmd = cmd
        msg = protocol.TextMsg(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                if proto:
                    return float(proto.resp[4:])
            logger.warning("Drone: get ext tof failed.")
            return None
        except Exception as e:
            logger.warning("Drone: get ext tof, send_sync_msg exception {0}".format(str(e)))
            return None
