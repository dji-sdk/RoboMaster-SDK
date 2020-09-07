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


import struct
import threading
from . import module
from . import protocol
from . import action
from . import logger
from . import dds
from . import util


__all__ = ['Chassis', 'ChassisMoveAction']


class ChassisMoveAction(action.Action):
    _action_proto_cls = protocol.ProtoPositionMove
    _push_proto_cls = protocol.ProtoPositionPush
    _target = protocol.host2byte(3, 6)

    def __init__(self, x=0, y=0, z=0, spd_xy=0, spd_z=0, **kw):
        super().__init__(**kw)
        self._x = x
        self._y = y
        self._z = z
        self._spd_xy = spd_xy
        self._spd_z = spd_z

    def __repr__(self):
        return "action_id:{0}, state:{1}, percent:{2}, x:{3}, y:{4}, z:{5}, xy_speed:{6}, z_speed:{7}".format(
            self._action_id, self._state, self._percent, self._x, self._y, self._z, self._spd_xy, self._spd_z)

    def encode(self):
        proto = protocol.ProtoPositionMove()
        proto._pos_x = util.CHASSIS_POS_X_SET_CHECKER.val2proto(self._x)
        proto._pos_y = util.CHASSIS_POS_Y_SET_CHECKER.val2proto(self._y)
        proto._pos_z = util.CHASSIS_POS_Z_SET_CHECKER.val2proto(self._z)
        # The spd_xy limit to [0.5, 2.0]
        if self._spd_xy < 0.5:
            self._spd_xy = 0.5
            logger.warning("spd_xy: below limit and is set to 0.5")
        if self._spd_xy > 2.0:
            self._spd_xy = 2.0
            logger.warning("spd_xy: over limit and is set to 2.0")
        proto._vel_xy_max = int(160 * self._spd_xy - 70)
        # The spd_z limit to [10, 540]
        if self._spd_z < 10:
            self._spd_z = 10
            logger.warning("spd_z: below limit and is set to 10")
        if self._spd_z > 540:
            self._spd_z = 540
            logger.warning("spd_z: over limit and is set to 540")
        proto._agl_omg_max = int(self._spd_z * 10)
        return proto

    def update_from_push(self, proto):
        if proto.__class__ is not self._push_proto_cls:
            return

        self._percent = proto._percent
        self._update_action_state(proto._action_state)

        self._pos_x = util.CHASSIS_POS_X_SET_CHECKER.proto2val(proto._pos_x)
        self._pos_y = util.CHASSIS_POS_Y_SET_CHECKER.proto2val(proto._pos_y)
        self._pos_z = util.CHASSIS_POS_Z_SET_CHECKER.proto2val(proto._pos_z)
        logger.info("{0} update_from_push: {1}".format(self.__class__.__name__, self))


class PositionSubject(dds.Subject):
    name = dds.DDS_POSITION
    uid = dds.SUB_UID_MAP[name]
    type = dds.DDS_SUB_TYPE_PERIOD

    def __init__(self, cs):
        self._position_x = 0
        self._position_y = 0
        self._position_z = 0
        self._cs = cs
        self._offset_x = 0
        self._offset_y = 0
        self._offset_z = 0
        self._first_flag = True

    def position(self):
        return self._position_x, self._position_y, self._position_z

    def data_info(self):
        ''' cs=0选用当前位置作为坐标原点，否则选用机器人上电时刻位置作为坐标原点'''
        if self._cs == 0:
            if self._first_flag:
                self._offset_x = self._position_x
                self._offset_y = self._position_y
                self._offset_z = self._position_z
                self._first_flag = False
            self._position_x = self._position_x - self._offset_x
            self._position_y = self._position_y - self._offset_y
            self._position_z = self._position_z - self._offset_z
        self._position_x = util.CHASSIS_POS_X_SUB_CHECKER.proto2val(self._position_x)
        self._position_y = util.CHASSIS_POS_Y_SUB_CHECKER.proto2val(self._position_y)
        self._position_z = util.CHASSIS_POS_Z_SUB_CHECKER.proto2val(self._position_z)
        return self._position_x, self._position_y, self._position_z

    def decode(self, buf):
        self._position_x, self._position_y, self._position_z = struct.unpack('<fff', buf)


