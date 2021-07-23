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


import copy
import time
import threading
from robomaster import action
from robomaster import flight
from robomaster import led
from . import logger
from . import tool

ROBOT_ID = 0
ROBOT_OBJ = 1
ROBOT_ACTION = 1


class MultiAction(object):
    """Action manager for multi robots"""

    def __init__(self, robots_action_dict):
        self._robots_action_dict = robots_action_dict  # key robot_id, value action.

    def wait_for_completed(self, timeout=8):
        """Wait for all robots to complete their actions

        :param timeout: Add up the wait times for all the cars.
        :return: True: action has completed, False: wait timeout.
        """
        if not self._robots_action_dict:
            logger.error("MultiAction: no action is waiting")
            return False
        robot_id_executing = []  # dictionary can`t change size during iteration, so use list
        start_time = time.time()
        spent_time = 0
        final_result = False
        for robot_id in self._robots_action_dict.keys():
            robot_id_executing.append(robot_id)
        logger.info(
            "MultiAction: Group action start waiting for completed, {0}".format(
                self._robots_action_dict[robot_id_executing[0]]))
        while spent_time < timeout:
            cur_time = time.time()
            spent_time = cur_time - start_time
            if not robot_id_executing:
                logger.info("MultiAction: wait_for_all_completed. All of robots are completed")
                final_result = True
                break
            for robot_id, robot_action in self._robots_action_dict.items():
                if self._robots_action_dict[robot_id].is_completed and (robot_id in robot_id_executing):
                    action_key = self._robots_action_dict[robot_id].make_action_key()
                    in_progress_list = self._robots_action_dict[robot_id]._obj._in_progress
                    # make sure the action has been removed form _in_progress
                    if action_key not in in_progress_list:
                        robot_id_executing.remove(robot_id)
                        logger.info(
                            "MultiAction: wait_for_all_completed. Robot id ({0}) action is completed, "
                            "action: {1}".format(robot_id, self._robots_action_dict[robot_id]))
            time.sleep(0.05)
        # timeout
        if not final_result:
            for robot_id, robot_action in self._robots_action_dict.items():
                if not robot_action.is_completed:
                    robot_action._changeto_state(action.ACTION_EXCEPTION)
                    logger.warning(
                        "MultiAction: wait_for_all_completed, timeout! Robot id {}, action {}".format(
                            robot_id, self._robots_action_dict[robot_id]))
        else:
            # each robot has completed its action
            logger.info("MultiAction: wait for all completed successfully, action {0}".format(self._robots_action_dict))
        return final_result


class TelloDispatcher(object):

    def __init__(self, client, event, _robot_host_dict):
        self._client = client
        self.event = event
        self._robot_host_dict = _robot_host_dict
        self._action_host_list = []
        self.cur_action = ""
        self.special = None

    @property
    def action_host_list(self):
        return self._action_host_list

    @action_host_list.setter
    def action_host_list(self, value):
        self._action_host_list = value

    def wait_for_completed(self, timeout=10):
        _queue = self._client.queue
        _action_host_list = copy.copy(self._action_host_list)
        tello_status = tool.TelloStatus(self.cur_action)
        cur_time = time.time()
        while len(_action_host_list) != 0:
            if time.time()-cur_time > timeout:
                logger.warning("action: {} ,timeout".format(self.cur_action))
                break
            qsize = _queue.qsize()
            for i in range(qsize):
                # todo 多group并行有可能会因为队列为空而出错，需要加锁
                if _queue.empty():
                    break
                proto = _queue.get()
                time.sleep(0.01)
                # todo 需要补全 ERROR LIST
                if proto.text in tello_status.FLIGHT_ACTION_SET:
                    #  FLIGHT respond
                    if proto.host in _action_host_list:
                        tello_status.judge(proto)
                        _action_host_list.remove(proto.host)
                    else:
                        _queue.put(proto)
                elif proto.text in tello_status.EXT_ACTION_SET:
                    # EXT respond
                    if proto.host in _action_host_list:
                        tello_status.judge(proto)
                        _action_host_list.remove(proto.host)
                    else:
                        _queue.put(proto)
                else:
                    # DRONE respond
                    if proto.host in _action_host_list:
                        tello_status.judge(proto)
                        _action_host_list.remove(proto.host)
                        id_ = self._robot_host_dict[proto.host]
                        logger.info("DRONE id: {}, reply: {}".format(id_, proto.text))
                        print("DRONE id: {}, reply: {}".format(id_, proto.text))   # output to console
                    else:
                        _queue.put(proto)
        if self.special == "takeoff":
            while not _queue.empty():
                _ = _queue.get()    # drone bug: takeoff reply double ok
        logger.info("wait_for_completed: finished")
        self.event.set()
        return self


