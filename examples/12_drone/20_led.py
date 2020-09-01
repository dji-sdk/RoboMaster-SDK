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
    tl_drone = robot.Drone()
    tl_drone.initialize()

    tl_led = tl_drone.led

    tl_led.set_led(r=0, g=0, b=0)

    rgb_list = [(100, 100, 100), (255, 255, 255), (255, 0, 0), (0, 0, 255),
                (0, 255, 0), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

    for rgb_info in rgb_list:
        tl_led.set_led(r=rgb_info[0], g=rgb_info[1], b=rgb_info[2])
        time.sleep(0.5)

    tl_drone.close()
