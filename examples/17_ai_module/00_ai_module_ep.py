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
from robomaster import robot


def ai_callback(sub_info):
    print(sub_info)
    num, list_info = sub_info
    for i in range(0, num):
        id, x, y, w, h, C = list_info[i]
        print("ai target index:{0} id:{1}, x:{2}, y:{3}, w:{4}, h:{5}, C:{6}".format(i, id, x, y, w, h, C))


if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="rndis")

    ep_ai_module = ep_robot.ai_module

    # 订阅ai模块的事件
    ep_ai_module.sub_ai_event(callback=ai_callback)
    time.sleep(15)
    ep_ai_module.unsub_ai_event()

    ep_robot.close()
