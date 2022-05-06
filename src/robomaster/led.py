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
from . import util


__all__ = ['Led', 'COMP_TOP_LEFT', 'COMP_TOP_RIGHT', 'COMP_BOTTOM_LEFT', 'COMP_BOTTOM_RIGHT',
           'COMP_BOTTOM_FRONT', 'COMP_BOTTOM_BACK', 'COMP_BOTTOM_ALL', 'COMP_TOP_ALL', 'COMP_ALL',
           'EFFECT_ON', 'EFFECT_OFF', 'EFFECT_PULSE', 'EFFECT_FLASH', 'EFFECT_BREATH',
           'EFFECT_SCROLLING']

COMP_TOP_LEFT = 'top_left'
COMP_TOP_RIGHT = 'top_right'
COMP_BOTTOM_LEFT = 'bottom_left'
COMP_BOTTOM_RIGHT = 'bottom_right'
COMP_BOTTOM_FRONT = 'bottom_front'
COMP_BOTTOM_BACK = 'bottom_back'
COMP_BOTTOM_ALL = 'bottom_all'
COMP_TOP_ALL = 'top_all'
COMP_ALL = 'all'

_VALID_COMP = [COMP_TOP_LEFT, COMP_TOP_RIGHT, COMP_BOTTOM_LEFT, COMP_BOTTOM_RIGHT, COMP_BOTTOM_FRONT,
               COMP_BOTTOM_BACK, COMP_BOTTOM_ALL, COMP_TOP_ALL, COMP_ALL]

EFFECT_ON = 'on'
EFFECT_OFF = 'off'
EFFECT_PULSE = 'pulse'
EFFECT_FLASH = 'flash'
EFFECT_BREATH = 'breath'
EFFECT_SCROLLING = 'scrolling'

TELLO_DISPLAY_GRAPH = '00rrrr000r0000r0r0r00r0rr000000rr0r00r0rr00rr00r0r0000r000rrrr00'

ARMOR_BOTTOM_BACK = 0x1
ARMOR_BOTTOM_FRONT = 0x2
ARMOR_BOTTOM_LEFT = 0x4
ARMOR_BOTTOM_RIGHT = 0x8
ARMOR_TOP_LEFT = 0x10
ARMOR_TOP_RIGHT = 0x20
ARMOR_TOP_ALL = 0x30
ARMOR_BOTTOM_ALL = 0xf
ARMOR_ALL = 0x3f


