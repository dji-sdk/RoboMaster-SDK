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


import robomaster
from robomaster import robot
from robomaster import flight


if __name__ == '__main__':
    tl_drone = robot.Drone()
    tl_drone.initialize()

    tl_flight = tl_drone.flight

    # 起飞
    tl_flight.takeoff().wait_for_completed()

    # 曲线飞行
    tl_flight.curve(x1=60, y1=60, z1=0, x2=120, y2=0, z2=30, speed=30).wait_for_completed()
    tl_flight.curve(x1=-60, y1=60, z1=0, x2=-120, y2=0, z2=-30, speed=30).wait_for_completed()

    # 降落
    tl_flight.land().wait_for_completed()

    tl_drone.close()
