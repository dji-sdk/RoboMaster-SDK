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


def sub_data_handler(angle_info):
    pitch_angle, yaw_angle, pitch_ground_angle, yaw_ground_angle = angle_info
    print("gimbal angle: pitch_angle:{0}, yaw_angle:{1}, pitch_ground_angle:{2}, yaw_ground_angle:{3}".format(
        pitch_angle, yaw_angle, pitch_ground_angle, yaw_ground_angle))


if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    ep_gimbal = ep_robot.gimbal

    # 订阅数据
    ep_gimbal.sub_angle(freq=5, callback=sub_data_handler)
    ep_gimbal.moveto(pitch=20, yaw=60).wait_for_completed()
    ep_gimbal.moveto(pitch=-10, yaw=-60).wait_for_completed()
    ep_gimbal.moveto(pitch=0, yaw=0, pitch_speed=100, yaw_speed=100).wait_for_completed()
    ep_gimbal.unsub_angle()

    ep_robot.close()
