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


if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    ep_gimbal = ep_robot.gimbal

    pitch_val = 15
    yaw_val = 30

    # 云台旋转到 pitch=0, yaw=0 位置
    ep_gimbal.moveto(pitch=0, yaw=0).wait_for_completed()

    # 云台以pitch角速度 50度每秒，yaw角速度100度每秒 旋转到pitch=15, yaw=90
    ep_gimbal.moveto(pitch=15, yaw=90, pitch_speed=50, yaw_speed=100).wait_for_completed()

    # 云台以pitch角速度 100度每秒，yaw角速度30度每秒 旋转到pitch=-15, yaw=-90
    ep_gimbal.moveto(pitch=-15, yaw=-90, pitch_speed=100, yaw_speed=30).wait_for_completed()

    # 云台旋转到 pitch=0, yaw=0 位置
    ep_gimbal.moveto(pitch=0, yaw=0).wait_for_completed()

    # 云台向左旋转30度*3次
    ep_gimbal.move(pitch=0, yaw=yaw_val).wait_for_completed()
    ep_gimbal.move(pitch=0, yaw=yaw_val).wait_for_completed()
    ep_gimbal.move(pitch=0, yaw=yaw_val).wait_for_completed()

    # 云台向右旋转30度*3次
    ep_gimbal.move(pitch=0, yaw=-yaw_val).wait_for_completed()
    ep_gimbal.move(pitch=0, yaw=-yaw_val).wait_for_completed()
    ep_gimbal.move(pitch=0, yaw=-yaw_val).wait_for_completed()

    # 云台向上旋转20度
    ep_gimbal.move(pitch=pitch_val, yaw=0).wait_for_completed()

    # 云台向下旋转20度
    ep_gimbal.move(pitch=-pitch_val, yaw=0).wait_for_completed()

    ep_gimbal.moveto(pitch=0, yaw=0).wait_for_completed()

    ep_robot.close()

