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


def sub_status_info_handler(status_info):
    static_flag, up_hill, down_hill, on_slope, pick_up, slip_flag, impact_x, impact_y, impact_z, \
    roll_over, hill_static = status_info
    print("chassis status: static_flag:{0}, up_hill:{1}, down_hill:{2}, on_slope:{3}, "
          "pick_up:{4}, impact_x:{5}, impact_y:{6}, impact_z:{7}, roll_over:{8}, "
          "hill_static:{9}".format(static_flag, up_hill, down_hill, on_slope, pick_up,
                                   slip_flag, impact_x, impact_y, impact_z, roll_over, hill_static))


if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    ep_chassis = ep_robot.chassis

    # 订阅底盘状态信息：
    ep_chassis.sub_status(freq=5, callback=sub_status_info_handler)
    time.sleep(3)
    ep_chassis.unsub_status()

    ep_robot.close()