class MultiModule(object):
    """ multi-robot`s module object"""

    def __init__(self, robot_group, module_name):
        self._robot_group = robot_group
        self._module_name = module_name
        self._current_action_name = None

    @property
    def name(self):
        return self._module_name

    def execute_action(self, action_name, *args, **kw):
        """Executive function for non-instantaneous action
        that have 'wait_for_all_completion()'.

        :param action_name: which action need exec
        :param args: the action params
        :param args: the action key params
        :return:
        """
        action_dict = {}
        for robot_id in self._robot_group._robots_id_in_group_list:
            robot_module = self._robot_group.all_robots_dict[robot_id].get_module(self._module_name)
            action_dict[robot_id] = getattr(robot_module, action_name)(*args, **kw)
            logger.info("Multi Module robot id {0}: begin to execute the action".format(robot_id))
        multi_action = MultiAction(action_dict)
        return multi_action

    def execute_command(self, command_name, *input_args, **input_kw):
        """Executive function for instantaneous action
        that do not have 'wait_for_all_completion()'.

        :param command_name: which command need send
        :param args: the command params
        :return:
        """
        start_time = time.time()
        thread_dict = {}  # {robot_id: thread}
        result_dict = {}  # {robot_id: result, ... }
        for robot_id in self._robot_group._robots_id_in_group_list:
            robot_module = self._robot_group.all_robots_dict[robot_id].get_module(self._module_name)
            exec_cmd_thread = tool.TelloThread(getattr(robot_module, command_name), *input_args, **input_kw)
            thread_dict[robot_id] = exec_cmd_thread
        second_time = time.time()
        # start threads
        for robot_id, thread_obj in thread_dict.items():
            thread_obj.start()
        logger.debug("send command start spend time {0}".format(time.time() - second_time))
        for robot_id, exec_cmd_thread in thread_dict.items():
            exec_cmd_thread.join()
            result_dict[robot_id] = exec_cmd_thread.get_result()
        spend_time = time.time() - start_time
        logger.debug("send command spend time {0}".format(spend_time))
        logger.debug("RobotGroupBase: execute_command, result {0}".format(result_dict))
        return result_dict


class MultiRmModule(MultiModule):
    """ Robomaster module """

    def __init__(self, robot_group, module_name):
        super().__init__(robot_group, module_name)

    """Only for gimbal"""

    def recenter(self, *args, **kw):
        """gimbal recenter

        :param args:
        :return:
        """
        return self.execute_action('recenter', *args, **kw)

    def suspend(self, *args, **kw):
        """gimbal suspend

        :param args:
        :return:
        """
        return self.execute_command('suspend', *args, **kw)

    def resume(self, *args, **kw):
        """gimbal resume

        :param args:
        :return:
        """
        return self.execute_command('resume', *args, **kw)

    """Only for chassis"""

    def drive_wheels(self, *args, **kw):
        """chassis drive wheels

        :param args:
        :return:
        """"""

        :param args:
        :return:
        """
        return self.execute_action('drive_wheels', *args, **kw)

    def drive_speed(self, *args, **kw):
        """chassis drive speed

        :param args:
        :return:
        """
        return self.execute_action('drive_wheels', *args, **kw)

    """Only for fire"""

    def fire(self, *args, **kw):
        """blaster fire

        :param args:
        :return:
        """
        return self.execute_command('fire', *args, **kw)

    """Share to multiple modules"""

    def move(self, *args, **kw):
        """gimbal & chassis move

        :param args:
        :return:
        """
        return self.execute_action('move', *args, **kw)

    def moveto(self, *args, **kw):
        """gimbal & chassis moveto

        :param args:
        :return:
        """
        return self.execute_action('moveto', *args, **kw)

    def set_led(self, *args, **kw):
        """blaster & armor led

        :param args:
        :return:
        """
        return self.execute_command('set_led', *args, **kw)

    """Only for gripper"""

    def close(self, *args, **kw):
        """gripper

        :param args:
        :return:
        """
        return self.execute_command('close', *args, **kw)

    def open(self, *args, **kw):
        """gripper

        :param args:
        :return:
        """
        return self.execute_command('open', *args, **kw)

    def pause(self):
        """gripper

        :param args:
        :return:
        """
        return self.execute_command('pause')