class AttiInfoSubject(dds.Subject):
    name = dds.DDS_ATTITUDE
    uid = dds.SUB_UID_MAP[name]
    type = dds.DDS_SUB_TYPE_PERIOD

    def __init__(self):
        self._yaw = 0
        self._pitch = 0
        self._roll = 0

    def atti_info(self):
        return self._yaw, self._pitch, self._roll

    def data_info(self):
        return self._yaw, self._pitch, self._roll

    def decode(self, buf):
        self._yaw, self._pitch, self._roll = struct.unpack('<fff', buf)
        self._yaw = util.CHASSIS_YAW_CHECKER.proto2val(self._yaw)
        self._pitch = util.CHASSIS_PITCH_CHECKER.proto2val(self._pitch)
        self._roll = util.CHASSIS_ROLL_CHECKER.proto2val(self._roll)


class ChassisModeSubject(dds.Subject):
    name = dds.DDS_CHASSIS_MODE
    uid = dds.SUB_UID_MAP[name]
    type = dds.DDS_SUB_TYPE_PERIOD

    def __init__(self):
        self._mis_cur_type = 0
        self._sdk_cur_type = 0

    def chassis_mode(self):
        return self._mis_cur_type, self._sdk_cur_type

    def data_info(self):
        return self._sdk_cur_type

    def decode(self, buf):
        self._mis_cur_type, self._sdk_cur_type = struct.unpack('<BB', buf)


class SbusSubject(dds.Subject):
    name = dds.DDS_SBUS
    uid = dds.SUB_UID_MAP[name]
    type = dds.DDS_SUB_TYPE_PERIOD

    def __init__(self):
        self._connect_status = 0
        self._subs_channel = [0]*16

    def subs_data(self):
        return self._connect_status, self._subs_channel

    def data_info(self):
        return self._connect_status, self._subs_channel

    def decode(self, buf):
        [self._connect_status, self._subs_channel[0], self._subs_channel[1], self._subs_channel[2],
         self._subs_channel[3], self._subs_channel[4], self._subs_channel[5], self._subs_channel[6],
         self._subs_channel[7], self._subs_channel[8], self._subs_channel[9], self._subs_channel[10],
         self._subs_channel[11], self._subs_channel[12], self._subs_channel[13], self._subs_channel[14],
         self._subs_channel[15]] = struct.unpack('<Bhhhhhhhhhhhhhhhh', buf)


class VelocitySubject(dds.Subject):
    name = dds.DDS_VELOCITY
    uid = dds.SUB_UID_MAP[name]

    def __init__(self):
        self._vgx = 0
        self._vgy = 0
        self._vgz = 0
        self._vbx = 0
        self._vby = 0
        self._vbz = 0

    @property
    def vel_data(self):
        return self._vgx, self._vgy, self._vgz, self._vbx, self._vby, self._vbz

    def data_info(self):
        return self._vgx, self._vgy, self._vgz, self._vbx, self._vby, self._vbz

    def decode(self, buf):
        self._vgx, self._vgy, self._vgz, self._vbx, self._vby, self._vbz = struct.unpack('<ffffff', buf)
        self._vgx = util.CHASSIS_SPD_X_CHECKER.proto2val(self._vgx)
        self._vgy = util.CHASSIS_SPD_Y_CHECKER.proto2val(self._vgy)
        self._vgz = util.CHASSIS_SPD_Z_CHECKER.proto2val(self._vgz)
        self._vbx = util.CHASSIS_SPD_X_CHECKER.proto2val(self._vbx)
        self._vby = util.CHASSIS_SPD_Y_CHECKER.proto2val(self._vby)
        self._vbz = util.CHASSIS_SPD_Z_CHECKER.proto2val(self._vbz)


