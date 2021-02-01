# -*-coding:utf-8-*-
# Copyright (c) 2020 DJI.
#
# Licensed under The 3-Clause BSD License (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the file LICENSE.txt or at
#
#     https://opensource.org/licenses/BSD-3-Clause
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
from multi_robomaster import multi_robot
from robomaster import led, blaster


ROBOTS_NUM = 6
DISTANCE_BY_SITE = 0.3


def reset_task(robot_group):
    """初始自由模式 & 關掉所有燈效"""
    robot_group.led.set_led(led.COMP_ALL, 255, 1, 1, led.EFFECT_OFF)
    robot_group.set_group_robots_mode(multi_robot.FREE_MODE)
    robot_group.led.set_led(led.COMP_ALL, 1, 255, 1, led.EFFECT_FLASH)
    # 目前只有步兵車，可以這樣用
    robot_group.gimbal.moveto(0, 0, 180, 180).wait_for_completed()
    robot_group.led.set_led(led.COMP_ALL, 255, 1, 1, led.EFFECT_OFF)


def ep_arm_initial_pos(robot_group):
    """ep_arm 初始雲台位置"""
    robot_group.gimbal.moveto(0, 0, 180, 180).wait_for_completed()
    robot_group.gimbal.moveto(-20, 0, 100, 100).wait_for_completed()


def ep_gimbal_initial_pos(robot_group):
    """ep_gimbal 初始雲台位置"""
    robot_group.gimbal.moveto(0, 0, 180, 180).wait_for_completed()
    robot_group.gimbal.moveto(-20, 0, 100, 100).wait_for_completed()


def light_order(robot_group):
    """組內小車燈依次亮起,雲台依次抬起"""
    media_sound_solmization_1a = 0x110
    music_note = media_sound_solmization_1a
    count = 0
    for robot_id in robot_group._robots_id_in_group_list:
        count += 1
        robot_obj = robot_group.get_robot(robot_id)
        # robot_obj.play_sound(music_note).wait_for_completed(0.5)
        # 音符的編碼順序為 1A -> 1ASharp -> 1B -> 1BSharp... ，因此每次要移動兩個編碼才能到下一個音符
        music_note += 2
        robot_obj.blaster.fire(fire_type='water', times=1)
        if count & 0x01:
            robot_obj.led.set_led(led.COMP_ALL, 255, 1, 1, led.EFFECT_ON)
            robot_obj.gimbal.moveto(0, 0, 180, 180).wait_for_completed()
        else:
            robot_obj.led.set_led(led.COMP_ALL, 75, 255, 255, led.EFFECT_ON)
            robot_obj.gimbal.moveto(0, 0, 180, 180).wait_for_completed()
        time.sleep(0.5)


def move_forward(robot_group):
    """全體前進"""
    robot_group.chassis.move(0.5, 0, 0, 1).wait_for_completed()


def rotate_right(robot_group):
    """底盤右轉"""
    robot_group.set_group_robots_mode(multi_robot.CHASSIS_LEAD_MODE)
    time.sleep(0.5)
    robot_group.chassis.move(0, 0, -90, 0, 180).wait_for_completed()


def rotate_left(robot_group):
    """底盤左轉"""
    robot_group.set_group_robots_mode(multi_robot.CHASSIS_LEAD_MODE)
    time.sleep(0.5)
    robot_group.chassis.move(0, 0, 90, 0, 180).wait_for_completed()


def rotate_dance(robot_group):
    """底盤solo舞蹈"""
    robot_group.set_group_robots_mode(multi_robot.CHASSIS_LEAD_MODE)
    robot_group.chassis.move(0.2, 0, 0, 1).wait_for_completed()
    robot_group.chassis.move(0, 0, 45, 0, 180).wait_for_completed()
    robot_group.chassis.move(0, 0, -90, 0, 180).wait_for_completed()
    robot_group.chassis.move(0, 0, 45, 0, 180).wait_for_completed()
    robot_group.chassis.move(0, 0, 360, 0, 180).wait_for_completed()


