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
from robomaster import robot
from robomaster import led


if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    ep_led = ep_robot.led

    # 设置灯效为常亮，亮度递增
    bright = 1
    for i in range(0, 8):
        ep_led.set_led(comp=led.COMP_ALL, r=bright << i, g=bright << i, b=bright << i, effect=led.EFFECT_ON)
        time.sleep(1)
        print("brightness: {0}".format(bright << i))

    ep_robot.close()