class EscSubject(dds.Subject):
    name = dds.DDS_ESC
    uid = dds.SUB_UID_MAP[name]
    type = dds.DDS_SUB_TYPE_PERIOD

    def __init__(self):
        self._speed = [0]*4
        self._angle = [0]*4
        self._timestamp = [0]*4
        self._state = [0]*4

    @property
    def esc_info(self):
        return self._speed, self._angle, self._timestamp, self._state

    def data_info(self):
        return self._speed, self._angle, self._timestamp, self._state

    def decode(self, buf):
        [self._speed[0], self._speed[1], self._speed[2], self._speed[3],
         self._angle[0], self._angle[1], self._angle[2], self._angle[3],
         self._timestamp[0], self._timestamp[1], self._timestamp[2], self._timestamp[3],
         self._state[0], self._state[1], self._state[2], self._state[3]] = struct.unpack('<hhhhhhhhIIIIBBBB', buf)


class ImuSubject(dds.Subject):
    name = dds.DDS_IMU
    uid = dds.SUB_UID_MAP[name]
    type = dds.DDS_SUB_TYPE_PERIOD

    def __init__(self):
        self._acc_x = 0
        self._acc_y = 0
        self._acc_z = 0
        self._gyro_x = 0
        self._gyro_y = 0
        self._gyro_z = 0

    def imu_info(self):
        return self._acc_x, self._acc_y, self._acc_z, self._gyro_x, self._gyro_y, self._gyro_z

    def data_info(self):
        return self._acc_x, self._acc_y, self._acc_z, self._gyro_x, self._gyro_y, self._gyro_z

    def decode(self, buf):
        self._acc_x, self._acc_y, self._acc_z, self._gyro_x, self._gyro_y, self._gyro_z = struct.unpack('<ffffff', buf)
        self._acc_x = util.CHASSIS_ACC_CHECKER.proto2val(self._acc_x)
        self._acc_y = util.CHASSIS_ACC_CHECKER.proto2val(self._acc_y)
        self._acc_z = util.CHASSIS_ACC_CHECKER.proto2val(self._acc_z)
        self._gyro_x = util.CHASSIS_GYRO_CHECKER.proto2val(self._gyro_x)
        self._gyro_y = util.CHASSIS_GYRO_CHECKER.proto2val(self._gyro_y)
        self._gyro_z = util.CHASSIS_GYRO_CHECKER.proto2val(self._gyro_z)


class SaStatusSubject(dds.Subject):
    name = dds.DDS_SA_STATUS
    uid = dds.SUB_UID_MAP[name]
    type = dds.DDS_SUB_TYPE_PERIOD

    def __init__(self):
        self._static_flag = 0
        self._up_hill = 0
        self._down_hill = 0
        self._on_slope = 0
        self._is_pick_up = 0
        self._slip_flag = 0
        self._impact_x = 0
        self._impact_y = 0
        self._impact_z = 0
        self._roll_over = 0
        self._hill_static = 0
        self.resv = 0

    def sa_status(self):
        return self._static_flag, \
               self._up_hill, \
               self._down_hill, \
               self._on_slope, \
               self._is_pick_up, \
               self._slip_flag, \
               self._impact_x, \
               self._impact_y, \
               self._impact_z, \
               self._roll_over, \
               self._hill_static

    def data_info(self):
        return self._static_flag, \
               self._up_hill, \
               self._down_hill, \
               self._on_slope, \
               self._is_pick_up, \
               self._slip_flag, \
               self._impact_x, \
               self._impact_y, \
               self._impact_z, \
               self._roll_over, \
               self._hill_static

    def decode(self, buf):
        self._static_flag = buf[0] & 0x01
        self._up_hill = (buf[0] >> 1) & 0x01
        self._down_hill = (buf[0] >> 2) & 0x01
        self._on_slope = (buf[0] >> 3) & 0x01
        self._is_pick_up = (buf[0] >> 4) & 0x01
        self._slip_flag = (buf[0] >> 5) & 0x01
        self._impact_x = (buf[0] >> 6) & 0x01
        self._impact_y = (buf[0] >> 7) & 0x01
        self._impact_z = (buf[1] >> 0) & 0x01
        self._roll_over = (buf[1] >> 1) & 0x01
        self._hill_static = (buf[1] >> 2) & 0x01


