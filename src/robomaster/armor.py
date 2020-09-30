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


__all__ = ['Armor']

HIT_TYPE_WATER_ATTACK = 0
HIT_TYPE_IR_ATTACK = 1

COMP_TOP_LEFT = 'top_left'
COMP_TOP_RIGHT = 'top_right'
COMP_BOTTOM_LEFT = 'bottom_left'
COMP_BOTTOM_RIGHT = 'bottom_right'
COMP_BOTTOM_FRONT = 'bottom_front'
COMP_BOTTOM_BACK = 'bottom_back'
COMP_BOTTOM_ALL = 'bottom_all'
COMP_TOP_ALL = 'top_all'
COMP_ALL = 'all'


COMP_TOP_LEFT_MASK = 1 << 5
COMP_TOP_RIGHT_MASK = 1 << 4
COMP_BOTTOM_LEFT_MASK = 1 << 3
COMP_BOTTOM_RIGHT_MASK = 1 << 2
COMP_BOTTOM_FRONT_MASK = 1 << 1
COMP_BOTTOM_BACK_MASK = 1 << 0
COMP_BOTTOM_ALL_MASK = 0x0f
COMP_TOP_ALL_MASK = 0x30
COMP_ALL_MASK = 0x3f


class ArmorHitEvent(dds.Subject):
    name = "hit_event"
    cmdset = 0x3f
    cmdid = 0x02
    type = dds.DDS_SUB_TYPE_EVENT

    def __init__(self):
        self._armor_id = 0
        self._type = 0
        self._mic_value = 0
        self._mic_len = 0

    @property
    def armor_id(self):
        """ 上一次被击打的装甲板ID """
        return self._armor_id

    def armor_comp(self):
        """ 上一次被击打的装甲板部位 """
        return Armor.id2comp(self._armor_id)

    @property
    def hit_type(self):
        """ 被击打类型
        :return: enum: ("water", "ir"): water:水弹，ir:红外
        """
        if self._type == HIT_TYPE_IR_ATTACK:
            return "ir"
        elif self._type == HIT_TYPE_WATER_ATTACK:
            return "water"
        else:
            logger.warning("ArmorHitEvent: unsupported hit type:{0}".format(self._type))
            return ""

    @property
    def strength(self):
        return self._mic_value

    def data_info(self):
        return self.armor_id, self.hit_type

    def decode(self, buf):
        self._armor_id, self._type, self._mic_value = buf


class IrHitEvent(dds.Subject):
    name = "ir_event"
    cmdset = 0x3f
    cmdid = 0x10
    type = dds.DDS_SUB_TYPE_EVENT

    def __init__(self):
        self._skill_id = 0
        self._role_id = 0
        self._recv_dev = 0
        self._recv_ir_pin = 0
        self._hit_cnt = 0

    @property
    def hit_times(self):
        """ 受到红外打击的次数 """
        return self._hit_cnt

    def data_info(self):
        return self._hit_cnt

    def decode(self, buf):
        self._hit_cnt = self._hit_cnt + 1
        self._skill_id, self._role_id, self._recv_dev, self._recv_ir_pin = buf


