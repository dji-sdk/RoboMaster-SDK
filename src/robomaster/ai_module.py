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

__all__ = ['AiModule', 'TelloAI']

IS_AI_FLAG = ";degree:"


class AiModuleEvent(dds.Subject):
    name = "ai_event"
    cmdset = 0x3f
    cmdid = 0xea
    type = dds.DDS_SUB_TYPE_EVENT

    def __init__(self):
        self._ai_info = []
        self._num = 0

    def data_info(self):
        return self._num, self._ai_info

    def decode(self, buf):
        self._num, self._ai_info = buf


class AiModule(module.Module):
    """ EP AI模块"""

    _host = protocol.host2byte(15, 1)

    def __init__(self, robot):
        super().__init__(robot)

    def init_ai_module(self):
        proto = protocol.ProtoRoboticAiInit()
        return self._send_async_proto(proto, target=protocol.host2byte(9, 2))

    def sub_ai_event(self, callback=None, *args, **kw):
        """ 订阅AI信息

        :param freq: enum:(1,5,10) 设置数据订阅数据的推送频率，单位 Hz
        :param callback: 回调函数，返回数据 明文字符串:

                :id: 目标对象ID
                :x: 目标图像的坐标x
                :y: 目标图像的坐标y
                :w: 目标图像的宽度
                :h: 目标图像的高度
                :C: 目标的置信度

        :param args: 可变参数
        :param kw: 关键字参数
        :return: bool: 数据订阅结果
        """
        self.init_ai_module()
        sub = self._robot.dds
        subject = AiModuleEvent()
        protocol.ProtoAiModuleEvent()
        return sub.add_subject_event_info(subject, callback, args, kw)

    def unsub_ai_event(self):
        """ 取消AI数据订阅

        :return: bool: 取消数据订阅结果
        """
        sub = self._robot.dds
        subject = AiModuleEvent()
        return sub.del_subject_event_info(subject)


class TelloAIInfoSubject(dds.Subject):
    name = dds.DDS_TELLO_AI

    def __init__(self):
        super().__init__()
        self._ai = 0
        self._info_num = 1
        self._freq = protocol.TelloDdsProto.DDS_FREQ

    def percent(self):
        return self._ai

    def data_info(self):
        return self._ai

    def decode(self, buf):
        info_buf = buf.split(';')
        ai_info = []
        if len(info_buf) == 7:
            for info in info_buf:
                if ":" in info:
                    if "x" in info:
                        ai_info.append(int(info.split(':')[1]) / 320)
                    elif "y" in info:
                        ai_info.append(int(info.split(':')[1]) / 240)
                    elif "w" in info:
                        ai_info.append(int(info.split(':')[1]) / 320)
                    elif "h" in info:
                        ai_info.append(int(info.split(':')[1]) / 240)
                    else:
                        ai_info.append(info.split(':')[1])
            self._ai = ai_info

        if dds.IS_AI_FLAG in buf:
            return True
        else:
            logger.debug("TelloAIInfoSubject: decode, buf is not match")
            return False


class TelloAI(object):
    """ 教育无人机 AI模块"""

    def __init__(self, robot):
        self._client = robot.client
        self._robot = robot

    def get_ai(self):
        """ 获取AI模块信息

        :return: int: AI模块明文字符串
        """
        cmd = "ai?"
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
                logger.warning("Drone: get_ai failed.")
        except Exception as e:
            logger.warning("Drone: get_ai, send_sync_msg exception {0}".format(str(e)))
            return None

    def sub_ai_info(self, freq=5, callback=None, *args, **kw):
        """ 订阅AI信息

        :param freq: enum:(1,5,10) 设置数据订阅数据的推送频率，单位 Hz
        :param callback: 回调函数，返回数据 明文字符串:

                :id: 目标对象ID
                :x: 目标图像的坐标x
                :y: 目标图像的坐标y
                :w: 目标图像的宽度
                :h: 目标图像的高度
                :C: 目标的置信度

        :param args: 可变参数
        :param kw: 关键字参数
        :return: bool: 数据订阅结果
        """
        sub = self._robot.dds
        subject = TelloAIInfoSubject()
        subject.freq = freq
        return sub.add_subject_info(subject, callback, args, kw)

    def unsub_ai_info(self):
        """ 取消订阅AI模块信息

        :return: 返回取消订阅结果
        """
        sub_dds = self._robot.dds
        return sub_dds.del_subject_info(dds.DDS_TELLO_AI)
