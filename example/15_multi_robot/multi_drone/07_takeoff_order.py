# -*-coding:utf-8-*-
# Copyright (c) 2020 DJI.
#
# Licensed under The 3-Clause BSD License (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the file LICENSE.txt or at
#
#     https://opensource.org/licenses/BSD-3-Clause
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from multi_robomaster import multi_robot
import time


def group_forward(robot_group):
    robot_group.forward(100).wait_for_completed()


def group_land(robot_group):
    robot_group.land().wait_for_completed()


if __name__ == '__main__':
    # get drone sn by run the expamles of /15_multi_robot/multi_drone/01_scan_ip.py

    robot_sn_list = ["0TQZH79ED00HA4", "0TQZH79ED00H5L"]
    multi_drone = multi_robot.MultiDrone()
    multi_drone.initialize(robot_num=2)
    multi_drone.number_id_by_sn([0, robot_sn_list[0]], [1, robot_sn_list[1]])
    multi_drone_group1 = multi_drone.build_group([0, 1])

    for drone_id in multi_drone_group1.robots_id_list:
        drone_obj = multi_drone_group1.get_robot(drone_id)
        drone_obj.takeoff().wait_for_completed()
        time.sleep(3)

    multi_drone.run([multi_drone_group1, group_land])
    multi_drone.close()