class Led(module.Module):
    """ EP 装甲灯模块 """

    _host = protocol.host2byte(24, 0)

    def __init__(self, robot):
        super().__init__(robot)

    def set_led(self, comp=COMP_ALL, r=0, g=0, b=0, effect=EFFECT_ON, freq=1):
        """ 设置整机装甲灯效

        :param comp: enum: ("all", "top_all", "top_right", "top_left", "bottom_all", "bottom_front", \
        "bottom_back", "bottom_left", "bottom_right") 灯效部位，all: 所有装甲灯；top_all:云台所有装甲灯；\
        top_right: 云台右侧装甲灯；top_left: 云台左侧装甲灯; bottom_all: 底盘所有装甲灯；bottom_front: 前装甲灯；\
        bottom_back: 后装甲灯；bottom_left: 左装甲灯；bottom_right: 右装甲灯
        :param r: int: [0~255]，RGB红色分量值
        :param g: int: [0~255]，RGB绿色分量值
        :param b: int: [0~255]，RGB蓝色分量值
        :param effect: enum: ("on", "off", "flash", "breath", "scrolling") 灯效类型，on:常亮；off:常灭；flash:闪烁；\
        breath:呼吸；scrolling:跑马灯（仅对云台灯有效）
        :param freq: int: [1, 10]，闪烁频率，仅对闪烁灯效有效
        :return: bool:调用结果
        """
        comp_mask = 0x0
        if comp == COMP_ALL:
            comp_mask = ARMOR_ALL
        elif comp == COMP_TOP_ALL:
            comp_mask = ARMOR_TOP_ALL
        elif comp == COMP_TOP_LEFT:
            comp_mask = ARMOR_TOP_LEFT
        elif comp == COMP_TOP_RIGHT:
            comp_mask = ARMOR_TOP_RIGHT
        elif comp == COMP_BOTTOM_ALL:
            comp_mask = ARMOR_BOTTOM_ALL
        elif comp == COMP_BOTTOM_BACK:
            comp_mask = ARMOR_BOTTOM_BACK
        elif comp == COMP_BOTTOM_LEFT:
            comp_mask = ARMOR_BOTTOM_LEFT
        elif comp == COMP_BOTTOM_FRONT:
            comp_mask = ARMOR_BOTTOM_FRONT
        elif comp == COMP_BOTTOM_RIGHT:
            comp_mask = ARMOR_BOTTOM_RIGHT
        else:
            logger.warning("Led: set_led, not support comp:{0}".format(comp))
            return False

        proto = protocol.ProtoSetSystemLed()
        proto._ctrl_mode = 7
        proto._comp_mask = comp_mask
        proto._r = util.COLOR_VALUE_CHECKER.val2proto(r)
        proto._g = util.COLOR_VALUE_CHECKER.val2proto(g)
        proto._b = util.COLOR_VALUE_CHECKER.val2proto(b)
        if effect is EFFECT_OFF:
            proto._effect_mode = 0
        elif effect is EFFECT_ON:
            proto._effect_mode = 1
        elif effect is EFFECT_BREATH:
            proto._effect_mode = 2
            proto._t1 = 1000
            proto._t2 = 1000
        elif effect is EFFECT_FLASH:
            proto._effect_mode = 3
            if freq == 0:
                logger.warning("Led: set_led: freq is zero.")
                freq = 1
            t = int(500/freq)
            proto._t1 = t
            proto._t2 = t
        elif effect is EFFECT_SCROLLING:
            proto._effect_mode = 4
            proto._t1 = 30
            proto._t2 = 40
            proto._led_mask = 0x0f
        else:
            logger.warning("Led: set_led, unsupported effect {0}".format(effect))

        return self._send_sync_proto(proto, protocol.host2byte(9, 0))

    def set_gimbal_led(self, comp=COMP_TOP_ALL, r=255, g=255, b=255, led_list=[0, 1, 2, 3], effect=EFFECT_ON):
        """ 设置云台灯效

        :param comp: enum: ("top_all", "top_left", "top_right")，云台部位
        :param r: int: [0, 255]，RGB红色分量值
        :param g: int: [0, 255]，RGB绿色分量值
        :param b: int: [0, 255]，RGB蓝色分量值
        :param led_list: list [idx0, idx1, ...]，idx：int[0,7] 云台灯序号列表.
        :param effect: enum: ("on", "off")，灯效类型
        :return: bool: 调用结果
        """
        comp_mask = 0x0
        if comp == COMP_ALL:
            comp_mask = ARMOR_ALL
        elif comp == COMP_TOP_ALL:
            comp_mask = ARMOR_TOP_ALL
        elif comp == COMP_TOP_LEFT:
            comp_mask = ARMOR_TOP_LEFT
        elif comp == COMP_TOP_RIGHT:
            comp_mask = ARMOR_TOP_RIGHT
        else:
            logger.warning("Led: set_gimbal_led, not support comp:{0}".format(comp))
            return False

        proto = protocol.ProtoSetSystemLed()
        proto._ctrl_mode = 7
        proto._comp_mask = comp_mask
        proto._led_mask = 0
        for i in range(0, len(led_list)):
            proto._led_mask += 1 << (led_list[i] % 8)
        proto._r = util.COLOR_VALUE_CHECKER.val2proto(r)
        proto._g = util.COLOR_VALUE_CHECKER.val2proto(g)
        proto._b = util.COLOR_VALUE_CHECKER.val2proto(b)
        if effect is EFFECT_OFF:
            proto._effect_mode = 0
        elif effect is EFFECT_ON:
            proto._effect_mode = 1
        else:
            logger.warning("Led: set_gimbal_led, unsupported effect {0}".format(effect))

        return self._send_sync_proto(proto, protocol.host2byte(9, 0))


