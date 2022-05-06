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
from . import logger
from . import action
from . import protocol
from . import dds


'''
Tello EDU, Flight.
Tello IP. 192.168.10.1 UDP PORT:8889

send command.

0.0.0.0 UDP PORT: 8890

0.0.0.0 11111 接收视频流

控制命令 ok, error
设置命令 ok, error
读取命令 ok, error

'''

__all__ = ['Flight', 'FORWARD', 'BACKWARD', 'UP', 'DOWN', 'LEFT', 'RIGHT', 'CLOCKWISE', 'COUNTERCLOCKWISE']

FORWARD = 'forward'
BACKWARD = 'back'
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
CLOCKWISE = 'cw'
COUNTERCLOCKWISE = 'ccw'


class FlightAction(action.TextAction):
    _action_proto_cls = protocol.TextProtoDrone
    _push_proto_cls = protocol.TextProtoDrone
    _target = 'Flight'

    def __init__(self, text_cmd, **kw):
        super().__init__(**kw)
        self.text_cmd = text_cmd
        if self.text_cmd[0:2] == 'Re':
            self._target = self.text_cmd[0:6]
        print('target:{}, text_cmd:{}'.format(self._target, text_cmd))

    def encode(self):
        proto = self._action_proto_cls()
        proto.text_cmd = self.text_cmd
        return proto

    def update_from_push(self, proto):
        if proto.__class__ is not self._push_proto_cls:
            logger.warning("FlightAction, update_from_push, proto.__class__ is not self._push_proto_cls")
            return
        self._update_action_state(proto._action_state)
        logger.info("{0} update_from_push: {1}".format(self.__class__.__name__, vars(self)))


class TelloAttiInfoSubject(dds.Subject):
    name = dds.DDS_TELLO_ATTITUDE

    def __init__(self):
        self._yaw = 0
        self._pitch = 0
        self._roll = 0
        self._info_num = 3
        self._freq = protocol.TelloDdsProto.DDS_FREQ

    def atti_info(self):
        return self._yaw, self._pitch, self._roll

    def data_info(self):
        return self._yaw, self._pitch, self._roll

    def decode(self, buf):
        push_info = buf.split(';')
        found_info_num = 0
        for info in push_info:
            if protocol.TelloDdsProto.DDS_YAW_FLAG in info:
                yaw_info = info.split(':')[1]
                self._yaw = int(yaw_info)
                found_info_num += 1
            elif protocol.TelloDdsProto.DDS_PITCH_FLAG in info:
                pitch_info = info.split(':')[1]
                self._pitch = int(pitch_info)
                found_info_num += 1
            elif protocol.TelloDdsProto.DDS_ROLL_FLAG in info:
                roll_info = info.split(':')[1]
                self._roll = int(roll_info)
                found_info_num += 1
        if found_info_num == self._info_num:
            return True
        else:
            logger.warning("TelloAttiInfoSubject: decode, found_info_num {0} is not match self._info_num {1}".format(
                found_info_num, self._info_num))
            return False

    @property
    def freq(self):
        return self._freq

    @freq.setter
    def freq(self, in_freq):
        if in_freq == 1 or in_freq == 5 or in_freq == 10:
            self._freq = in_freq


class TelloImuInfoSubject(dds.Subject):
    name = dds.DDS_TELLO_IMU

    def __init__(self):
        self._vgx = 0
        self._vgy = 0
        self._vgz = 0
        self._agx = 0
        self._agy = 0
        self._agz = 0
        self._info_num = 6
        self._freq = protocol.TelloDdsProto.DDS_FREQ

    def Imu_info(self):
        return self._vgx, self._vgy, self._vgz, self._agx, self._agy, self._agz

    def data_info(self):
        return self._vgx, self._vgy, self._vgz, self._agx, self._agy, self._agz

    def decode(self, buf):
        push_info = buf.split(';')
        found_info_num = 0
        for info in push_info:
            if protocol.TelloDdsProto.DDS_VGX_FLAG in info:
                vgx_str = info.split(':')[1]
                self._vgx = float(vgx_str)
                found_info_num += 1
            elif protocol.TelloDdsProto.DDS_VGY_FLAG in info:
                vgy_str = info.split(':')[1]
                self._vgy = float(vgy_str)
                found_info_num += 1
            elif protocol.TelloDdsProto.DDS_VGZ_FLAG in info:
                vgz_str = info.split(':')[1]
                self._vgz = float(vgz_str)
                found_info_num += 1
            elif protocol.TelloDdsProto.DDS_AGX_FLAG in info:
                agx_str = info.split(':')[1]
                self._agx = float(agx_str)
                found_info_num += 1
            elif protocol.TelloDdsProto.DDS_AGY_FLAG in info:
                agy_str = info.split(':')[1]
                self._agy = float(agy_str)
                found_info_num += 1
            elif protocol.TelloDdsProto.DDS_AGZ_FLAG in info:
                agz_str = info.split(':')[1]
                self._agz = float(agz_str)
                found_info_num += 1

        if found_info_num == self._info_num:
            return True
        else:
            logger.debug("TelloImuInfoSubject: decode, found_info_num {0} is not match self._info_num {1}".format(
                found_info_num, self._info_num))
            return False

    @property
    def freq(self):
        return self._freq

    @freq.setter
    def freq(self, in_freq):
        if in_freq == 1 or in_freq == 5 or in_freq == 10:
            self._freq = in_freq