def move_backward(robot_group):
    """底盤後移"""
    robot_group.chassis.move(-DISTANCE_BY_SITE, 0, 0, 1, 0).wait_for_completed()


def led_red_blink(robot_group):
    """紅燈閃爍"""
    robot_group.led.set_led(led.COMP_ALL, 255, 1, 1, led.EFFECT_FLASH)


def led_grey_blink(robot_group):
    """grey閃爍"""
    robot_group.led.set_led(led.COMP_ALL, 75, 255, 255, led.EFFECT_FLASH)


def led_red_solid(robot_group):
    """紅燈常亮"""
    robot_group.led.set_led(led.COMP_ALL, 255, 1, 1, led.EFFECT_ON)


def led_grey_solid(robot_group):
    """grey常亮"""
    robot_group.led.set_led(led.COMP_ALL, 75, 255, 255, led.EFFECT_ON)


def move_left(robot_group):
    """底盤左移"""
    robot_group.chassis.move(0, 0.6, 0, 2, 0).wait_for_completed()


def move_right(robot_group):
    """底盤右移"""
    robot_group.chassis.move(0, -0.6, 0, 2, 0).wait_for_completed()


def gimbal_down(robot_group):
    """雲台下垂"""
    robot_group.gimbal.moveto(-20, 0, 180, 180).wait_for_completed()


def gimbal_recenter(robot_group):
    """雲台回中"""
    robot_group.gimbal.moveto(0, 0, 180, 180).wait_for_completed()


def rotate_circle_right(robot_group):
    """順時針轉圈"""
    robot_group.chassis.move(0, 0, 360, 0, 360).wait_for_completed()


def rotate_circle_left(robot_group):
    """逆時針轉圈"""
    robot_group.chassis.move(0, 0, -360, 0, 360).wait_for_completed()


def rotate_right_dance(robot_group):
    """右轉"""
    robot_group.set_group_robots_mode(multi_robot.CHASSIS_LEAD_MODE)
    robot_group.chassis.move(0, 0, -90, 0, 180).wait_for_completed()
    robot_group.gimbal.moveto(-20, 0, 100, 100).wait_for_completed()


def rotate_left_dance(robot_group):
    """左轉"""
    robot_group.set_group_robots_mode(multi_robot.CHASSIS_LEAD_MODE)
    robot_group.chassis.move(0, 0, 90, 0, 180).wait_for_completed()
    robot_group.gimbal.moveto(-20, 0, 100, 100).wait_for_completed()


def gimbal_left_up(robot_group):
    """雲台左轉，並抬起"""
    robot_group.set_group_robots_mode(multi_robot.FREE_MODE)
    robot_group.gimbal.moveto(30, 90, 100, 100).wait_for_completed()


def gimbal_right_up(robot_group):
    """雲台右轉,並抬起"""
    robot_group.set_group_robots_mode(multi_robot.FREE_MODE)
    robot_group.gimbal.moveto(30, -90, 100, 100).wait_for_completed()


def ending_formation(robot_group):
    """結束隊形"""
    robot_group.blaster.fire(blaster.WATER_FIRE, 3)
    time.sleep(2)
    robot_group.gimbal.moveto(20, 0, 100, 100).wait_for_completed()
    # 連續執行三次點頭動作
    for count in range(3):
        robot_group.gimbal.move(-20, 0, 150, 150).wait_for_completed()
        robot_group.gimbal.move(20, 0, 150, 150).wait_for_completed()
    # 低頭，熄燈，落幕
    robot_group.gimbal.moveto(-20, 0, 100, 100).wait_for_completed()
    robot_group.led.set_led(led.COMP_ALL, 255, 1, 1, led.EFFECT_OFF)


def nod_action(robot_group):
    """雲台做點頭動作"""
    # sound_action = robot_group.play_sound(define.SOUND_ID_ATTACK, 3)
    robot_group.gimbal.moveto(-20, 0, 100, 100).wait_for_completed()
    robot_group.gimbal.moveto(0, 0, 100, 100).wait_for_completed()


