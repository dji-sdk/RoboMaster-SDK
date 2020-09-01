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

    #设置PWM输出频率为50Hz
    ep_chassis.set_pwm_freq(pwm1=50,pwm2=50,pwm3=50,pwm4=50,pwm5=50,pwm6=50)
    #设置PWM输出占空比为20%
    ep_chassis.set_pwm_value(pwm1=20,pwm2=20,pwm3=20,pwm4=20,pwm5=20,pwm6=20)

    ep_robot.close()
