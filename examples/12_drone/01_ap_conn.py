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


if __name__ == '__main__':
    # 如果本地IP 自动获取不正确，手动指定本地IP地址
    # robomaster.config.LOCAL_IP_STR = "192.168.10.22"
    tl_drone = robot.Drone()
    # 初始化
    tl_drone.initialize()

    # 获取飞机SDK版本信息
    version = tl_drone.get_sdk_version()
    print("Drone SDK Version: {0}".format(version))

    tl_drone.close()