if __name__ == '__main__':
    # robomaster.config.LOCAL_IP_STR = "192.168.1.111"
    # get robot sn by run the exmaples of /15_multi_robot/multi_ep/01_scan_robot_sn.py
    robots_sn_list = ['3JKDH3B00138T0', '3JKDH3B001628K', '3JKDH3B0016UMV',
                      '3JKDH3B001M8MW', '3JKDH3B001PQ53', '3JKDH3B001470C']

    multi_robots = multi_robot.MultiEP()
    multi_robots.initialize()
    # 本例程只支持帶雲台的EP車，不支持夾爪的EP車, 如有夾爪請自行修改代碼
    number = multi_robots.number_id_by_sn([0, robots_sn_list[0]], [1, robots_sn_list[1]], [2, robots_sn_list[2]],
                                          [3, robots_sn_list[3]], [4, robots_sn_list[4]], [5, robots_sn_list[5]])
    print("The number of robot is: {0}".format(number))
    robot_group_all = multi_robots.build_group([0, 1, 2, 3, 4, 5])
    robot_group_ep_gimbal = multi_robots.build_group([0, 2, 4])
    robot_group_ep_arm = multi_robots.build_group([1, 3, 5])

    ep_gimbal_leader = multi_robots.build_group([2])
    ep_arm_leader = multi_robots.build_group([3])
    # 初始擺放，雲台向左，雲台向右，依次擺放
    multi_robots.run([robot_group_all, reset_task])
    multi_robots.run([robot_group_ep_gimbal, ep_gimbal_initial_pos], [robot_group_ep_arm, ep_arm_initial_pos])
    # 依次點亮燈，抬起雲台
    multi_robots.run([robot_group_all, light_order])
    # 兩組向兩面散開
    multi_robots.run([robot_group_all, move_forward])
    # 面向觀眾
    multi_robots.run([robot_group_ep_gimbal, rotate_left], [robot_group_ep_arm, rotate_right])
    # 兩邊對齊
    multi_robots.run([robot_group_ep_gimbal, move_backward])
    # 燈效閃爍
    multi_robots.run([robot_group_ep_gimbal, led_red_blink], [robot_group_ep_arm, led_grey_blink])
    # 兩邊轉頭面向對方
    multi_robots.run([robot_group_ep_gimbal, rotate_left], [robot_group_ep_arm, rotate_right])
    # 步兵leader 舞
    multi_robots.run([ep_gimbal_leader, rotate_dance])
    # 點頭
    multi_robots.run([robot_group_ep_arm, nod_action])
    # leader 舞
    multi_robots.run([ep_arm_leader, rotate_dance])
    # 步兵點頭
    multi_robots.run([robot_group_ep_gimbal, nod_action])
    # 面向觀眾
    multi_robots.run([robot_group_ep_gimbal, rotate_right], [robot_group_ep_arm, rotate_left])
    # 燈效
    multi_robots.run([robot_group_ep_gimbal, led_red_solid], [robot_group_ep_arm, led_grey_solid])
    # 兩邊左右旋轉
    multi_robots.run([robot_group_ep_gimbal, rotate_right], [robot_group_ep_arm, rotate_left])
    multi_robots.run([robot_group_ep_gimbal, rotate_left], [robot_group_ep_arm, rotate_right])
    multi_robots.run([robot_group_ep_gimbal, rotate_circle_right], [robot_group_ep_arm, rotate_circle_left])
    multi_robots.run([robot_group_ep_gimbal, rotate_circle_left], [robot_group_ep_arm, rotate_circle_right])
    # 結束隊形,對天空放禮炮->
    multi_robots.run([robot_group_ep_gimbal, gimbal_right_up], [robot_group_ep_arm, gimbal_left_up])
    multi_robots.run([robot_group_all, ending_formation])

    print("Game over")