class Flight:
    """ 教育无人机 飞行器模块 """
    _cmd_label = random.randint(0, 99)
    _retry_times = 5

    def __init__(self, robot):
        self._client = robot.client
        self._action_dispatcher = robot.action_dispatcher
        self._robot = robot

    def takeoff(self, retry=True):
        """ 自动起飞

        :param: retry: bool:是否重发命令
        :return: action对象
        """
        cmd = "takeoff"
        if retry is False:
            flight_action = FlightAction(cmd)
            self._action_dispatcher.send_action(flight_action)
        else:
            for i in range(1, self._retry_times + 1):
                re_cmd = "Re{0:0>2d}{1:0>2d} ".format(self._cmd_label % 100, i) + cmd
                flight_action = FlightAction(re_cmd)
                self._action_dispatcher.send_action(flight_action)
            self._cmd_label += 1
        return flight_action

    def land(self, retry=True):
        """ 自动降落

        :param: retry: bool:是否重发命令
        :return: action对象
        """
        cmd = "land"
        if retry is False:
            flight_action = FlightAction(cmd)
            self._action_dispatcher.send_action(flight_action)
        else:
            for i in range(1, self._retry_times + 1):
                re_cmd = "Re{0:0>2d}{1:0>2d} ".format(self._cmd_label % 100, i) + cmd
                flight_action = FlightAction(re_cmd)
                self._action_dispatcher.send_action(flight_action)
            self._cmd_label += 1
        return flight_action

    def up(self, distance=0, retry=True):
        """ 向上飞distance厘米，指相对距离

        :param: distance: float:[20, 500]向上飞行的相对距离，单位 cm
        :param: retry: bool:是否重发命令
        :return: action对象
        """
        return self.fly(UP, distance, retry)

    def down(self, distance=0, retry=True):
        """ 向下飞distance厘米，指相对距离

        :param: distance: float:[20, 500]向下飞行的相对距离，单位 cm
        :param: retry: bool:是否重发命令
        :return: action对象
        """
        return self.fly(DOWN, distance, retry)

    def forward(self, distance=0, retry=True):
        """ 向前飞行distance厘米，指相对距离

        :param: distance: float:[20, 500]向前飞行的相对距离，单位 cm
        :param: retry: bool:是否重发命令
        :return: action对象
        """
        return self.fly(FORWARD, distance, retry)

    def backward(self, distance=0, retry=True):
        """ 向后飞行distance厘米， 指相对距离

        :param: distance: float:[20, 500]向后飞行的相对距离，单位 cm
        :param: retry: bool:是否重发命令
        :return: action对象
        """
        return self.fly(BACKWARD, distance, retry)

    def left(self, distance=0, retry=True):
        """ 向左飞行distance厘米， 指相对距离

        :param: distance: float:[20, 500]向左飞行的相对距离，单位 cm
        :param: retry: bool:是否重发命令
        :return: action对象
        """
        return self.fly(LEFT, distance, retry)

    def right(self, distance=0, retry=True):
        """ 向右飞行distance厘米， 指相对距离

        :param: distance: float:[20, 500]向右飞行的相对距离，单位 cm
        :param: retry: bool:是否重发命令
        :return: action对象
        """
        return self.fly(RIGHT, distance, retry)

    def fly(self, direction=FORWARD, distance=0, retry=True):
        """ 控制飞机向指定方向飞行指定距离。

        :param: direction: string: 飞行的方向，"forward" 向上飞行， "back" 向下飞行， "up" 向上飞行，
                                    "down" 向下飞行， "left" 向左飞行， "right" 向右飞行
        :param: distance: float:[20, 500]，飞行的距离，单位 cm
        :param: retry: bool:是否重发命令
        :return: action对象
        """
        # TODO check cmd.
        if retry is False:
            cmd = "{0} {1}".format(direction, distance)
            flight_action = FlightAction(cmd)
            self._action_dispatcher.send_action(flight_action)
        else:
            for i in range(1, self._retry_times + 1):
                cmd = "Re{0:0>2d}{1:0>2d} {2} {3}".format(self._cmd_label % 100, i, direction, distance)
                flight_action = FlightAction(cmd)
                self._action_dispatcher.send_action(flight_action)
            self._cmd_label += 1
        return flight_action

    def rotate(self, angle=0, retry=True):
        """ 控制飞机旋转指定角度

        :param: angle: float:[-360, 360] 旋转的角度，俯视飞机时，顺时针为正角度，逆时针为负角度
        :param: retry: bool:是否重发命令
        :return: action对象
        """
        if angle >= 0:
            direction = "cw"
        else:
            direction = "ccw"
            angle = -angle

        if retry is False:
            cmd = "{0} {1}".format(direction, angle)
            flight_action = FlightAction(cmd)
            self._action_dispatcher.send_action(flight_action)
        else:
            for i in range(1, self._retry_times + 1):
                cmd = "Re{0:0>2d}{1:0>2d} {2} {3}".format(self._cmd_label % 100, i, direction, angle)
                flight_action = FlightAction(cmd)
                self._action_dispatcher.send_action(flight_action)
            self._cmd_label += 1
        return flight_action

    def flip_forward(self, retry=True):
        """ 控制飞机向前翻滚

        当电量低于50%时无法完成翻滚
        :param: retry: bool:是否重发命令
        :return: action对象
        """
        return self.flip("f", retry)

    def flip_backward(self, retry=True):
        """ 控制飞机向后翻滚

        当电量低于50%时无法完成翻滚
        :param: retry: bool:是否重发命令
        :return: action对象
        """
        return self.flip("b", retry)

    def flip_left(self, retry=True):
        """ 控制飞机向左翻滚

        当电量低于50%时无法完成翻滚
        :param: retry: bool:是否重发命令
        :return: action对象
        """
        return self.flip("l", retry)

    def flip_right(self, retry=True):
        """ 控制飞机向右翻滚

        当电量低于50%时无法完成翻滚
        :param: retry: bool:是否重发命令
        :return: action对象
        """
        return self.flip("r", retry)

    def flip(self, direction="f", retry=True):
        """ 控制飞机向指定方向翻滚

        当电量低于50%时无法完成翻滚
        :param direction: string: 飞机翻转的方向， ’l‘ 向左翻滚，’r‘ 向右翻滚，’f‘ 向前翻滚， ’b‘ 向后翻滚
        :param: retry: bool:是否重发命令
        :return: action对象
        """
        cmd = "flip {0}".format(direction)
        if retry is False:
            flight_action = FlightAction(cmd)
            self._action_dispatcher.send_action(flight_action)
        else:
            for i in range(1, self._retry_times + 1):
                re_cmd = "Re{0:0>2d}{1:0>2d} ".format(self._cmd_label % 100, i) + cmd
                flight_action = FlightAction(re_cmd)
                self._action_dispatcher.send_action(flight_action)
            self._cmd_label += 1
        return flight_action

    def throw_fly(self):
        """ 控制飞机抛飞

        :return: action对象
        """
        cmd = "throwfly"
        flight_action = FlightAction(cmd)
        self._action_dispatcher.send_action(flight_action)
        return flight_action

    def go(self, x, y, z, speed=10, mid=None, retry=True):
        """ 控制飞机以设置速度飞向指定坐标位置

        注意， x,y,z 同时在-20~20时，飞机不会运动。当不使用挑战卡时，飞机所在位置为坐标系原点，飞机的前方为x轴正方向，飞机的左方为y轴的正方向

        :param: x: float: [-500, 500] x轴的坐标，单位 cm
        :param: y: float: [-500, 500] y轴的坐标，单位 cm
        :param: z: float: [-500, 500] z轴的坐标，单位 cm
        :param: speed: float: [10, 100] 运动速度， 单位 cm/s
        :param: mid: string: 不使用挑战卡时mid为None，运动坐标系为飞机自身坐标系；当使用挑战卡时mid为对应挑战卡编号，
                            运动坐标系为指定挑战卡的坐标系。支持编号可参考挑战卡使用说明。
        :param: retry: bool:是否重发命令
        :return: action对象
        """
        cmd = "go {0} {1} {2} {3}".format(x, y, z, speed)
        if mid:
            cmd += " {0}".format(mid)

        if retry is False:
            flight_action = FlightAction(cmd)
            self._action_dispatcher.send_action(flight_action)
        else:
            for i in range(1, self._retry_times + 1):
                re_cmd = "Re{0:0>2d}{1:0>2d} ".format(self._cmd_label % 100, i) + cmd
                flight_action = FlightAction(re_cmd)
                self._action_dispatcher.send_action(flight_action)
            self._cmd_label += 1
        return flight_action

    def move(self, x=0, y=0, z=0, speed=10, mid=None, retry=True):
        """ 飞机相对位置的控制

        x/y/z值不能同时在-20~20之间，适用该接口时应当先打开挑战卡检测功能

        :param: x: float:[-500, 500]，目标位置在挑战卡坐标系中的x坐标，实际取值范围要根据挑战卡大小调整，单位 cm
        :param: y: float:[-500, 500]，目标位置在挑战卡坐标系中的y坐标，实际取值范围要根据挑战卡大小调整，单位 cm
        :param: z: float:[-500, 500]，目标位置在挑战卡坐标系中的z坐标，实际取值范围要根据挑战卡大小调整，单位 cm
        :param: speed: int:[10, 100]，运动速度，单位 cm/s
        :param: mid: string: 挑战卡的编号，支持编号可参考挑战卡使用说明
        :param: retry: bool:是否重发命令
        :return: action对象
        """
        if mid:
            proto = protocol.TelloDdsProto
            pad_pos_x = self._robot.get_status(proto.DDS_PAD_X_FLAG)
            pad_pos_y = self._robot.get_status(proto.DDS_PAD_Y_FLAG)
            pad_pos_z = self._robot.get_status(proto.DDS_PAD_Z_FLAG)
            logger.info("Flight: moveto now position x {0} y {1} z {2} move to x {3}  y{4} z {5}".format(
                pad_pos_x, pad_pos_y, pad_pos_z, pad_pos_x + x, pad_pos_y + y, pad_pos_z + z))
            x = pad_pos_x + x
            y = pad_pos_y + y
            z = pad_pos_z + z
            return self.go(x, y, z, speed, mid, retry)
        else:
            logger.error("Flight: move, mid is None")
            return None

    def moveto(self, yaw=0, retry=True):
        """ 控制飞机旋转到挑战卡坐标系中指定的绝对角度

        :param: yaw: float:[-180, 180]，飞机在挑战卡上的的角度，俯视时，顺时针为正角度，逆时针为负角度
        :param: retry: bool:是否重发命令
        :return: action 对象
        """
        _, pad_yaw, _ = self._robot.get_status(protocol.TelloDdsProto.DDS_PAD_MPRY_FLAG)
        # 挑战卡上测试得到yaw轴逆时针为正，为保持与rotate接口的的一致性所以这里需要取反
        pad_yaw = -pad_yaw
        angle_diff = (yaw - pad_yaw)
        logger.debug("Flight: moveto, angle_diff {0}".format(angle_diff))
        logger.info("Flight: moveto, now pad-angle {0} rotate to {1}".format(pad_yaw, yaw))
        return self.rotate(angle_diff, retry)

    def rc(self, a=0, b=0, c=0, d=0):
        """ 控制飞机遥控器的四个杆量

        :param a: float:[-100, 100] 横滚
        :param b: float:[-100, 100] 俯仰
        :param c: float:[-100, 100] 油门
        :param d: float:[-100, 100] 偏航
        """
        cmd = "rc {0} {1} {2} {3}".format(a, b, c, d)
        proto = protocol.TextProtoDrone()
        proto.text_cmd = cmd
        msg = protocol.TextMsg(proto)
        try:
            self._client.send_async_msg(msg)
        except Exception as e:
            logger.warning("Drone: set rc, send_sync_msg exception {0}".format(str(e)))

    def curve(self, x1=0, y1=0, z1=0, x2=0, y2=0, z2=0, speed=20, mid=None, retry=True):
        """ 以设置速度飞弧线，经过对应坐标系中的(x1, y1, z1)点到（x2, y2, z2）点

        如果选用mid参数，则对应坐标系为指定挑战卡的坐标系。不使用挑战卡时，飞机的前方为x轴正方向，飞机的左方为y轴的正方向
        如果mid参数为默认值None,则为飞机自身坐标系

        :param: x1: float:[-500, 500] x轴坐标
        :param: y1: float:[-500, 500] y轴坐标
        :param: z1: float:如果使用挑战卡（mid不为None），取值范围为 [0, 500]; 如果不使用挑战卡（mid为None），取值范围为[-500, 500]
        :param: x2: float:[-500, 500] x轴坐标
        :param: y2: float:[-500, 500] y轴坐标
        :param: z2: float:如果使用挑战卡（mid不为None），取值范围为 [0, 500]; 如果不使用挑战卡（mid为None），取值范围为[-500, 500]
        :param: speed: float:[10, 60] 飞行的速度
        :param: mid: string: 不使用挑战卡时mid为None，运动坐标系为飞机自身坐标系；当使用挑战卡时mid为对应挑战卡编号，运动坐标系为对应挑战卡
                            坐标系。挑战卡编号参考挑战卡使用说明
        :param: retry: bool:是否重发命令
        :return: action对象
        """
        cmd = ""
        if mid:
            cmd = "curve {0} {1} {2} {3} {4} {5} {6} {7}".format(
                x1, y1, z1, x2, y2, z2, speed, mid)
        else:
            cmd = "curve {0} {1} {2} {3} {4} {5} {6}".format(
                x1, y1, z1, x2, y2, z2, speed)

        if retry is False:
            flight_action = FlightAction(cmd)
            self._action_dispatcher.send_action(flight_action)
        else:
            for i in range(1, self._retry_times + 1):
                re_cmd = "Re{0:0>2d}{1:0>2d} ".format(self._cmd_label % 100, i) + cmd
                flight_action = FlightAction(re_cmd)
                self._action_dispatcher.send_action(flight_action)
            self._cmd_label += 1
        return flight_action

    def stop(self, retry=True):
        """ 停止rc运动并悬停，任何时候都可以

        :param: retry: bool:是否重发命令
        :return: bool: 控制结果
        """
        cmd = "stop"
        if retry is False:
            flight_action = FlightAction(cmd)
            self._action_dispatcher.send_action(flight_action)
        else:
            for i in range(1, self._retry_times + 1):
                re_cmd = "Re{0:0>2d}{1:0>2d} ".format(self._cmd_label % 100, i) + cmd
                flight_action = FlightAction(re_cmd)
                self._action_dispatcher.send_action(flight_action)
            self._cmd_label += 1
        return flight_action

    def jump(self, x=0, y=0, z=0, speed=20, yaw=0, mid1='m-1', mid2='m-1', retry=True):
        """ 飞行器飞往mid1坐标系的(x, y, z)点后悬停，识别mid2的挑战卡，飞到mid2坐标系下(0, 0, z)的位置并且旋转到设定的yaw值

        :param: x: float: [-500, 500]，x轴的坐标，单位 cm
        :param: y: float: [-500, 500]，y轴的坐标，单位 cm
        :param: z: float: [0, 500]，z轴的坐标，单位 cm
        :param: speed: float:[10, 60]，飞行的速度, 单位 cm/s
        :param: yaw: [-360, 360] 最终悬停的yaw轴角度, 单位 °
        :param: mid1: string: 第一个挑战卡的id, 挑战卡id的介绍参考挑战卡使用说明
        :param: mid2: string: 第一个挑战卡的id, 挑战卡id的介绍参考挑战卡使用说明
        :param: retry: bool:是否重发命令
        :return: action对象
        """
        cmd = "jump {0} {1} {2} {3} {4} {5} {6}".format(x, y, z, speed, yaw, mid1, mid2)

        if retry is False:
            flight_action = FlightAction(cmd)
            self._action_dispatcher.send_action(flight_action)
        else:
            for i in range(1, self._retry_times + 1):
                re_cmd = "Re{0:0>2d}{1:0>2d} ".format(self._cmd_label % 100, i) + cmd
                flight_action = FlightAction(re_cmd)
                self._action_dispatcher.send_action(flight_action)
            self._cmd_label += 1
        return flight_action

    def set_speed(self, speed=0):
        """ 设置当前飞行速度

        :param speed: float:[10, 100]，飞行速度，单位 cm/s
        :return: bool: 设置结果
        """
        cmd = "speed {0}".format(speed)
        proto = protocol.TextProtoDrone()
        proto.text_cmd = cmd
        msg = protocol.TextMsg(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                if proto:
                    if proto.resp == "ok":
                        return True
                    else:
                        logger.warning("Flight: set_speed, resp {0}".format(proto.resp))
                        return False
                else:
                    return False
            else:
                logger.warning("Drone: set_speed failed.")
        except Exception as e:
            logger.warning("Drone: set_speed, send_sync_msg exception {0}".format(str(e)))
            return False

    def mission_pad_on(self):
        """ 打开挑战卡探测

        默认同时打开前视和下视探测
        :return: bool: 控制结果
        """
        return self._pad_detection(1)

    def mission_pad_off(self):
        """ 关闭挑战卡探测

        :return: bool:控制结果
        """
        return self._pad_detection(0)

    def _pad_detection(self, on_off=1):
        """  挑战卡检测功能开启/关闭的底层控制接口

        :param on_off: int:[0, 1], 0 关闭挑战卡检测功能，1 打开挑战卡检测功能
        :return: bool: 控制结果
        """
        cmd = ""
        if on_off == 1:
            cmd = "mon"
        elif on_off == 0:
            cmd = "moff"
        proto = protocol.TextProtoDrone()
        proto.text_cmd = cmd
        msg = protocol.TextMsg(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                if proto:
                    if proto.resp == "ok":
                        return True
                    else:
                        logger.warning("Flight: _pad_detection, resp {0}".format(proto.resp))
                        return False
                else:
                    return False
            else:
                logger.warning("Drone: _pad_detection failed.")
        except Exception as e:
            logger.warning("Drone: _pad_detection, send_sync_msg exception {0}".format(str(e)))
            return False

    def motor_on(self):
        """ 控制飞机转桨

        :return: action对象
        """
        cmd = "motoron"
        flight_action = FlightAction(cmd)
        self._action_dispatcher.send_action(flight_action)
        return flight_action

    def motor_off(self):
        """ 控制飞机停桨

        :return: action对象
        """
        cmd = "motoroff"
        flight_action = FlightAction(cmd)
        self._action_dispatcher.send_action(flight_action)
        return flight_action

    def get_speed(self):
        """ 获取当前设置速度

        :return: float: 当前速度值，单位 cm/s
        """
        cmd = "speed?"
        proto = protocol.TextProtoDrone()
        proto.text_cmd = cmd
        msg = protocol.TextMsg(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                if proto:
                    return float(proto.resp)
                else:
                    return None
            else:
                logger.warning("Drone: get_speed failed.")
        except Exception as e:
            logger.warning("Drone: get_speed, send_sync_msg exception {0}".format(str(e)))
            return None

    def sub_attitude(self, freq=5, callback=None, *args, **kw):
        """ 订阅飞机姿态信息

        :param freq: enum:(1, 5, 10)，订阅数据的频率
        :param callback: 传入数据处理的回掉函数
        :param args: 回调函数参数
        :param kw: 回调函数参数
        :return: bool: 数据订阅结果
        """
        sub = self._robot.dds
        subject = TelloAttiInfoSubject()
        subject.freq = freq
        return sub.add_subject_info(subject, callback, args, kw)

    def unsub_attitude(self):
        """ 取消订阅飞机姿态信息

        :return: bool: 取消数据订阅结果
        """
        sub_dds = self._robot.dds
        return sub_dds.del_subject_info(dds.DDS_TELLO_ATTITUDE)

    def sub_imu(self, freq=5, callback=None, *args, **kw):
        """ 订阅飞机陀螺仪信息

        :param freq: enum:(1, 5, 10)，订阅数据的频率
        :param callback: 传入数据处理的回掉函数
        :param args: 回调函数参数
        :param kw: 回调函数参数
        :return: bool: 数据订阅结果
        """
        sub = self._robot.dds
        subject = TelloImuInfoSubject()
        subject.freq = freq
        return sub.add_subject_info(subject, callback, args, kw)

    def unsub_imu(self):
        """ 取消订阅飞机陀螺仪信息

        :return: bool: 取消数据订阅结果
        """
        sub_dds = self._robot.dds
        return sub_dds.del_subject_info(dds.DDS_TELLO_IMU)
