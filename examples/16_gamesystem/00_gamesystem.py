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


def robot_control(run):
    if run == ord('w'):
        print("forward！")
        ep.chassis.drive_speed(0.5, 0, 0)
    elif run == ord('s'):
        print("back！")
        ep.chassis.drive_speed(-0.5, 0, 0)
    elif run == ord('a'):
        print("left")
        ep.chassis.drive_speed(0, -0.5, 0)
    elif run == ord('d'):
        print("right！")
        ep.chassis.drive_speed(0, 0.5, 0)
    elif run == 0:
        print("stop！")
        ep.chassis.drive_speed(0, 0, 0)


def sub_data_handler(sub_info):
    """    返回数据 (buf: 键鼠数据 [mouse_press, mouse_x, mouse_y, seq, key_num, key_1, key2, ….])
           mouse_press: 1为鼠标右键, 2为鼠标左键, 4为鼠标中间
           mouse_x : 鼠标移动距离, 范围-100 ~ 100
           mouse_y : 鼠标移动距离, 范围-100 ~ 100
           seq: 序列号 0~255
           key_num: 识别到的按键数, 最多识别三个按键
           key1: 被按下的键盘键值
    """
    print("mouse_press:{0} mouse_x:{1} mouse_y:{2} key1:{3}"
          .format(sub_info[0], sub_info[1], sub_info[2], sub_info[-1]))
    robot_control(sub_info[-1])


if __name__ == '__main__':
    ep = robot.Robot()
    ep.initialize(conn_type="rndis")
    ep.chassis.stick_overlay(1)
    ep.set_robot_mode(mode=robot.GIMBAL_LEAD)
    ep.sub_game_msg(callback=sub_data_handler)