class TelloAction(object):

    def __init__(self, client, _robot_id_dict, _robot_sn_dict, _robot_host_dict):
        self._client = client
        self._robot_id_dict = _robot_id_dict
        self._robot_sn_dict = _robot_sn_dict
        self._robot_host_dict = _robot_host_dict
        self.event = threading.Event()
        self.event.set()
        self._dispatcher = TelloDispatcher(self._client, self.event, self._robot_host_dict)
        self.robot_group_host_list = []

    def action_group(self, robot_group):
        self.robot_group_host_list = robot_group.robot_group_host_list
        self._dispatcher.action_host_list = self.robot_group_host_list
        return self

    def send_command(self, command):
        self.event.wait(10)
        if self.event.isSet():
            for host in self.robot_group_host_list:
                logger.info("execute command：{}".format(command))
                proto = tool.TelloProtocol(command, host)
                self._client.send(proto)
            self.event.clear()
        else:
            self.event.set()
            logger.warning("execute command：{}, timeout".format(command))

    def send_custom_command(self, command_host_list, action="go"):
        self.event.wait(10)
        if self.event.isSet():
            for command_host in command_host_list:
                command, host = command_host
                logger.info("execute command：{}".format(command))
                proto = tool.TelloProtocol(command, host)
                self._client.send(proto)
            self.event.clear()
        else:
            self.event.set()
            logger.warning("execute command：{}, timeout".format(action))

    def get_sn(self):
        """ 获取sn

        :return: _dispatcher对象
        """
        cmd = "sn?"
        self.send_command(cmd)
        self._dispatcher.cur_action = cmd
        return self._dispatcher.wait_for_completed(10)

    def get_battery(self):
        """ 获取电量

        :return: _dispatcher对象
        """
        cmd = "battery?"
        self.send_command(cmd)
        self._dispatcher.cur_action = cmd
        return self._dispatcher.wait_for_completed(10)

    def takeoff(self, retry=True):
        """ 自动起飞

        :param: retry: bool:是否重发命令
        :return: _dispatcher对象
        """
        cmd = "takeoff"
        self.send_command(cmd)
        self._dispatcher.cur_action = cmd
        self._dispatcher.special = "takeoff"
        return self._dispatcher

    def land(self, retry=True):
        """ 自动降落

        :param: retry: bool:是否重发命令
        :return: _dispatcher对象
        """
        cmd = "land"
        self.send_command(cmd)
        self._dispatcher.cur_action = cmd
        return self._dispatcher

    def up(self, distance, retry=True):
        """ 向上飞distance厘米，指相对距离

        :param: distance: float:[20, 500]向上飞行的相对距离，单位 cm
        :param: retry: bool:是否重发命令
        :return: _dispatcher对象
        """
        return self.fly(flight.UP, distance, retry)

    def down(self, distance, retry=True):
        """ 向下飞distance厘米，指相对距离

        :param: distance: float:[20, 500]向下飞行的相对距离，单位 cm
        :param: retry: bool:是否重发命令
        :return: _dispatcher对象
        """
        return self.fly(flight.DOWN, distance, retry)

    def forward(self, distance, retry=True):
        """ 向前飞distance厘米，指相对距离

        :param: distance: float:[20, 500]向前飞行的相对距离，单位 cm
        :param: retry: bool:是否重发命令
        :return: _dispatcher对象
        """
        return self.fly(flight.FORWARD, distance, retry)

    def backward(self, distance, retry=True):
        """ 向后飞distance厘米，指相对距离

        :param: distance: float:[20, 500]向后飞行的相对距离，单位 cm
        :param: retry: bool:是否重发命令
        :return: _dispatcher对象
        """
        return self.fly(flight.BACKWARD, distance, retry)

    def left(self, distance, retry=True):
        """ 向左飞distance厘米，指相对距离

        :param: distance: float:[20, 500]向左飞行的相对距离，单位 cm
        :param: retry: bool:是否重发命令
        :return: _dispatcher对象
        """
        return self.fly(flight.LEFT, distance, retry)

    def right(self, distance, retry=True):
        """ 向右飞distance厘米，指相对距离

        :param: distance: float:[20, 500]向右飞行的相对距离，单位 cm
        :param: retry: bool:是否重发命令
        :return: _dispatcher对象
        """
        return self.fly(flight.RIGHT, distance, retry)

    def fly(self, _action, distance, retry):
        """ 控制飞机向指定方向飞行指定距离。

        :param: direction: string: 飞行的方向，"forward" 向上飞行， "back" 向下飞行， "up" 向上飞行，
                                    "down" 向下飞行， "left" 向左飞行， "right" 向右飞行
        :param: distance: float:[20, 500]，飞行的距离，单位 cm
        :param: retry: bool:是否重发命令
        :return: _dispatcher对象
        """
        cmd = "{0} {1}".format(_action, distance)
        self._dispatcher.cur_action = cmd
        self.send_command(cmd)
        return self._dispatcher

    def rotate(self, angle=0, retry=True):
        """ 控制飞机旋转指定角度

        :param: angle: float:[-360, 360] 旋转的角度，俯视飞机时，顺时针为正角度，逆时针为负角度
        :param: retry: bool:是否重发命令
        :return: _dispatcher对象
        """
        if angle >= 0:
            direction = "cw"
        else:
            direction = "ccw"
            angle = -angle

        cmd = "{0} {1}".format(direction, angle)
        self._dispatcher.cur_action = cmd
        self.send_command(cmd)
        return self._dispatcher

    def flip_forward(self, retry=True):
        """ 控制飞机向前翻滚

        当电量低于50%时无法完成翻滚
        :param: retry: bool:是否重发命令
        :return: _dispatcher对象
        """
        return self.flip("f", retry)

    def flip_backward(self, retry=True):
        """ 控制飞机向后翻滚

        当电量低于50%时无法完成翻滚
        :param: retry: bool:是否重发命令
        :return: _dispatcher对象
        """
        return self.flip("b", retry)

    def flip_left(self, retry=True):
        """ 控制飞机向左翻滚

        当电量低于50%时无法完成翻滚
        :param: retry: bool:是否重发命令
        :return: _dispatcher对象
        """
        return self.flip("l", retry)

    def flip_right(self, retry=True):
        """ 控制飞机向右翻滚

        当电量低于50%时无法完成翻滚
        :param: retry: bool:是否重发命令
        :return: _dispatcher对象
        """
        return self.flip("r", retry)

    def flip(self, direction="f", retry=True):
        """ 控制飞机向指定方向翻滚

        当电量低于50%时无法完成翻滚
        :param direction: string: 飞机翻转的方向， ’l‘ 向左翻滚，’r‘ 向右翻滚，’f‘ 向前翻滚， ’b‘ 向后翻滚
        :param: retry: bool:是否重发命令
        :return: _dispatcher对象
        """
        cmd = "flip {0}".format(direction)
        self._dispatcher.cur_action = cmd
        self.send_command(cmd)
        return self._dispatcher

    def go(self, go_dict):
        """ 控制飞机以设置速度飞向指定坐标位置

        :return: _dispatcher对象
        """
        self._dispatcher.cur_action = "go"
        if isinstance(go_dict, dict):
            cmd_formatter = "go {0} {1} {2} {3} {4}"
            self._custom_drone_command(go_dict, cmd_formatter)
        else:
            raise Exception("input type must be dict")
        return self._dispatcher

    def mission_pad_on(self):
        """ 开启视觉识别

        :return: _dispatcher对象
        """
        cmd = "mon"
        self._dispatcher.cur_action = cmd
        self.send_command(cmd)
        return self._dispatcher.wait_for_completed(0.5)

    def mission_pad_off(self):
        """ 关闭视觉识别

        """
        cmd = "moff"
        self._dispatcher.cur_action = cmd
        self.send_command(cmd)
        return self._dispatcher.wait_for_completed(0.5)

    def motor_on(self):
        """ 开启静置转桨

        :return: _dispatcher对象
        """
        cmd = "motoron"
        self._dispatcher.cur_action = cmd
        self.send_command(cmd)
        return self._dispatcher.wait_for_completed(0.5)

    def motor_off(self):
        """ 开启静置转桨

        """
        cmd = "motoroff"
        self._dispatcher.cur_action = cmd
        self.send_command(cmd)
        return self._dispatcher.wait_for_completed(0.5)

    def set_led(self, r=0, g=255, b=0, command_dict=None):
        """ 设置扩展模块led颜色

        :param r: int:[0, 255], 扩展led红色通道的强度
        :param g: int:[0, 255], 扩展led绿色通道的强度
        :param b: int:[0, 255], 扩展led蓝色通道的强度
        :param command_dict: dict, 多飞机的自定义显示
        :return:
        """
        self._dispatcher.cur_action = "EXT led"
        cmd_formatter = "EXT led {0} {1} {2}"
        if isinstance(command_dict, dict):
            self._custom_drone_command(command_dict, cmd_formatter)
        else:
            cmd = cmd_formatter.format(r, g, b)
            self.send_command(cmd)
        return self._dispatcher.wait_for_completed(0.5)

    def set_led_breath(self, freq=1, r=0, g=255, b=0, command_dict=None):
        """ 设置扩展模块led以指定的颜色与频率实现呼吸效果

        :param freq: int:[0.1, 2.5], 扩展led呼吸模式下的频率，共十档，随着数字增大速度变快
        :param r: int:[0, 255], 扩展led红色通道的强度
        :param g: int:[0, 255], 扩展led绿色通道的强度
        :param b: int:[0, 255], 扩展led蓝色通道的强度
        :param command_dict: dict, 多飞机的自定义显示
        :return:
        """
        self._dispatcher.cur_action = "EXT led br"
        cmd_formatter = "EXT led br {0} {1} {2} {3}"
        if isinstance(command_dict, dict):
            self._custom_drone_command(command_dict, cmd_formatter)
        else:
            cmd = cmd_formatter.format(freq, r, g, b)
            self.send_command(cmd)
        return self._dispatcher.wait_for_completed(0.5)

    def set_led_blink(self, freq=5, r1=0, g1=255, b1=0, r2=0, g2=255, b2=255, command_dict=None):
        """ 设置扩展模块led以制定的两种颜色与频率实现闪烁效果

        :param freq: int:[0.1, 10], 扩展ked闪烁模式下的频率， 共十档，随着数字增大速度变快
        :param r1: int:[0, 255], 第一种颜色的红色通道的强度
        :param g1: int:[0, 255], 第一种颜色的绿色通道的强度
        :param b1: int:[0, 255], 第一种颜色的蓝色通道的强度
        :param r2: int:[0, 255], 第二种颜色的红色通道的强度
        :param g2: int:[0, 255], 第二种颜色的绿色通道的强度
        :param b2: int:[0, 255], 第二种颜色的蓝色通道的强度
        :param command_dict: dict, 多飞机的自定义显示
        :return:
        """
        self._dispatcher.cur_action = "EXT led bl"
        cmd_formatter = "EXT led bl {0} {1} {2} {3} {4} {5} {6}"
        if isinstance(command_dict, dict):
            self._custom_drone_command(command_dict, cmd_formatter)
        else:
            cmd = cmd_formatter.format(freq, r1, g1, b1, r2, g2, b2)
            self.send_command(cmd)
        return self._dispatcher.wait_for_completed(0.5)

    def set_mled_bright(self, bright=255):
        """ 设置点阵屏的亮度

        :param bright: int:[0, 255] 点阵屏的亮度
        :return:
        """
        cmd = "EXT mled sl {0}".format(bright)
        self._dispatcher.cur_action = cmd
        self.send_command(cmd)
        return self._dispatcher.wait_for_completed(0.5)

    def set_mled_boot(self, display_graph):
        """ 设置点阵屏的开机画面

        :param display_graph: string: 长度最大为64，点阵屏显示图案的编码字符串，每个字符解读为二进制后对应位置的led点的状态，
        '0'为关闭该位置led，'r'为点亮红色，'b'为点亮蓝色，'p' 为点亮紫色，输入的长度不足64，后面对应的led点默认都是'0'熄灭状态
        :param command_dict: dict, 多飞机的自定义显示
        :return:
        """
        cmd = "EXT mled sg {0}".format(display_graph)
        self._dispatcher.cur_action = cmd
        self.send_command(cmd)
        return self._dispatcher.wait_for_completed(0.5)

    def set_mled_sc(self):
        """ 清除点阵屏开机显示画面

        :return:
        """
        cmd = "EXT mled sc"
        self._dispatcher.cur_action = cmd
        self.send_command(cmd)
        return self._dispatcher.wait_for_completed(0.5)

    def set_mled_char(self, color="r", display_char="0", command_dict=None):
        """ 控制扩展点阵屏模块，显示输入的字符

        :param: color: char: 'r'为红色，'b'为蓝色，'p' 为紫色
        :param: display_char: char: [0~9, A~F, heart]， 显示的字符
        :param command_dict: dict, 多飞机的自定义显示
        :return: bool:
        """
        self._dispatcher.cur_action = "EXT mled s"
        cmd_formatter = "EXT mled s {} {}"
        if isinstance(command_dict, dict):
            self._custom_drone_command(command_dict, cmd_formatter)
        else:
            cmd = cmd_formatter.format(color, display_char)
            self.send_command(cmd)
        return self._dispatcher.wait_for_completed(0.5)

    def set_mled_graph(self, display_graph, command_dict=None):
        """ 用户自定义扩展点阵屏显示图案

        :param display_graph: string: 长度最大为64，点阵屏显示图案的编码字符串，每个字符解读为二进制后对应位置的led点的状态，
        '0'为关闭该位置led，'r'为点亮红色，'b'为点亮蓝色，'p' 为点亮紫色，输入的长度不足64，后面对应的led点默认都是'0'熄灭状态
        :param command_dict: dict, 多飞机的自定义显示
        :return:bool:
        """
        self._dispatcher.cur_action = "EXT mled g"
        cmd_formatter = "EXT mled g {0}"
        if isinstance(command_dict, dict):
            self._custom_drone_command(command_dict, cmd_formatter)
        else:
            cmd = cmd_formatter.format(display_graph)
            self.send_command(cmd)
        return self._dispatcher.wait_for_completed(tool.EXT_TIMEOUT)

    def set_mled_char_scroll(self, direction='l', color='r', freq=1.5, display_str="DJI"):
        """ 控制扩展点阵屏滚动显示字符串

        :param: direction: char: 点阵屏滚动方向，'l': 字符串向左移动，'r': 字符串向右移动，'u' 字符串向上移动，'d' 字符串向下移动
        :param: color: char: 点阵屏显示的颜色， 'r'红色，'b'蓝色，'p'紫色
        :param: freq: float:[0.1, 2.5], 点阵屏滚动的频率, 0.1-2.5HZ之间, 随着数字增大速度变快
        :param: display_str: string:需要显示的字符串
        :return:
        """
        cmd = "EXT mled {0} {1} {2} {3} ".format(direction, color, freq, display_str)
        return self._set_mled_scroll(cmd)

    def set_mled_graph_scroll(self, direction='l', freq=1.5, display_graph=led.TELLO_DISPLAY_GRAPH):
        """ 控制扩展点阵屏滚动显示图像

        :param: direction: char: 点阵屏滚动方向，'l': 字符串向左移动，'r': 字符串向右移动，'u' 字符串向上移动，'d' 字符串向下移动
        :param: freq: float:[0.1, 2.5], 点阵屏滚动的频率, 0.1-2.5HZ之间, 随着数字增大速度变快
        :param: display_str: string:需要显示的图像
        :return:
        """
        cmd = "EXT mled {0} {1} {2} {3} ".format(direction, "g", freq, display_graph)
        return self._set_mled_scroll(cmd)

    def _set_mled_scroll(self, cmd):
        """ 控制扩展点阵屏滚动显示

        :return:
        """
        self._dispatcher.cur_action = cmd
        self.send_command(cmd)
        return self._dispatcher.wait_for_completed(0.5)

    def set_custom_text(self, text='', command_dict=None):
        cmd_formatter = "EXT {}"
        self.event.set()
        if isinstance(command_dict, dict):
            self._custom_drone_command(command_dict, cmd_formatter)
        else:
            cmd = cmd_formatter.format(text)
            self.send_command(cmd)

    def _custom_drone_command(self, command_dict, cmd_formatter):
        command_host_list = []
        if len(command_dict) != len(self.robot_group_host_list):
            logger.error(
                "TelloAction: go, the inputs robots num does not match the actual robots number in group")
            raise Exception("Input robots number is not match!")
        for _id, command in command_dict.items():
            sn = self._robot_id_dict[_id]
            host = self._robot_sn_dict[sn]
            if host not in self.robot_group_host_list:
                raise Exception("DRONE id: {0} does not exit in this group".format(_id))
            cmd = cmd_formatter.format(command)
            command_host_list.append([cmd, host])
        self.send_custom_command(command_host_list)
