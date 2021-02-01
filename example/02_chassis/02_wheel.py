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
import time
from robomaster import robot


if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    ep_chassis = ep_robot.chassis

    # 指定麥輪速度
    speed = 50
    slp = 1

    # 轉動右前輪
    ep_chassis.drive_wheels(w1=speed, w2=0, w3=0, w4=0)
    time.sleep(slp)

    # 轉動左前輪
    ep_chassis.drive_wheels(w1=0, w2=speed, w3=0, w4=0)
    time.sleep(slp)

    # 轉動左後輪
    ep_chassis.drive_wheels(w1=0, w2=0, w3=speed, w4=0)
    time.sleep(slp)

    # 轉動右後輪
    ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=speed)
    time.sleep(slp)

    # 前進 3秒
    ep_chassis.drive_wheels(w1=speed, w2=speed, w3=speed, w4=speed)
    time.sleep(slp)

    # 後退 3秒
    ep_chassis.drive_wheels(w1=-speed, w2=-speed, w3=-speed, w4=-speed)
    time.sleep(slp)

    # 左移 3秒
    ep_chassis.drive_wheels(w1=speed, w2=-speed, w3=speed, w4=-speed)
    time.sleep(slp)

    # 右移 3秒
    ep_chassis.drive_wheels(w1=-speed, w2=speed, w3=-speed, w4=speed)
    time.sleep(slp)

    # 左轉 3秒
    ep_chassis.drive_wheels(w1=speed, w2=-speed, w3=-speed, w4=speed)
    time.sleep(slp)

    # 右轉 3秒
    ep_chassis.drive_wheels(w1=-speed, w2=speed, w3=speed, w4=-speed)
    time.sleep(slp)

    # 停止麥輪運動
    ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)

    ep_robot.close()
