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


import time
from robomaster import action
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


class MultiDroneModule(MultiModule):
    """ Tello module """

    def __init__(self, robot_group, module_name):
        super().__init__(robot_group, module_name)

    def get_battery(self):
        """ 获取电池电量

        :return: dict: {robot_id, battery_info}
        """
        return self.execute_command('get_battery')

    def takeoff(self, *args, **kw):
        """for tello

        :param args:
        :return:
        """
        return self.execute_action('takeoff', *args, **kw)

    def land(self, *args, **kw):
        """ for tello

        :param args:
        :return:
        """
        return self.execute_action('land', *args, **kw)

    def up(self, *args, **kw):
        """for tello

        :param args:
        :return:
        """
        return self.execute_action('up', *args, **kw)

    def down(self, *args, **kw):
        """for tello

        :param args:
        :return:
        """
        return self.execute_action('down', *args, **kw)

    def forward(self, *args, **kw):
        """for tello

        :param args:
        :return:
        """
        return self.execute_action('forward', *args, **kw)

    def backward(self, *args, **kw):
        """for tello

        :param args:
        :return:
        """
        return self.execute_action('backward', *args, **kw)

    def left(self, *args, **kw):
        """for tello

        :param args:
        :return:
        """
        return self.execute_action('left', *args, **kw)

    def right(self, *args, **kw):
        """for tello

        :param args:
        :return:
        """
        return self.execute_action('right', *args, **kw)

    def rotate(self, *args, **kw):
        """

        :return:
        """
        return self.execute_action('rotate', *args, **kw)

    def flip_forward(self, *args, **kw):
        """ for tello

        :param args:
        :return:
        """
        return self.execute_action('flip_forward', *args, **kw)

    def flip_backward(self, *args, **kw):
        """ for tello

        :param args:
        :return:
        """
        return self.execute_action('flip_backward', *args, **kw)

    def flip_left(self, *args, **kw):
        """ for tello

        :param args:
        :return:
        """
        return self.execute_action('flip_left', *args, **kw)

    def flip_right(self, *args, **kw):
        """ for tello

        :param args:
        :return:
        """
        return self.execute_action('flip_right', *args, **kw)

    def mission_pad_on(self, *args, **kw):
        """ for tello

        :param args:
        :return:
        """
        return self.execute_action('mission_pad_on', *args, **kw)

    def mission_pad_off(self, *args, **kw):
        """ for tello

        :param args:
        :return:
        """
        return self.execute_action('mission_pad_off', *args, **kw)

    def go(self, go_dict):
        """ for tello

        :param args: go_dict: {[robot_id1: x1, y1, z1, speed1, mid1],
                               [robot_id1: x1, y1, z1, speed1, mid1],
                               ... }
        :return:
        """
        action_dict = {}
        if len(go_dict) != self._robot_group.robots_num:
            logger.error("MultiDroneModule: go, the inputs robots num does not match the actual robots number in group")
            raise Exception("Input robots number is not match!")
        for robot_id, go_params in go_dict.items():
            if robot_id not in self._robot_group._robots_id_in_group_list:
                logger.error("MultiDroneModule: go, there is not robot_id {0} in group!".format(robot_id))
                raise Exception("There is not robot_id {0} in group!".format(robot_id))
            robot_obj = self._robot_group.get_robot(robot_id)
            action = robot_obj.flight.go(*go_params)
            action_dict[robot_id] = action
        multi_action = MultiAction(action_dict)
        return multi_action

    def motor_on(self, *args, **kw):
        """ for tello

        :param args:
        :return:
        """
        return self.execute_action('motor_on', *args, **kw)

    def motor_off(self, *args, **kw):
        """ for tello

        :param args:
        :return:
        """
        return self.execute_action('motor_off', *args, **kw)

    def set_led(self, *args, **kw):
        """ 扩展模块led的灯光颜色

        :param args:
        :param kw:
        :return:
        """
        return self.execute_command("set_led", *args, **kw)

    def set_led_breath(self, *args, **kw):
        """ 扩展模块led呼吸

        :param args:
        :param kw:
        :return:
        """
        return self.execute_command("set_led_breath", *args, **kw)

    def set_led_blink(self, *args, **kw):
        """ 扩展模块led灯闪烁

        :return: bool: 设置结果
        """
        return self.execute_command('set_led_blink', *args, **kw)

    def set_mled_bright(self, *args, **kw):
        """ 扩展模块点阵屏亮度

        :return: bool: 设置结果
        """
        return self.execute_command('set_mled_bright', *args, **kw)

    def set_mled_boot(self, *args, **kw):
        """ 扩展模块点阵屏开机画面

        :return: bool: 设置结果
        """
        return self.execute_command('set_mled_boot', *args, **kw)

    def set_mled_sc(self, *args, **kw):
        """ 清除扩展模块点阵屏开机画面

        :return: bool: 设置结果
        """
        return self.execute_command('set_mled_sc', *args, **kw)

    def set_mled_char(self, *args, **kw):
        """ 控制扩展点阵屏模块，显示输入的字符

        :return: bool: 设置结果
        """
        return self.execute_command('set_mled_char', *args, **kw)

    def set_mled_graph(self, *args, **kw):
        """ 扩展模块点阵屏显示自定义图案

        :return: bool: 设置结果
        """
        return self.execute_command('set_mled_graph', *args, **kw)

    def set_mled_char_scroll(self, *args, **kw):
        """ 控制扩展点阵屏滚动显示字符串

        :param args:
        :param kw:
        :return:
        """
        return self.execute_command("set_mled_char_scroll", *args, **kw)

    def set_mled_graph_scroll(self, *args, **kw):
        """ 控制扩展点阵屏滚动显示图像

        :param args:
        :param kw:
        :return:
        """
        return self.execute_command("set_mled_graph_scroll", *args, **kw)
