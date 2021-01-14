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
from robomaster import flight


if __name__ == '__main__':
    tl_drone = robot.Drone()
    tl_drone.initialize()

    tl_flight = tl_drone.flight

    # 打开挑战卡检测
    tl_flight.mission_pad_on()

    # 起飞
    tl_flight.takeoff().wait_for_completed()

    # 飞行到挑战卡上方
    tl_flight.go(x=0, y=0, z=100, speed=30, mid="m1").wait_for_completed()

    # 挑战卡上曲线飞行
    tl_flight.curve(x1=50, y1=50, z1=100, x2=100, y2=0, z2=100, speed=30, mid="m1").wait_for_completed()

    # 降落
    tl_flight.land().wait_for_completed()

    # 关闭挑战卡检测
    tl_flight.mission_pad_off()

    tl_drone.close()
