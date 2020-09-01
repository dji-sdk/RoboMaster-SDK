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


def takeoff_land_task1(robot_group):
    robot_group.flight.takeoff().wait_for_completed()
    robot_group.flight.forward(100).wait_for_completed()
    robot_group.flight.land().wait_for_completed()


def takeoff_land_task2(robot_group):
    robot_group.flight.takeoff().wait_for_completed()
    robot_group.flight.backward(100).wait_for_completed()
    robot_group.flight.land().wait_for_completed()


if __name__ == '__main__':
    #get drone sn by run the expamles of /15_multi_robot/multi_drone/02_basic.py
    robot_sn_list = ['0TQZH79ED00H96', '0TQZH79ED00H5U']
    multi_drone = multi_robot.MultiDrone()
    multi_drone.initialize(2)
    multi_drone.number_id_by_sn([0, robot_sn_list[0]], [1, robot_sn_list[1]])
    multi_drone_group1 = multi_drone.build_group([0])
    multi_drone_group2 = multi_drone.build_group([1])
    multi_drone.run([multi_drone_group1, takeoff_land_task1],
                    [multi_drone_group2, takeoff_land_task2])
    multi_drone.close()



