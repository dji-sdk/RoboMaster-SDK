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


from robomaster import robot


if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    ep_chassis = ep_robot.chassis

    x_val = 0.5
    y_val = 0.6
    z_val = 90

    # 前进 0.5米
    ep_chassis.move(x=x_val, y=0, z=0, xy_speed=0.7).wait_for_completed()

    # 后退 0.5米
    ep_chassis.move(x=-x_val, y=0, z=0, xy_speed=0.7).wait_for_completed()

    # 左移 0.6米
    ep_chassis.move(x=0, y=-y_val, z=0, xy_speed=0.7).wait_for_completed()

    # 右移 0.6米
    ep_chassis.move(x=0, y=y_val, z=0, xy_speed=0.7).wait_for_completed()

    # 左转 90度
    ep_chassis.move(x=0, y=0, z=z_val, z_speed=45).wait_for_completed()

    # 右转 90度
    ep_chassis.move(x=0, y=0, z=-z_val, z_speed=45).wait_for_completed()

    ep_robot.close()
