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
from robomaster import led


if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    ep_led = ep_robot.led

    # 依次设置云台3颗 led 灯亮
    it = 0
    for i in range(0, 8):
        led1 = it % 8
        led2 = (it + 1) % 8
        led3 = (it + 2) % 8
        it += 1
        ep_led.set_gimbal_led(comp=led.COMP_TOP_ALL, r=255, g=25, b=25,
                              led_list=[led1, led2, led3], effect=led.EFFECT_ON)
        print("Gimbal Led: {0} {1} {2} is on!".format(led1, led2, led3))
        time.sleep(0.5)

    ep_robot.close()
