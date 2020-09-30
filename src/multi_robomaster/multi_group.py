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
import threading
from . import multi_module
from . import logger
from . import tool


class RobotGroupBase(object):
    """robot group object"""

    def __init__(self, robots_group_list, all_robots_dict):
        # Input checking should be done in MultiRobot.build_group()
        self._robots_id_in_group_list = robots_group_list  # robot id list
        self._all_robots_dict = all_robots_dict  # all robots in MultiRobot
        self._group_modules_dict = {}  # the modules of RobotGroup. {name:module-obj, ... }

    def __del__(self):
        for module_name, module_obj in self._group_modules_dict.items():
            del module_obj
            logger.info(
                "RobotGroupBase: __del__ delete module: {}".format(module_name))

    def initialize(self):
        self._scan_group_module()

    def get_robot(self, robot_id):
        """Get robot by robot-id

        :param robot_id:
        :return:
        """
        return self._all_robots_dict[robot_id]

    @property
    def robots_num(self):
        return len(self._robots_id_in_group_list)

    @property
    def all_robots_dict(self):
        return self._all_robots_dict

    def _scan_group_module(self):
        pass

    def get_group_module(self, name):
        """Get group module by name

        :param name:
        :return:
        """
        get_result = True
        for robot_id in self._robots_id_in_group_list:
            if self._all_robots_dict[robot_id].get_module(name) is None:
                get_result = False
                logger.error(
                    "[MulitRobot] robot id {0}: the {1} module is not online".format(
                        robot_id, name))
        if get_result:
            logger.debug(
                "RobotGroup: get_group_module, group modules {0}".format(
                    self._group_modules_dict))
            return self._group_modules_dict[name]
        else:
            return None

    @property
    def robots_id_list(self):
        return self._robots_id_in_group_list

    def append(self, robots_id_list):
        """ Add robots to the group

        :param robots_id_list:
        :return:
        """
        check_result, robot_id = tool.check_robots_id(
            robots_id_list, self._all_robots_dict)
        if not check_result:
            raise Exception('Robot id %d is not exist' % robot_id)
        for robot_id in robots_id_list:
            if robot_id in self._robots_id_in_group_list:
                logger.warning(
                    "RobotGroupBase: robot id {0} is in group {1}".format(
                        robot_id, self._robots_id_in_group_list))
            else:
                self._robots_id_in_group_list.append(robot_id)
                logger.info(
                    "RobotGroupBase: robot id {0} has been added into  group {1}".format(
                        robot_id, self._robots_id_in_group_list))

    def remove(self, robots_id_list):
        """remove the robots from robot group

        :param robots_list: robots need to be remove
        :return:  True: successful, False: some robot are not in this group
        """
        final_result = True
        for robot_id in robots_id_list:
            if robot_id not in self._robots_id_in_group_list:
                logger.warning(
                    "RobotGroupBase: robot id {0} is not in group {1}".format(
                        robot_id, self._robots_id_in_group_list))
                final_result = False
            else:
                self._robots_id_in_group_list.remove(robot_id)
                logger.info(
                    "RobotGroupBase:  robot id {0} has been removed from  group {1}".format(
                        robot_id, self._robots_id_in_group_list))
        return final_result

    def execute_action(self, action_name, *args, **kw):
        """Executive function for non-instantaneous action
        that have 'wait_for_all_completion()'.

        :param action_name: which action need exec
        :param args: the action params
        :param args: the action key params
        :return:
        """
        action_dict = {}
        for robot_id in self._robots_id_in_group_list:
            robot_obj = self.all_robots_dict[robot_id]
            action_dict[robot_id] = getattr(robot_obj, action_name)(*args, **kw)
            logger.info("Multi Module robot id {0}: begin to execute the action".format(robot_id))
        multi_action = multi_module.MultiAction(action_dict)
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
        for robot_id in self._robots_id_in_group_list:
            robot_obj = self.all_robots_dict[robot_id]
            exec_cmd_thread = tool.TelloThread(target=getattr(robot_obj, command_name), *input_args, **input_kw)
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

    def get_sn(self):
        """ 获取组内机器的sn编号

        :param args:
        :return: dict: {robot_id: SN, ... }储存机器sn编号的字典，字典的键为机器的编号，值为对应的机器的sn号码
        """
        return self.execute_command('get_sn')


