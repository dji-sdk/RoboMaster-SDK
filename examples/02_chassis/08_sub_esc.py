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


def sub_esc_info_handler(esc_info):
    speed, angle, timestamp, state = esc_info
    print("chassis esc: speed:{0}, angle:{1}, timestamp:{2}, state:{3}".format(speed, angle, timestamp, state))


if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    ep_chassis = ep_robot.chassis

    # 订阅底盘电调信息
    ep_chassis.sub_esc(freq=5, callback=sub_esc_info_handler)
    ep_chassis.move(x=1, y=0, z=0, xy_speed=1.0).wait_for_completed()
    ep_chassis.move(x=-1, y=0, z=0, xy_speed=1.0).wait_for_completed()
    ep_chassis.unsub_esc()

    ep_robot.close()
