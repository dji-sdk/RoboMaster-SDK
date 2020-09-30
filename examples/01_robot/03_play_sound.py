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
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    # 依次播放几个系统音效
    ep_robot.play_sound(robot.SOUND_ID_ATTACK).wait_for_completed()
    ep_robot.play_sound(robot.SOUND_ID_SHOOT).wait_for_completed()
    ep_robot.play_sound(robot.SOUND_ID_SCANNING).wait_for_completed()
    ep_robot.play_sound(robot.SOUND_ID_RECOGNIZED).wait_for_completed()
    ep_robot.play_sound(robot.SOUND_ID_GIMBAL_MOVE).wait_for_completed()
    ep_robot.play_sound(robot.SOUND_ID_COUNT_DOWN).wait_for_completed()
    ep_robot.play_sound(robot.SOUND_ID_1A).wait_for_completed()
    ep_robot.play_sound(robot.SOUND_ID_1B).wait_for_completed()
    ep_robot.play_sound(robot.SOUND_ID_1C).wait_for_completed()
    ep_robot.play_sound(robot.SOUND_ID_1D).wait_for_completed()
    ep_robot.play_sound(robot.SOUND_ID_1E).wait_for_completed()
    ep_robot.play_sound(robot.SOUND_ID_1F).wait_for_completed()


    ep_robot.close()
