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


from multi_robomaster import multi_robot


def takeoff_land_task1(robot_group):
    robot_group.takeoff().wait_for_completed()
    robot_group.forward(100).wait_for_completed()
    robot_group.land().wait_for_completed()


def takeoff_land_task2(robot_group):
    robot_group.takeoff().wait_for_completed()
    robot_group.backward(100).wait_for_completed()
    robot_group.land().wait_for_completed()


if __name__ == '__main__':
    # get drone sn by run the expamles of /15_multi_robot/multi_drone/01_scan_ip.py

    robot_sn_list = ["0TQZH79ED00H56", "0TQZH79ED00H89"]
    multi_drone = multi_robot.MultiDrone()
    multi_drone.initialize(robot_num=2)
    multi_drone.number_id_by_sn([0, robot_sn_list[0]], [1, robot_sn_list[1]])
    multi_drone_group1 = multi_drone.build_group([0])
    multi_drone_group2 = multi_drone.build_group([1])
    multi_drone.run([multi_drone_group1, takeoff_land_task1],
                    [multi_drone_group2, takeoff_land_task2])
    multi_drone.close()



