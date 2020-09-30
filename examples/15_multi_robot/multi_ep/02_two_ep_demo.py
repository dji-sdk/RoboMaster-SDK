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

def group_task(robot_group):
    x = 0.3
    y = 0.3
    z = 90

    # 前进 0.3米
    robot_group.chassis.move(-x, 0, 0, 2, 180).wait_for_completed()

    # 后退 0.3米
    robot_group.chassis.move(x, 0, 0, 2, 180).wait_for_completed()

    # 左移 0.3米
    robot_group.chassis.move(0, -y, 0, 2, 180).wait_for_completed()

    # 右移 0.3米
    robot_group.chassis.move(0, y, 0, 2, 180).wait_for_completed()

    # 左转 90度
    robot_group.chassis.move(0, 0, z, 2, 180).wait_for_completed()

    # 右转 90度
    robot_group.chassis.move(0, 0, -z, 2, 180).wait_for_completed()


def group_task1(robot_group):

    # 前进 0.3米
    robot_group.chassis.move(0.3, 0, 0, 2, 180).wait_for_completed()


if __name__ == '__main__':
    #get robot sn by run the exmaples of /15_multi_robot/multi_ep/01_scan_robot_sn.py
    robots_sn_list = ['3JKDH2T001KMP2', '3JKDH2T0013ELK']
    multi_robots = multi_robot.MultiEP()
    multi_robots.initialize()
    number = multi_robots.number_id_by_sn([0, robots_sn_list[0]], [1, robots_sn_list[1]])
    print("The number of robot is: {0}".format(number))
    robot_group = multi_robots.build_group([0, 1])
    robot_group1 = multi_robots.build_group([0])
    multi_robots.run([robot_group, group_task])
    multi_robots.run([robot_group1, group_task1])
    print("Game over")
    multi_robots.close()


