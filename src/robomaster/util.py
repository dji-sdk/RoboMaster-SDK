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


# read from config, localization, Use Metric or Inch.
from . import logger

UNIT_METRIC = 'Unit Metric'
UNIT_INCH = 'Unit Inch'

_VALID_UNIT = {UNIT_METRIC, UNIT_INCH}


class UnitChecker(object):
    # Unit
    def __init__(self, name, default=0, start=0, end=0, step=1, decimal=2, scale=1, unit=UNIT_METRIC):
        self._name = name
        self._start = start
        self._end = end
        self._step = step
        self._decimal = decimal
        self._scale = scale
        self._unit = unit
        # if decimal = 0, set None to round() to get a integer
        if self._decimal == 0:
            self._decimal = None

    @property
    def name(self):
        return self._name

    @property
    def default(self):
        return self._default

    @property
    def scale(self):
        return self._scale

    @property
    def step(self):
        return self._step

    @property
    def decimal(self):
        return self._decimal

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def unit(self):
        return self._unit

    def check(self, value):
        if self._start and self._end:
            if value > self._end:
                value = self._end
                logger.warning("{0}: over limit and is set to {1}".format(self._name, self._end))
            if value < self._start:
                value = self._start
                logger.warning("{0}: below limit and is set to {1}".format(self._name, self._start))
        return value

    def proto2val(self, val):
        val = val / self.scale
        val = round(val, self._decimal)
        val = self.check(val)
        return val

    def val2proto(self, val):
        val = self.check(val)
        val = val * self._scale
        val = round(val, self._decimal)
        return val


# 云台目标角度
GIMBAL_PITCH_TARGET_CHECKER = UnitChecker("gimbal pitch target", default=0, start=-20.0, end=35.0, step=1, decimal=0,
                                          scale=10)
GIMBAL_YAW_TARGET_CHECKER = UnitChecker("gimbal yaw target", default=0, start=-250, end=250, step=1, decimal=0,
                                        scale=10)
# 云台旋转角度
GIMBAL_PITCH_MOVE_CHECKER = UnitChecker("gimbal pitch move", default=0, start=-55.0, end=55.0, step=1, decimal=0,
                                        scale=10)
GIMBAL_YAW_MOVE_CHECKER = UnitChecker("gimbal yaw move", default=0, start=-500, end=500, step=1, decimal=0, scale=10)

# 云台位置控制模式时的速度参数
GIMBAL_PITCH_MOVE_SPEED_SET_CHECKER = UnitChecker("gimbal pitch move speed set", default=30, start=0, end=540, step=1,
                                                  decimal=0, scale=1)
GIMBAL_YAW_MOVE_SPEED_SET_CHECKER = UnitChecker("gimbal yaw move speed set", default=30, start=0, end=540, step=1,
                                                decimal=0, scale=1)
# 云台速度控制模式时的速度参数
GIMBAL_PITCH_SPEED_SET_CHECKER = UnitChecker("gimbal pitch speed set", default=30, start=-540, end=540, step=1,
                                             decimal=0, scale=10)
GIMBAL_YAW_SPEED_SET_CHECKER = UnitChecker("gimbal yaw speed set", default=30, start=-540, end=540, step=1, decimal=0,
                                           scale=10)

GIMBAL_ATTI_PITCH_CHECKER = UnitChecker("gimbal atti pitch", default=0, start=None, end=None, step=1, decimal=2,
                                        scale=10)
GIMBAL_ATTI_YAW_CHECKER = UnitChecker("gimbal atti yaw", default=0, start=None, end=None, step=1, decimal=2, scale=10)

# 底盘数值检查
CHASSIS_POS_X_SET_CHECKER = UnitChecker('chassis pos x set', default=0, start=-5.0, end=5.0, step=0.01, decimal=0,
                                        scale=100)
CHASSIS_POS_Y_SET_CHECKER = UnitChecker('chassis pos y set', default=0, start=-5.0, end=5.0, step=0.01, decimal=0,
                                        scale=100)
CHASSIS_POS_Z_SET_CHECKER = UnitChecker('chassis pos z set', default=0, start=-1800, end=1800, step=0.1, decimal=0,
                                        scale=10)

CHASSIS_POS_X_SUB_CHECKER = UnitChecker('chassis pos x sub', default=0, start=None, end=None, step=0.01, decimal=5)
CHASSIS_POS_Y_SUB_CHECKER = UnitChecker('chassis pos y sub', default=0, start=None, end=None, step=0.01, decimal=5)
CHASSIS_POS_Z_SUB_CHECKER = UnitChecker('chassis pos z sub', default=0, start=None, end=None, step=0.1, decimal=2,
                                        scale=10)

CHASSIS_PITCH_CHECKER = UnitChecker('chassis pitch', default=0, start=-180, end=180, step=0.1, decimal=2, scale=1)
CHASSIS_YAW_CHECKER = UnitChecker('chassis yaw', default=0, start=-180, end=180, step=0.1, decimal=2, scale=1)
CHASSIS_ROLL_CHECKER = UnitChecker('chassis roll', default=0, start=-180, end=180, step=0.1, decimal=2, scale=1)

CHASSIS_ACC_CHECKER = UnitChecker('chassis acc', default=0, start=None, end=None, step=None, decimal=5)
CHASSIS_GYRO_CHECKER = UnitChecker('chassis gyro', default=0, start=None, end=None, step=None, decimal=5)

CHASSIS_SPD_X_CHECKER = UnitChecker('chassis spd x', default=0, start=-3.5, end=3.5, step=0.01, decimal=2)
CHASSIS_SPD_Y_CHECKER = UnitChecker('chassis spd y', default=0, start=-3.5, end=3.5, step=0.01, decimal=2)
CHASSIS_SPD_Z_CHECKER = UnitChecker('chassis spd z', default=0, start=-600, end=600, step=1, decimal=0)

WHEEL_SPD_CHECKER = UnitChecker('wheel speed', default=0, start=-1000, end=1000, step=1, decimal=0)

PWM_VALUE_CHECKER = UnitChecker('pwm value', default=0, start=0, end=50000, step=1, decimal=0)
PWM_FREQ_CHECKER = UnitChecker('pwm freq', default=1000, start=0, end=100, step=1, decimal=0, scale=10)

# 机械臂、机械爪数值检查
ROBOTIC_ARM_POS_CHECK = UnitChecker('robotic arm pos', default=0, start=None, end=None, step=1, decimal=0)
GRIPPER_POWER_CHECK = UnitChecker('gripper power', default=50, start=1, end=100, step=1, decimal=0, scale=6.6)

COLOR_VALUE_CHECKER = UnitChecker('color rgb', default=0, start=0, end=255, step=1, decimal=0)
FIRE_TIMES_CHECKER = UnitChecker('fire times', default=1, start=1, end=5, step=1, decimal=0)
