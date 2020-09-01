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


import random
import time
import robomaster
from robomaster import robot
from robomaster import armor


def hit_callback(sub_info, ep_robot):
    # 被击打装甲的ID，被击打类型
    armor_id, hit_type = sub_info
    print("hit event: hit_comp:{0}, hit_type:{1}".format(armor_id, hit_type))
    # 被击打后变换所有装甲的颜色
    ep_led = ep_robot.led
    ep_led.set_led(comp="all", r=random.randint(0, 255), g=random.randint(0, 255), b=random.randint(0, 255))


if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    ep_armor = ep_robot.armor

    # 设置所有装甲灵敏度为 5
    ep_armor.set_hit_sensitivity(comp="all", sensitivity=5)

    # 订阅装甲被击打的事件
    ep_armor.sub_hit_event(hit_callback, ep_robot)
    time.sleep(15)
    ep_armor.unsub_hit_event()

    ep_robot.close()