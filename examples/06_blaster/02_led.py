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


import time
import robomaster
from robomaster import robot
from robomaster import blaster


if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    ep_blaster = ep_robot.blaster

    # 设置发射器灯效为常亮，亮度递增
    ep_blaster.set_led(brightness=2, effect=blaster.LED_ON)
    time.sleep(1)
    ep_blaster.set_led(brightness=4, effect=blaster.LED_ON)
    time.sleep(1)
    ep_blaster.set_led(brightness=8, effect=blaster.LED_ON)
    time.sleep(1)
    ep_blaster.set_led(brightness=16, effect=blaster.LED_ON)
    time.sleep(1)
    ep_blaster.set_led(brightness=32, effect=blaster.LED_ON)
    time.sleep(1)
    ep_blaster.set_led(brightness=64, effect=blaster.LED_ON)
    time.sleep(1)
    ep_blaster.set_led(brightness=128, effect=blaster.LED_ON)
    time.sleep(1)
    ep_blaster.set_led(brightness=255, effect=blaster.LED_ON)
    time.sleep(1)

    # 设置发射器灯效为熄灭
    ep_blaster.set_led(brightness=0, effect=blaster.LED_OFF)

    ep_robot.close()



