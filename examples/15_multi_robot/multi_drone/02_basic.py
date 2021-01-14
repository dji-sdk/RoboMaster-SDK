# -*-coding:utf-8-*-
# Copyright (c) 2020 DJI, Inc.
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

from multi_robomaster import multi_robot


def basic_task(robot_group):
    robot_group.get_sn()
    robot_group.get_battery()


if __name__ == '__main__':
    # get drone sn by run the expamles of /15_multi_robot/multi_drone/01_scan_ip.py

    robot_sn_list = ["0TQZH79ED00H56", "0TQZH79ED00H89"]
    sn_list = []
    battery_list = []
    drone_num = 2
    multi_drone = multi_robot.MultiDrone()
    multi_drone.initialize(robot_num=2)
    multi_drone.number_id_by_sn([0, robot_sn_list[0]], [1, robot_sn_list[1]])
    tello_group = multi_drone.build_group([0, 1])
    multi_drone.run([tello_group, basic_task])
    multi_drone.close()

