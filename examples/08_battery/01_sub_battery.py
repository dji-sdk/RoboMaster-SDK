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


def sub_info_handler(batter_info, ep_robot):
    percent = batter_info
    print("Battery: {0}%.".format(percent))
    ep_led = ep_robot.led
    brightness = int(percent * 255 / 100)
    ep_led.set_led(comp="all", r=brightness, g=brightness, b=brightness)


if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    ep_battery = ep_robot.battery

    ep_battery.sub_battery_info(5, sub_info_handler, ep_robot)
    time.sleep(10)
    ep_battery.unsub_battery_info()

    ep_robot.close()