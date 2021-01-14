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
import time


def sub_data_handler(sub_info):
    distance = sub_info
    print("tof1:{0}  tof2:{1}  tof3:{2}  tof4:{3}".format(distance[0], distance[1], distance[2], distance[3]))


if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    ep_sensor = ep_robot.sensor
    ep_sensor.sub_distance(freq=5, callback=sub_data_handler)
    time.sleep(60)
    ep_sensor.unsub_distance()
    ep_robot.close()
