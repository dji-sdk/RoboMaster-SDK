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


def sub_atti_info_handler(attitute_info):
    yaw, pitch, roll = attitute_info
    print("Drone attitude: yaw:{0}, ptich:{1}, roll:{2} ".format(yaw, pitch, roll))


def sub_imu_info_handler(imu_info):
    vgx, vgy, vgz, agx, agy, agz = imu_info
    print("Drone imu: vgx {0}, vgy {1}, vgz {2}, agx {3}, agy {4}, agz {5}".format(vgx, vgy, vgz, agx, agy, agz))


if __name__ == '__main__':
    tl_drone = robot.Drone()
    tl_drone.initialize()

    # 订阅信息
    tl_drone.flight.sub_imu(5, sub_imu_info_handler)
    tl_drone.flight.sub_attitude(10, sub_atti_info_handler)

    # 起飞
    tl_drone.flight.takeoff().wait_for_completed()
    # 降落
    tl_drone.flight.take_off().wait_for_completed()

    # 取消所有订阅
    tl_drone.flight.unsub_imu()
    tl_drone.flight.unsub_attitude()
    time.sleep(5)

    tl_drone.close()