class Armor(module.Module):
    _host = protocol.host2byte(24, 1)

    def __init__(self, robot):
        super().__init__(robot)

    def sub_hit_event(self, callback=None, *args, **kw):
        """ 打击事件订阅

        :param callback: 回调函数, 返回数据 (armor_id, hit_type)：

                :param armor_id: int:[1, 6]打击装甲的编号，1 底盘后；2 底盘前；3 底盘左；4 底盘右；5 云台左；6 云台右
                :param hit_type: enum:("water", "ir")，被打击类型，water:水弹，ir:红外

        :param args: 可变参数
        :param kw: 关键字参数
        :return: bool: 事件订阅结果
        """
        sub = self._robot.dds
        subject = ArmorHitEvent()
        protocol.ProtoArmorHitEvent()
        return sub.add_subject_event_info(subject, callback, args, kw)

    def sub_ir_event(self, callback=None, *args, **kw):
        """ 红外打击事件订阅

        :param callback: 回调函数, 返回数据 (hit_cnt)
        :param hit_cnt: 受到红外击打的次数

        :param args: 可变参数
        :param kw: 关键字参数
        :return: bool: 事件订阅结果
        """
        sub = self._robot.dds
        subject = IrHitEvent()
        protocol.ProtoIrHitEvent()
        return sub.add_subject_event_info(subject, callback, args, kw)

    def unsub_hit_event(self):
        """ 取消打击事件订阅

        :return: bool: 取消事件订阅结果
        """
        sub = self._robot.dds
        subject = ArmorHitEvent()
        return sub.del_subject_event_info(subject)

    def unsub_ir_event(self):
        """ 取消红外打击事件订阅

        :return: bool: 取消事件订阅结果
        """
        sub = self._robot.dds
        subject = IrHitEvent()
        return sub.del_subject_event_info(subject)

    def set_hit_sensitivity(self, comp=COMP_ALL, sensitivity=5):
        """ 设置装甲灵敏度

        :param comp: enum:("all", "top_all", "bottom_all", "top_left", "top_right", "bottom_left", \
        "bottom_right", "bottom_front", "bottom_back")：要设置的装甲部位
        :param sensitivity: int:[0, 10] 灵敏度系数，系数越大灵敏度越低
        :return: bool:返回调用结果
        """
        k = 1.5 - sensitivity / 10.0
        proto = protocol.ProtoSetArmorParam()
        proto._armor_mask = self._comp2mask(comp) & 0x3f
        proto._voice_energy_en = 500
        proto._voice_energy_ex = 300
        proto._voice_len_max = 50
        proto._voice_len_min = 13
        proto._voice_len_silence = 6
        proto._voice_peak_count = 1
        proto._voice_peak_min = int(160 * k)
        proto._voice_peak_ave = int(180 * k)
        proto._voice_peak_final = int(200 * k)
        logger.info("Armor: set_hit_sensitivity, armor_comp:{0}, sensitivity:{1}".format(comp, sensitivity))
        return self._send_sync_proto(proto)

    @staticmethod
    def comp2id(comp):
        """ 装甲部位转换为装甲ID

        :param comp: enum ("bottom_back", "bottom_front", "bottom_left", "bottom_right", "top_left", "top_right") 装甲部位
        :return: int: [1, 6] 装甲ID
        """
        if comp == COMP_BOTTOM_BACK:
            return 1
        elif comp == COMP_BOTTOM_FRONT:
            return 2
        elif comp == COMP_BOTTOM_LEFT:
            return 3
        elif comp == COMP_BOTTOM_RIGHT:
            return 4
        elif comp == COMP_TOP_LEFT:
            return 5
        elif comp == COMP_TOP_RIGHT:
            return 6
        else:
            logger.warning("Armor: comp2id, unsupported comp:{0}".format(comp))
            return 0

    @staticmethod
    def id2comp(armor_id):
        """ 装甲ID转换为装甲部位

        :param armor_id: int [1, 6]，装甲ID
        :return comp: enum: ("bottom_back", "bottom_front", "bottom_left", "bottom_right", "top_left", "top_right")，\
        装甲部位
        """
        if armor_id == 1:
            return COMP_BOTTOM_BACK
        elif armor_id == 2:
            return COMP_BOTTOM_FRONT
        elif armor_id == 3:
            return COMP_BOTTOM_LEFT
        elif armor_id == 4:
            return COMP_BOTTOM_RIGHT
        elif armor_id == 5:
            return COMP_TOP_LEFT
        elif armor_id == 6:
            return COMP_TOP_RIGHT
        else:
            logger.warning("Armor: id2comp, unsupported id:{0}".format(armor_id))
            return ""

    @staticmethod
    def _mask2comp(comp_mask):
        comp = ""
        if comp_mask == COMP_ALL_MASK:
            comp = COMP_ALL
        elif comp_mask == COMP_TOP_ALL_MASK:
            comp = COMP_TOP_ALL
        elif comp_mask == COMP_BOTTOM_ALL_MASK:
            comp = COMP_BOTTOM_ALL
        elif comp_mask == COMP_TOP_LEFT_MASK:
            comp = COMP_TOP_LEFT
        elif comp_mask == COMP_TOP_RIGHT_MASK:
            comp = COMP_TOP_RIGHT
        elif comp_mask == COMP_BOTTOM_BACK_MASK:
            comp = COMP_BOTTOM_BACK
        elif comp_mask == COMP_BOTTOM_FRONT_MASK:
            comp = COMP_BOTTOM_FRONT
        elif comp_mask == COMP_BOTTOM_LEFT_MASK:
            comp = COMP_BOTTOM_LEFT
        elif comp_mask == COMP_BOTTOM_RIGHT_MASK:
            comp = COMP_BOTTOM_RIGHT
        else:
            logger.warning("Armor: mask2comp, unsupported comp_mask:{0}".format(comp_mask))
        return comp

    @staticmethod
    def _comp2mask(comp):
        comp_mask = 0
        if comp == COMP_ALL:
            comp_mask = COMP_ALL_MASK
        elif comp == COMP_TOP_ALL:
            comp_mask = COMP_TOP_ALL_MASK
        elif comp == COMP_TOP_LEFT:
            comp_mask = COMP_TOP_LEFT_MASK
        elif comp == COMP_TOP_RIGHT:
            comp_mask = COMP_TOP_RIGHT_MASK
        elif comp == COMP_BOTTOM_ALL:
            comp_mask = COMP_BOTTOM_ALL_MASK
        elif comp == COMP_BOTTOM_BACK:
            comp_mask = COMP_BOTTOM_BACK_MASK
        elif comp == COMP_BOTTOM_FRONT:
            comp_mask = COMP_BOTTOM_FRONT_MASK
        elif comp == COMP_BOTTOM_LEFT:
            comp_mask = COMP_BOTTOM_LEFT_MASK
        elif comp == COMP_BOTTOM_RIGHT:
            comp_mask = COMP_BOTTOM_RIGHT_MASK
        else:
            logger.warning("Armor: comp2mask, unsupported comp:{0}".format(comp))
        return comp_mask
