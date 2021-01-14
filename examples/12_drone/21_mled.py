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


if __name__ == '__main__':
    mled_smile1 = '000000000r0000r0r0r00r0r000000000000000000r00r00000rr00000000000'
    mled_smile2 = '00rrrr000r0000r0r0r00r0rr000000rr0r00r0rr00rr00r0r0000r000rrrr00'

    tl_drone = robot.Drone()
    tl_drone.initialize()

    # 显示自定义图案
    tl_drone.led.set_mled_graph(mled_smile1)
    time.sleep(3)
    tl_drone.led.set_mled_graph(mled_smile2)
    time.sleep(3)

    # 显示数字
    for num in range(10):
        tl_drone.led.set_mled_char('r', num)
        time.sleep(0.5)

    # 显示字符A, B, C
    tl_drone.led.set_mled_char(color='b', display_char='A')
    time.sleep(3)
    tl_drone.led.set_mled_char(color='b', display_char='B')
    time.sleep(3)
    tl_drone.led.set_mled_char(color='b', display_char='C')
    time.sleep(3)

    # 清屏
    tl_drone.led.set_mled_char('0')

    tl_drone.close()