class Chassis(module.Module):
    """ EP 底盘模块，可以控制底盘的速度、位置、订阅底盘的数据，控制麦克纳姆轮等操作 """

    _host = protocol.host2byte(3, 6)

    def __init__(self, robot):
        super().__init__(robot)
        self._action_dispatcher = robot.action_dispatcher
        self._auto_timer = None

    def stop(self):
        if self._auto_timer:
            if self._auto_timer.is_alive():
                self._auto_timer.cancel()
        super().stop()

    def _set_mode(self, mode):
        proto = protocol.ProtoChassisSetWorkMode()
        return self._send_sync_proto(proto)

    def _get_mode(self):
        proto = protocol.ProtoChassisGetWorkMode()
        return self._send_sync_proto(proto)

    # drives.
    def drive_wheels(self, w1=0, w2=0, w3=0, w4=0, timeout=None):
        """　设置麦轮转速

        :param w1: int:[-1000,1000]，右前麦轮速度，以车头方向前进旋转为正方向，单位 rpm
        :param w2: int:[-1000,1000]，左前麦轮速度，以车头方向前进旋转为正方向，单位 rpm
        :param w3: int:[-1000,1000]，左后麦轮速度，以车头方向前进旋转为正方向，单位 rpm
        :param w4: int:[-1000,1000]，右后麦轮速度，以车头方向前进旋转为正方向，单位 rpm
        :param timeout: float:(0,inf)，超过指定时间内未收到麦轮转速指令，主动控制机器人停止，单位 s
        """
        proto = protocol.ProtoSetWheelSpeed()
        proto._w1_spd = util.WHEEL_SPD_CHECKER.val2proto(w1)
        proto._w2_spd = util.WHEEL_SPD_CHECKER.val2proto(-w2)
        proto._w3_spd = util.WHEEL_SPD_CHECKER.val2proto(-w3)
        proto._w4_spd = util.WHEEL_SPD_CHECKER.val2proto(w4)
        if timeout:
            if self._auto_timer:
                if self._auto_timer.is_alive():
                    self._auto_timer.cancel()
            self._auto_timer = threading.Timer(timeout, self._auto_stop_timer, args=("drive_wheels",))
            self._auto_timer.start()
            return self._send_sync_proto(proto)
        return self._send_sync_proto(proto)

    def _auto_stop_timer(self, api="drive_speed"):
        if api == "drive_speed":
            logger.info("Chassis: drive_speed timeout, auto stop!")
            self.drive_speed(0, 0, 0)
        elif api == "drive_wheels":
            logger.info("Chassis: drive_wheels timeout, auto stop!")
            self.drive_wheels(0, 0, 0)
        else:
            logger.warning("Chassis: unsupported api:{0}".format(api))

    def drive_speed(self, x=0.0, y=0.0, z=0.0, timeout=None):
        """ 设置底盘速度，立即生效

        :param x: float:[-3.5,3.5]，x 轴向运动速度即前进速度，单位 m/s
        :param y: float:[-3.5,3.5]，y 轴向运动速度即横移速度，单位 m/s
        :param z: float:[-600,600]，z 轴向运动速度即旋转速度，单位 °/s
        :param timeout: float:(0,inf)，超过指定时间内未收到麦轮转速指令，主动控制机器人停止，单位 s
        """
        proto = protocol.ProtoChassisSpeedMode()
        proto._x_spd = util.CHASSIS_SPD_X_CHECKER.val2proto(x)
        proto._y_spd = util.CHASSIS_SPD_Y_CHECKER.val2proto(y)
        proto._z_spd = util.CHASSIS_SPD_Z_CHECKER.val2proto(z)
        logger.info("x_spd:{0:f}, y_spd:{1:f}, z_spd:{2:f}".format(proto._x_spd, proto._y_spd, proto._z_spd))
        if timeout:
            if self._auto_timer:
                if self._auto_timer.is_alive():
                    self._auto_timer.cancel()
            self._auto_timer = threading.Timer(timeout, self._auto_stop_timer, args=("drive_speed",))
            self._auto_timer.start()
            return self._send_sync_proto(proto)
        return self._send_sync_proto(proto)

    def set_pwm_value(self, pwm1=None, pwm2=None, pwm3=None, pwm4=None, pwm5=None, pwm6=None):
        """ 设置PWM输出占空比

        :param pwm1: int:[0,100]，pwm输出占空比，单位%
        :param pwm2: int:[0,100]，pwm输出占空比，单位%
        :param pwm3: int:[0,100]，pwm输出占空比，单位%
        :param pwm4: int:[0,100]，pwm输出占空比，单位%
        :param pwm5: int:[0,100]，pwm输出占空比，单位%
        :param pwm6: int:[0,100]，pwm输出占空比，单位%
        """
        proto = protocol.ProtoChassisPwmPercent()
        proto._mask = 0
        if pwm1:
            proto._mask = 1
            proto._pwm1 = util.PWM_VALUE_CHECKER.val2proto(pwm1)
        if pwm2:
            proto._mask |= (1 << 1)
            proto._pwm2 = util.PWM_VALUE_CHECKER.val2proto(pwm2)
        if pwm3:
            proto._mask |= (1 << 2)
            proto._pwm3 = util.PWM_VALUE_CHECKER.val2proto(pwm3)
        if pwm4:
            proto._mask |= (1 << 3)
            proto._pwm4 = util.PWM_VALUE_CHECKER.val2proto(pwm4)
        if pwm5:
            proto._mask |= (1 << 4)
            proto._pwm5 = util.PWM_VALUE_CHECKER.val2proto(pwm5)
        if pwm6:
            proto._mask |= (1 << 5)
            proto._pwm6 = util.PWM_VALUE_CHECKER.val2proto(pwm6)
        return self._send_sync_proto(proto)

    def set_pwm_freq(self, pwm1=None, pwm2=None, pwm3=None, pwm4=None, pwm5=None, pwm6=None):
        """ 设置PWM输出频率

        :param pwm1~6: int:[0,50000]，pwm输出频率，单位Hz
        """
        proto = protocol.ProtoChassisPwmFreq()
        proto._mask = 0
        if pwm1:
            proto._mask = 1
            proto._pwm1 = util.PWM_VALUE_CHECKER.val2proto(pwm1)
        if pwm2:
            proto._mask |= (1 << 1)
            proto._pwm2 = util.PWM_VALUE_CHECKER.val2proto(pwm2)
        if pwm3:
            proto._mask |= (1 << 2)
            proto._pwm3 = util.PWM_VALUE_CHECKER.val2proto(pwm3)
        if pwm4:
            proto._mask |= (1 << 3)
            proto._pwm4 = util.PWM_VALUE_CHECKER.val2proto(pwm4)
        if pwm5:
            proto._mask |= (1 << 4)
            proto._pwm5 = util.PWM_VALUE_CHECKER.val2proto(pwm5)
        if pwm6:
            proto._mask |= (1 << 5)
            proto._pwm6 = util.PWM_VALUE_CHECKER.val2proto(pwm6)
        return self._send_sync_proto(proto)

    # actions.
    def move(self, x=0, y=0, z=0, xy_speed=0.5, z_speed=30):
        """ 控制底盘运动当指定位置，坐标轴原点为当前位置

        :param x: float: [-5,5]，x轴向运动距离，单位 m
        :param y: float: [-5,5]，y轴向运动距离，单位 m
        :param z: float: [-1800,1800]，z轴向旋转角度，单位 °
        :param xy_speed: float: [0.5,2]，xy轴向运动速度，单位 m/s
        :param z_speed: float: [10,540]，z轴向旋转速度，单位 °/s
        :return: 返回action对象
        """
        action = ChassisMoveAction(x, y, z, xy_speed, z_speed)
        self._action_dispatcher.send_action(action)
        return action

    # 数据订阅接口
    def sub_position(self, cs=0, freq=5, callback=None, *args, **kw):
        """ 订阅底盘位置信息

        :param cs: int: [0,1] 设置底盘位置的坐标系，0 机器人当前位置，1 机器人上电位置
        :param freq: enum: (1, 5, 10, 20, 50) 设置数据订阅数据的推送频率，单位 Hz
        :param callback: 回调函数，返回数据 (x, y, z):

                        :x: x轴方向距离，单位 m
                        :y: y轴方向距离，单位 m
                        :z: z轴方向旋转角度，单位 °

        :param args: 可变参数
        :param kw: 关键字参数
        :return: bool: 数据订阅结果
        """
        sub = self._robot.dds
        subject = PositionSubject(cs)
        subject.freq = freq
        return sub.add_subject_info(subject, callback, args, kw)

    def unsub_position(self):
        """ 取消订阅底盘位置信息

        :return: bool: 取消数据订阅的结果
        """
        sub_dds = self._robot.dds
        return sub_dds.del_subject_info(dds.DDS_POSITION)

    def sub_attitude(self, freq=5, callback=None, *args, **kw):
        """ 订阅底盘姿态信息

        :param freq: enum: (1, 5, 10, 20, 50) 设置数据订阅数据的推送频率，单位 Hz
        :param callback: 回调函数，返回数据 (yaw, pitch, roll)：

                        :yaw: yaw轴姿态角
                        :pitch: pitch轴姿态角
                        :roll: roll轴姿态角

        :param args: 可变参数
        :param kw: 关键字参数
        :return: bool: 数据订阅结果
        """
        sub = self._robot.dds
        subject = AttiInfoSubject()
        subject.freq = freq
        return sub.add_subject_info(subject, callback, args, kw)

    def unsub_attitude(self):
        """ 取消订阅底盘姿态信息

        :return: bool: 取消数据订阅的结果
        """
        sub_dds = self._robot.dds
        return sub_dds.del_subject_info(dds.DDS_ATTITUDE)

    def sub_status(self, freq=5, callback=None, *args, **kw):
        """ 订阅底盘状态信息

        :param freq: enum: (1, 5, 10, 20, 50)，设置数据订阅数据的推送频率，单位 Hz
        :param callback: 回调函数，返回数据 (static_flag, up_hill, down_hill, on_slope, is_pickup, slip_flag, \
        impact_x, impact_y, impact_z, roll_over, hill_static):

                        :static_flag: 状态标准位
                        :up_hill: 处于上坡状态
                        :down_hill: 处于下坡状态
                        :on_slope: 处于倾斜状态
                        :is_pickup: 处于抱起状态
                        :slip_flag: 车身打滑
                        :impact_x: x轴发生撞击
                        :impact_y: y轴发生撞击
                        :impact_z: z轴发生撞击
                        :roll_over: 车身翻转
                        :hill_static: 处于斜坡状态

        :param args: 可变参数
        :param kw: 关键字参数
        :return: bool: 数据订阅结果
        """
        sub = self._robot.dds
        subject = SaStatusSubject()
        subject.freq = freq
        return sub.add_subject_info(subject, callback, args, kw)

    def unsub_status(self):
        """ 取消订阅底盘状态信息

        :return: bool: 取消数据订阅的结果
        """
        sub_dds = self._robot.dds
        return sub_dds.del_subject_info(dds.DDS_SA_STATUS)

    def sub_imu(self, freq=5, callback=None, *args, **kw):
        """ 订阅底盘IMU陀螺仪信息

        :param freq: enum: (1, 5, 10, 20, 50)，设置数据订阅数据的推送频率，单位 Hz
        :param callback: 回调函数，返回数据 (acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z):

                    :acc_x: x轴加速度
                    :acc_y: y轴加速度
                    :acc_z: z轴加速度
                    :gyro_x: x轴角速度
                    :gyro_y: y轴角速度
                    :gyro_z: z轴角速度

        :param args: 可变参数
        :param kw: 关键字参数
        :return: bool: 数据订阅结果
        """
        sub_dds = self._robot.dds
        subject = ImuSubject()
        subject.freq = freq
        return sub_dds.add_subject_info(subject, callback, args, kw)

    def unsub_imu(self):
        """ 取消订阅底盘IMU陀螺仪信息

        :return: bool: 取消数据订阅的结果
        """
        sub_dds = self._robot.dds
        return sub_dds.del_subject_info(dds.DDS_IMU)

    def sub_mode(self, freq=5, callback=None, *args, **kw):
        """ 订阅底盘模式信息

        :param freq: enum: (1, 5, 10, 20, 50)，设置数据订阅数据的推送频率，单位 Hz
        :param callback: 回调函数，返回数据 mode:

                        :mode: 底盘模式

        :param args: 可变参数
        :param kw: 关键字参数
        :return: bool: 数据订阅结果
        """
        sub_dds = self._robot.dds
        subject = ChassisModeSubject()
        subject.freq = freq
        return sub_dds.add_subject_info(subject, callback, args, kw)

    def unsub_mode(self):
        """ 取消订阅底盘模式信息

        :return: bool: 取消数据订阅的结果
        """
        sub_dds = self._robot.dds
        return sub_dds.del_subject_info(dds.DDS_CHASSIS_MODE)

    def sub_esc(self, freq=5, callback=None, *args, **kw):
        """ 订阅底盘电调信息

        :param freq: enum: (1, 5, 10, 20, 50)，设置数据订阅数据的推送频率，单位 Hz
        :param callback: 回调函数，返回数据 (speed[4], angle[4], timestamp, state):

                        :speed[4]: 4个电机的速度值，单位rpm,范围：-8192~8191
                        :angle[4]: 4个电机的角度值，数值范围：0~32767映射0~360
                        :timestamp: 4个电机的包序号
                        :state: 4个电调的状态

        :param args: 可变参数
        :param kw: 关键字参数
        :return: bool: 数据订阅结果
        """
        sub_dds = self._robot.dds
        subject = EscSubject()
        subject.freq = freq
        return sub_dds.add_subject_info(subject, callback, args, kw)

    def unsub_esc(self):
        """ 取消订阅电调信息

        :return: bool: 取消数据订阅的结果
        """
        sub_dds = self._robot.dds
        return sub_dds.del_subject_info(dds.DDS_ESC)

    def sub_velocity(self, freq=5, callback=None, *args, **kw):
        """ 订阅底盘加速度信息

        :param freq: enum:(1, 5, 10, 20, 50) 设置数据订阅数据的推送频率，单位 Hz
        :param callback: 回调函数，返回数据（vgx, vgy, vgz, vbx, vby, vbz)：

                        :vgx: 上电时刻下的世界坐标系下x方向速度
                        :vgy: 上电时刻下的世界坐标系下y方向速度
                        :vgz: 上电时刻下的世界坐标系下z方向速度
                        :vbx: 当前时刻的车身坐标系下x方向速度
                        :vby: 当前时刻的车身坐标系下y方向速度
                        :vbz: 当前时刻的车身坐标系下z方向速度

        :param args: 可变参数
        :param kw: 关键字参数
        :return: bool: 数据订阅结果
        """
        sub_dds = self._robot.dds
        subject = VelocitySubject()
        subject.freq = freq
        return sub_dds.add_subject_info(subject, callback, args, kw)

    def unsub_velocity(self):
        """ 取消订阅底盘加速度信息

        :return: bool: 取消数据订阅的结果
        """
        sub_dds = self._robot.dds
        return sub_dds.del_subject_info(dds.DDS_VELOCITY)

    def _sub_sbus(self, freq=5, callback=None, *args, **kw):
        """ 订阅底盘SBUS信息

        :param freq: enum: (1, 5, 10, 20, 50)，设置数据订阅数据的推送频率，单位 Hz
        :param callback: 回调函数，返回数据 (connect_status, sbus_channel[16]):

                        :connect_status: sbus是否连接
                        :sbus_channel[16]: sbus的16通道数据

        :param args: 可变参数
        :param kw: 关键字参数
        :return: bool: 数据订阅结果
        """
        sub_dds = self._robot.dds
        subject = SbusSubject()
        subject.freq = freq
        return sub_dds.add_subject_info(subject, callback, args, kw)

    def _unsub_sbus(self):
        """ 取消订阅SBUS信息

        :return: bool: 取消数据订阅的结果
        """
        sub_dds = self._robot.dds
        return sub_dds.del_subject_info(dds.DDS_SBUS)
