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


def sub_attitude_info_handler(attitude_info):
    yaw, pitch, roll = attitude_info
    print("chassis attitude: yaw:{0}, pitch:{1}, roll:{2} ".format(yaw, pitch, roll))


if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    ep_chassis = ep_robot.chassis

    # 订阅底盘姿态信息
    ep_chassis.sub_attitude(freq=10, callback=sub_attitude_info_handler)
    ep_chassis.move(x=0, y=0, z=90).wait_for_completed()
    ep_chassis.move(x=0, y=0, z=-90).wait_for_completed()
    ep_chassis.unsub_attitude()

    ep_robot.close()
