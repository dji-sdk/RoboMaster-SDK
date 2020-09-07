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


__all__ = ['Blaster', 'WATER_FIRE', 'INFRARED_FIRE', 'LED_ON', 'LED_OFF']

WATER_FIRE = 'water'
INFRARED_FIRE = 'ir'

LED_ON = 'on'
LED_OFF = 'off'
LED_FLASH = 'flash'
LED_BREATH = 'breath'


class Blaster(module.Module):
    """ EP 发射器模块 """
    _host = protocol.host2byte(23, 0)

    def __init__(self, robot):
        super().__init__(robot)

    def fire(self, fire_type=WATER_FIRE, times=1):
        """ 发射器发射

        :param fire_type: enum: ("water", "ir")， 发射器发射类型，水弹、红外弹
        :param times: 发射次数
        :return: bool: 调用结果
        """
        proto = protocol.ProtoBlasterFire()
        if fire_type == WATER_FIRE:
            proto._type = 0
        elif fire_type == INFRARED_FIRE:
            proto._type = 1
        else:
            logger.warning("Blaster: fire, unsupported fire_type {0}".format(fire_type))
            return False
        proto._times = util.FIRE_TIMES_CHECKER.val2proto(times)
        return self._send_sync_proto(proto)

    def set_led(self, brightness=255, effect=LED_ON):
        """ 设置发射器灯效

        :param brightness: int:[0,255]，亮度
        :param effect: enum:("on", "off")，on 表示常亮，off 表示常灭
        :return: bool:调用结果
        """

        proto = protocol.ProtoBlasterSetLed()
        proto._g = util.COLOR_VALUE_CHECKER.check(brightness)
        proto._r = util.COLOR_VALUE_CHECKER.check(brightness)
        proto._b = util.COLOR_VALUE_CHECKER.check(brightness)
        if effect is LED_OFF:
            proto._effect = 0
        elif effect is LED_ON:
            proto._effect = 1
        else:
            logger.warning("Blaster: set_led, unsupported effect value {0}".format(effect))
            return False

        return self._send_sync_proto(proto)