class TelloLed(object):
    """ 教育无人机 扩展LED模块 """

    def __init__(self, robot):
        self._robot = robot
        self._client = robot.client

    def set_led(self, r=0, g=255, b=0):
        """ 设置扩展模块led颜色

        :param r: int:[0, 255], 扩展led红色通道的强度
        :param g: int:[0, 255], 扩展led绿色通道的强度
        :param b: int:[0, 255], 扩展led蓝色通道的强度
        :return: bool: 扩展led模块控制结果
        """
        cmd = "EXT led {0} {1} {2}".format(r, g, b)
        proto = protocol.TextProtoDrone()
        proto.text_cmd = cmd
        msg = protocol.TextMsg(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                if proto:
                    if proto.resp == "led ok":
                        return True
                    else:
                        logger.warning("Drone: set ext led failed, resp {0}".format(proto.resp))
            logger.error("Drone: set ext led failed")
            return False
        except Exception as e:
            logger.error("Drone: set ext led, send_sync_msg exception {0}".format(str(e)))
            return False

    def set_led_breath(self, freq=1, r=0, g=255, b=0):
        """ 设置扩展模块led以指定的颜色与频率实现呼吸效果

        :param freq: int:[0.1, 2.5], 扩展led呼吸模式下的频率，共十档，随着数字增大速度变快
        :param r: int:[0, 255], 扩展led红色通道的强度
        :param g: int:[0, 255], 扩展led绿色通道的强度
        :param b: int:[0, 255], 扩展led蓝色通道的强度
        :return: bool: 扩展led模块控制结果
        """
        cmd = "EXT led br {0} {1} {2} {3}".format(freq, r, g, b)
        proto = protocol.TextProtoDrone()
        proto.text_cmd = cmd
        msg = protocol.TextMsg(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                if proto:
                    if proto.resp == "led ok":
                        return True
                    else:
                        logger.warning("Drone: set ext led breath failed, resp {0}".format(proto.resp))
            logger.error("Drone: set ext led breath failed")
            return False
        except Exception as e:
            logger.error("Drone: set ext led breath, send_sync_msg exception {0}".format(str(e)))
            return False

    def set_led_blink(self, freq=5, r1=0, g1=255, b1=0, r2=0, g2=255, b2=255):
        """ 设置扩展模块led以制定的两种颜色与频率实现闪烁效果

        :param freq: int:[0.1, 10], 扩展ked闪烁模式下的频率， 共十档，随着数字增大速度变快
        :param r1: int:[0, 255], 第一种颜色的红色通道的强度
        :param g1: int:[0, 255], 第一种颜色的绿色通道的强度
        :param b1: int:[0, 255], 第一种颜色的蓝色通道的强度
        :param r2: int:[0, 255], 第二种颜色的红色通道的强度
        :param g2: int:[0, 255], 第二种颜色的绿色通道的强度
        :param b2: int:[0, 255], 第二种颜色的蓝色通道的强度
        :return: bool: 扩展led模块控制结果
        """
        cmd = "EXT led bl {0} {1} {2} {3} {4} {5} {6}".format(freq, r1, g1, b1, r2, g2, b2)
        proto = protocol.TextProtoDrone()
        proto.text_cmd = cmd
        msg = protocol.TextMsg(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                if proto:
                    if proto.resp == "led ok":
                        return True
                    else:
                        logger.warning("Drone: set ext led blink failed, resp {0}".format(proto.resp))
            logger.error("Drone: set ext led blink failed")
            return False
        except Exception as e:
            logger.error("Drone: set ext led blink, send_sync_msg exception {0}".format(str(e)))
            return False

    def set_mled_bright(self, bright=255):
        """ 设置点阵屏的亮度

        :param bright: int:[0, 255] 点阵屏的亮度
        :return: bool: 点阵屏亮度的设置结果
        """
        cmd = "EXT mled sl {0}".format(bright)
        proto = protocol.TextProtoDrone()
        proto.text_cmd = cmd
        msg = protocol.TextMsg(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                if proto:
                    if proto.resp == "matrix ok":
                        return True
                    else:
                        logger.warning("Drone: set ext mled bright failed, resp {0}".format(proto.resp))
            logger.error("Drone: set ext mled bright failed")
            return False
        except Exception as e:
            logger.error("Drone: set ext mled bright, send_sync_msg exception {0}".format(str(e)))
            return False

    def set_mled_boot(self, display_graph):
        """ 设置点阵屏的开机画面

        :param display_graph: string: 长度最大为64，点阵屏显示图案的编码字符串，每个字符解读为二进制后对应位置的led点的状态，
        '0'为关闭该位置led，'r'为点亮红色，'b'为点亮蓝色，'p' 为点亮紫色，输入的长度不足64，后面对应的led点默认都是'0'熄灭状态
        :return: bool: 设置开机动画的结果
        """
        cmd = "EXT mled sg {0}".format(display_graph)
        proto = protocol.TextProtoDrone()
        proto.text_cmd = cmd
        msg = protocol.TextMsg(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                if proto:
                    if proto.resp == "matrix ok":
                        return True
                    else:
                        logger.warning("Drone: set ext mled boot display failed, resp {0}".format(proto.resp))
            logger.error("Drone: set ext mled boot display failed")
            return False
        except Exception as e:
            logger.error("Drone: set ext mled boot display, send_sync_msg exception {0}".format(str(e)))
            return False

    def set_mled_sc(self):
        """ 清除点阵屏开机显示画面

        :return: bool: 清除点阵屏机显示画面的结果
        """
        cmd = "EXT mled sc"
        proto = protocol.TextProtoDrone()
        proto.text_cmd = cmd
        msg = protocol.TextMsg(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                if proto:
                    if proto.resp == "matrix ok":
                        return True
                    else:
                        logger.warning("Drone: set ext mled display clear failed, resp {0}".format(proto.resp))
            logger.error("Drone: set ext mled display clear failed")
            return False
        except Exception as e:
            logger.error("Drone: set ext mled display clear, send_sync_msg exception {0}".format(str(e)))
            return False

    def set_mled_char(self, color="r", display_char="0"):
        """ 控制扩展点阵屏模块，显示输入的字符

        :param: color: char: 'r'为红色，'b'为蓝色，'p' 为紫色
        :param: display_char: char: [0~9, A~F, heart]， 显示的字符
        :return: bool: 控制结果
        """
        cmd = "EXT mled s {0} {1}".format(color, display_char)
        proto = protocol.TextProtoDrone()
        proto.text_cmd = cmd
        msg = protocol.TextMsg(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                if proto:
                    if proto.resp == "matrix ok":
                        return True
                    else:
                        logger.warning("Drone: set ext mled char resp {0}".format(proto.resp))
            logger.error("Drone: set mled char resp failed.")
            return False
        except Exception as e:
            logger.warning("Drone: set ext mled char, send_sync_msg exception {0}".format(str(e)))
            return False

    def set_mled_graph(self, display_graph):
        """ 用户自定义扩展点阵屏显示图案

        :param display_graph: string: 长度最大为64，点阵屏显示图案的编码字符串，每个字符解读为二进制后对应位置的led点的状态，
        '0'为关闭该位置led，'r'为点亮红色，'b'为点亮蓝色，'p' 为点亮紫色，输入的长度不足64，后面对应的led点默认都是'0'熄灭状态
        :return:bool: 控制结果
        """
        cmd = "EXT mled g {0}".format(display_graph)
        proto = protocol.TextProtoDrone()
        proto.text_cmd = cmd
        msg = protocol.TextMsg(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                if proto:
                    if proto.resp == "matrix ok":
                        return True
                    else:
                        logger.warning("Drone: set ext mled custom failed, resp {0}".format(proto.resp))
            logger.warning("Drone: set mled resp custom failed.")
            return False
        except Exception as e:
            logger.warning("Drone: set ext mled custom , send_sync_msg exception {0}".format(str(e)))
            return False

    def set_mled_char_scroll(self, direction='l', color='r', freq=1.5, display_str="DJI"):
        """ 控制扩展点阵屏滚动显示字符串

        :param: direction: char: 点阵屏滚动方向，'l': 字符串向左移动，'r': 字符串向右移动，'u' 字符串向上移动，'d' 字符串向下移动
        :param: color: char: 点阵屏显示的颜色， 'r'红色，'b'蓝色，'p'紫色
        :param: freq: float:[0.1, 2.5], 点阵屏滚动的频率, 0.1-2.5HZ之间, 随着数字增大速度变快
        :param: display_str: string:需要显示的字符串
        :return: 设置结果
        """
        cmd = "EXT mled {0} {1} {2} {3} ".format(direction, color, freq, display_str)
        return self._set_mled_scroll(cmd)

    def set_mled_graph_scroll(self, direction='l', freq=1.5, display_graph=TELLO_DISPLAY_GRAPH):
        """ 控制扩展点阵屏滚动显示图像

        :param: direction: char: 点阵屏滚动方向，'l': 字符串向左移动，'r': 字符串向右移动，'u' 字符串向上移动，'d' 字符串向下移动
        :param: freq: float:[0.1, 2.5], 点阵屏滚动的频率, 0.1-2.5HZ之间, 随着数字增大速度变快
        :param: display_str: string:需要显示的图像
        :return: 设置结果
        """
        cmd = "EXT mled {0} {1} {2} {3} ".format(direction, "g", freq, display_graph)
        return self._set_mled_scroll(cmd)

    def _set_mled_scroll(self, cmd):
        """ 控制扩展点阵屏滚动显示

        :return: 设置结果
        """
        proto = protocol.TextProtoDrone()
        proto.text_cmd = cmd
        msg = protocol.TextMsg(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                if proto:
                    if proto.resp == "matrix ok":
                        return True
                    else:
                        logger.warning("Drone: set ext mled scroll failed, resp {0}".format(proto.resp))
            logger.error("Drone: set mled scroll resp failed.")
            return False
        except Exception as e:
            logger.warning("Drone: set ext mled scroll, send_sync_msg exception {0}".format(str(e)))
            return False
