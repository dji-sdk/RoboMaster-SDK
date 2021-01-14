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


def sub_tof_info_handler(tof_info):
    tof = tof_info
    print("drone tof: {0}".format(tof))


def sub_drone_info_handler(drone_info):
    high, baro, motor_time = drone_info
    print("drone info: high:{0}, baro:{1}, motor_time:{2}".format(high, baro, motor_time))


if __name__ == '__main__':
    tl_drone = robot.Drone()
    tl_drone.initialize()

    # 订阅TOF和飞行器信息
    tl_drone.sub_tof(freq=10, callback=sub_tof_info_handler)
    tl_drone.sub_drone_info(freq=1, callback=sub_drone_info_handler)

    tl_flight = tl_drone.flight
    tl_flight.takeoff().wait_for_completed()
    tl_flight.land().wait_for_completed()

    # 取消订阅信息
    tl_drone.unsub_tof()
    tl_drone.unsub_drone_info()

    tl_drone.close()

