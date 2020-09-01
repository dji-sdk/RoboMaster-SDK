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
    sn_info_dict = robot_group.get_sn()
    battery_info_dict = robot_group.battery.get_battery()
    print("Example: sn {0}, soc {1}".format(sn_info_dict, battery_info_dict))


if __name__ == '__main__':
    tello_ip_list = ['0TQZH79ED00H96', '0TQZH79ED00H5U']
    sn_list = []
    battery_list = []
    drone_num = 2
    multi_drone = multi_robot.MultiDrone()
    multi_drone.initialize(2)
    multi_drone.number_id_by_sn([0, tello_ip_list[0]], [1, tello_ip_list[1]])
    tello_group = multi_drone.build_group([0, 1])
    multi_drone.run([tello_group, basic_task])
    multi_drone.close()

