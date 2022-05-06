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


__all__ = ['Vision', 'PERSON', 'GESTURE', 'LINE', 'MARKER', 'ROBOT']


PERSON = "person"
GESTURE = "gesture"
LINE = "line"
MARKER = "marker"
ROBOT = "robot"


class VisionPushEvent(dds.Subject):
    name = "vision_push"
    cmdset = 0x0a
    cmdid = 0xa4
    type = dds.DDS_SUB_TYPE_EVENT

    def __init__(self):
        self._type = 0
        self._status = 0
        self._errcode = 0
        self._rect_info = []

    def data_info(self):
        return self._rect_info

    def decode(self, data):
        _type, status, rect_info = data
        if len(rect_info) == 0:
            self._rect_info = []
            return

        self._type, self._status, self._rect_info = _type, status, rect_info

        logger.info("detect info = {0}".format(Vision._type2info(self._type)))
        if self._type == 2:  # gesture
            for i in range(0, len(self._rect_info)):
                self._rect_info[i][4] = Vision._id2gesture(self._rect_info[i][4])
        elif self._type == 5:  # marker
            for i in range(0, len(self._rect_info)):
                self._rect_info[i][4] = Vision._id2marker(self._rect_info[i][4])


class Vision(module.Module):
    """ EP 视觉识别模块 """

    _host = protocol.host2byte(17, 7)

    def __init__(self, robot):
        super().__init__(robot)
        self.on_detect_event_cb = None
        self._func_mask = 0

    def reset(self):
        self._disable_detection(0)

    @staticmethod
    def _id2marker(marker_id):
        """ ID转换为Marker字符 """
        if marker_id == 1:
            return "red"
        elif marker_id == 2:
            return "yellow"
        elif marker_id == 3:
            return "green"
        elif marker_id == 4:
            return "left"
        elif marker_id == 5:
            return "right"
        elif marker_id == 6:
            return "forward"
        elif marker_id == 7:
            return "backward"
        elif marker_id == 8:
            return "heart"
        elif marker_id == 9:
            return "sword"
        elif 10 <= marker_id <= 19:
            return str(marker_id - 10)
        elif 20 <= marker_id <= 45:
            return chr(marker_id + 65 - 20)
        elif marker_id == 46:
            return "!"
        elif marker_id == 47:
            return "?"
        elif marker_id == 48:
            return "#"
        else:
            logger.warning("Vision: unsupported marker_id:{0}".format(marker_id))
            return ""

    @staticmethod
    def _type2info(det_type):
        if det_type == 1:
            return "person"
        elif det_type == 2:
            return "gesture"
        elif det_type == 4:
            return "line"
        elif det_type == 5:
            return "marker"
        elif det_type == 7:
            return "robot"
        elif det_type == 0:
            return "shoulder"
        else:
            logger.warning("Vision: type2info, unsupported type {0}".format(det_type))

    @staticmethod
    def _id2gesture(gus_id):
        if gus_id == 1:
            return "jump"
        elif gus_id == 2:
            return "left hand up"
        elif gus_id == 3:
            return "right hand up"
        elif gus_id == 4:
            return "victory"
        elif gus_id == 5:
            return "give in"
        elif gus_id == 6:
            return "capture"
        elif gus_id == 7:
            return "left hand wave"
        elif gus_id == 8:
            return "right hand wave"
        if gus_id == 9:
            return "idle"
        else:
            logger.warning("Vision: id2gesture, unsupported id {0}".format(gus_id))

    def sub_detect_info(self, name, color=None, callback=None, *args, **kw):
        """  订阅智能识别消息

        :param name: enum: ("person", "gesture", "line", "marker", "robot")，person 行人，gesture 手势，line 线识别，\
        marker 标签识别，robot 机器人识别
        :param color: enum:("red", "green", "blue"): 指定识别颜色，仅线识别和标签识别时生效
        :param callback: 回调函数，返回数据 (list(rect_info)):

            :rect_info: 包含的信息如下：
                    person 行人识别：(x, y, w, h), x 中心点x轴坐标，y 中心点y轴坐标，w 宽度，h 高度
                    gesture 手势识别：(x, y, w, h), x 中心点x轴坐标，y 中心点y轴坐标，w 宽度，h 高度
                    line 线识别：(x, y, theta, C)，x点x轴坐标，y点y轴坐标，theta切线角，C 曲率
                    marker 识别：(x, y, w, h, marker), x 中心点x轴坐标，y 中心点y轴坐标，w 宽度，h 高度，marker 识别到的标签
                    robot 机器人识别：(x, y, w, h)，x 中心点x轴坐标，y 中心点y轴坐标，w 宽度，h 高度
        """
        self._func_mask = self._get_sdk_function()
        if self._func_mask is None:
            logger.error("Vision: sub_detect_info, get_vision_function failed!")
            return False

        if name is PERSON:
            self._func_mask = self._func_mask | (1 << 1)
        elif name is GESTURE:
            self._func_mask = self._func_mask | (1 << 2)
        elif name is LINE:
            self._func_mask = self._func_mask | (1 << 4)
        elif name is MARKER:
            self._func_mask = self._func_mask | (1 << 5)
        elif name is ROBOT:
            self._func_mask = self._func_mask | (1 << 7)
        else:
            logger.error("Vision: sub_detect_info, params error, name:{0}".format(name))
            return False

        result = self._enable_detection(self._func_mask)

        if result:
            sub = self._robot.dds
            subject = VisionPushEvent()
            protocol.ProtoVisionDetectInfo()
            sub.add_subject_event_info(subject, callback, args, kw)
            if name is LINE or name is MARKER:
                self._set_color(name, color)
            return True
        else:
            logger.warning("Vision: sub_detect_info, add sub event error, name:{0}".format(name))
            return False

    def unsub_detect_info(self, name):
        """ 取消智能订阅消息

        :param name: enum: ("person", "gesture", "line", "marker", "robot")，取消的智能识别功能
        :return: bool: 调用结果
        """
        self._func_mask = self._get_sdk_function()

        if name == PERSON:
            self._func_mask = self._func_mask & ~(1 << 1)
        elif name == GESTURE:
            self._func_mask = self._func_mask & ~(1 << 2)
        elif name == LINE:
            self._func_mask = self._func_mask & ~(1 << 4)
        elif name == MARKER:
            self._func_mask = self._func_mask & ~(1 << 5)
        elif name == ROBOT:
            self._func_mask = self._func_mask & ~(1 << 7)
        else:
            logger.warning("Vision: sub_detect_info, params error, name:{0}".format(name))
            return False
        return self._disable_detection(self._func_mask)

    def _enable_detection(self, name):
        """
        开启视觉检测功能

        :param name: 检测功能的类型
        :return: 返回使能是否成功
        """
        proto = protocol.ProtoVisionDetectEnable()
        proto._type = name
        msg = protocol.Msg(self.client.hostbyte, self._host, proto)
        try:
            resp_msg = self.client.send_sync_msg(msg)
            if resp_msg:
                return True
            else:
                logger.warning("Vision: enable fail")
                return False
        except Exception as e:
            logger.warning("Vision: sub_detect_info, send_sync_msg, exception {0}".format(e))
            return False
        return True

    def _disable_detection(self, func_mask):
        """ 关闭视觉对应类型的检测功能

        :param func_mask: 视觉检测功能类型
        :return: bool: 调用结果
        """
        proto = protocol.ProtoVisionDetectEnable()
        proto._type = func_mask
        msg = protocol.Msg(self._client.hostbyte, self._host, proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                return True
            else:
                logger.warning("Robot: enable vision failed.")
                return False
        except Exception as e:
            logger.warning("Robot: enable vision err, send_sync_msg exception {0}".format(str(e)))
            return False

    def _get_sdk_function(self):
        """ 获取视觉检测的功能类型

        :return: 当前视觉检测的功能类型
        """
        proto = protocol.ProtoVisionDetectStatus()
        msg = protocol.Msg(self._client.hostbyte, self._host, proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                prot = resp_msg.get_proto()
                if prot:
                    return prot._vision_type
                else:
                    return None
            else:
                logger.warning("Robot: get vision type failed.")
                return None
        except Exception as e:
            logger.warning("Robot: get vision type, send_sync_msg exception {0}".format(str(e)))
            return None

    def _set_color(self, name, color):
        proto = protocol.ProtoVisionSetColor()
        if name is LINE:
            proto._type = 1
        elif name is MARKER:
            proto._type = 2
        else:
            logger.warning("Vision: _set_color, unsupported name {0}".format(name))
            return False
        if color == "red":
            proto._color = 1
        elif color == "green":
            proto._color = 2
        elif color == "blue":
            proto._color = 3
        else:
            logger.warning("Vision: _set_color, unsupported color {0}".format(color))
            return False
        return self._send_sync_proto(proto)