class RMGroup(RobotGroupBase):

    def __init__(self, robots_group_list, all_robots_dict):
        super().__init__(robots_group_list, all_robots_dict)

    def _scan_group_module(self):
        _chassis = multi_module.MultiRmModule(self, 'Chassis')
        _gimbal = multi_module.MultiRmModule(self, 'Gimbal')
        _blaster = multi_module.MultiRmModule(self, 'Blaster')
        _led = multi_module.MultiRmModule(self, 'Led')
        _robotic_arm = multi_module.MultiRmModule(self, 'RoboticArm')
        _gripper = multi_module.MultiRmModule(self, 'Gripper')
        self._group_modules_dict[_chassis.name] = _chassis
        self._group_modules_dict[_gimbal.name] = _gimbal
        self._group_modules_dict[_blaster.name] = _blaster
        self._group_modules_dict[_led.name] = _led
        self._group_modules_dict[_robotic_arm.name] = _robotic_arm
        self._group_modules_dict[_gripper.name] = _gripper

    def set_group_robots_mode(self, mode="free"):
        all_result = True
        for robot_id in self._robots_id_in_group_list:
            result = self._all_robots_dict[robot_id].set_robot_mode(mode)
            all_result = result and all_result
            if not result:
                logger.error(
                    "RobotGroup: set group_robots_mode {0}, robot id {1} set mode error!".format(mode, robot_id))
            else:
                logger.info(
                    "RobotGroup: set group_robots_mode {0}, robot id {1} set mode successfully!".format(mode, robot_id))
        if all_result:
            logger.info(
                "RobotGroup: set_group_robots_mode {1}, group {0}  set successfully".format(
                    self._robots_id_in_group_list, mode))
        else:
            logger.info(
                "RobotGroup: set_group_robots_mode {1}, group {0} set error".format(
                    self._robots_id_in_group_list, mode))
        return all_result

    def play_sound(self, sound_id, times=1):
        """
        robots in group play sound
        :param sound_id:
        :return:
        """
        final_result = False
        for robot_id in self._robots_id_in_group_list:
            result = self._all_robots_dict[robot_id].play_sound(
                sound_id, times)
            if not result:
                logger.warning("RobotGroup: Robot id {0} play_sound failed".format(robot_id))
            final_result = final_result and result
        return final_result

    @property
    def chassis(self):
        """ Get chassis obj """
        return self.get_group_module("Chassis")

    @property
    def gimbal(self):
        """ Get gimbal obj """
        return self.get_group_module("Gimbal")

    @property
    def blaster(self):
        """ Get blaster obj """
        return self.get_group_module("Blaster")

    @property
    def led(self):
        """ Get led obj """
        return self.get_group_module("Led")

    @property
    def robotic_arm(self):
        """ Get arm obj """
        return self.get_group_module("RoboticArm")

    @property
    def sensor(self):
        """ Get sensor obj"""
        return self.get_group_module("DistanceSensor")

    @property
    def gripper(self):
        """ Get gripper obj """
        return self.get_group_module("Gripper")


class SingleDroneInGroup(multi_module.TelloAction):

    def __init__(self, client, _robot_id, _robot_sn, _robot_host):
        self._client = client
        self._robot_id = _robot_id
        self._robot_sn = _robot_sn
        self._robot_host = _robot_host
        self.event = threading.Event()
        self.robot_group_host_list = []
        self.event.set()
        self._dispatcher = multi_module.TelloDispatcher(self._client, self.event, {self._robot_host: self._robot_id})
        self._dispatcher.action_host_list = [self._robot_host]

    def close(self):
        pass

    def send_command(self, command):
        self.event.wait(10)
        if self.event.isSet():
            logger.info("execute command：{}".format(command))
            proto = tool.TelloProtocol(command, self._robot_host)
            self._client.send(proto)
            self.event.clear()
        else:
            self.event.set()
            logger.warning("execute command：{}, timeout".format(command))


class TelloGroup(RobotGroupBase):

    def __init__(self, client, robot_id_group_list, _robot_id_dict={}, _robot_host_dict={}):
        super().__init__(robot_id_group_list, _robot_id_dict)
        self._robot_host_dict = _robot_host_dict
        self._robot_group_host_list = []
        self.init()
        self.client = client

    def init(self):
        for robot_id in self._robots_id_in_group_list:
            sn = self._all_robots_dict[robot_id]
            host = self._robot_host_dict[sn]
            self._robot_group_host_list.append(host)

    def get_sn(self):
        """ find sn in group"""
        return [self._all_robots_dict[robot_id] for robot_id in self._robots_id_in_group_list]

    @property
    def robot_group_host_list(self):
        return self._robot_group_host_list

    def get_robot(self, robot_id):
        """  get Drone obj """
        robot_sn = self._all_robots_dict[robot_id]
        robot_host = self._robot_host_dict[robot_sn]
        logger.info('get robot:SN:{}, HOST:{}' .format(robot_sn, robot_host))
        return SingleDroneInGroup(self.client, robot_id, robot_sn, robot_host)
