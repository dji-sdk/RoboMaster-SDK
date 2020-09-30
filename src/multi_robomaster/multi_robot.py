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


import sys
import time
import random
import threading
from robomaster import protocol
from robomaster import conn
from robomaster import robot
from robomaster import client
from robomaster import config
from . import logger
from . import tool
from . import multi_group
from . import multi_module


ROBOT_ID = 0
ROBOT_OBJ = 1
CHASSIS_LEAD_MODE = 2
GIMBAL_LEAD_MODE = 1
FREE_MODE = 0


class MultiRobotBase(object):

    def __init__(self):
        self._robots_list = []
        self._robots_num = 0
        self._group_list = []  # [group1, group2, ...]
        self._robot_ip_list = []  # [robot1_ip, robot2_ip, ...]
        self._robots_dict = {}  # key:id, value: robot obj

    def __del__(self):
        pass

    def initialize(self, robot_num):
        """scan all robots and init its

        :param num:
        :return:
        """
        self._robots_list = self._scan_multi_robot(robot_num)
        if not self._robots_list:
            logger.error("MultiRobotBase: initialize. No robot was found!")
            raise Exception("No robot was found!")
        self._robots_num = len(self._robots_list)
        for robot_obj in self._robots_list:
            robot_obj.initialize()

    def close(self):
        for robot_obj in self._robots_list:
            robot_obj.close()

    @property
    def all_robots(self):
        return self._robots_list

    @property
    def robots_num(self):
        return len(self._robots_list)

    @property
    def groups_num(self):
        return len(self._group_list)

    def _scan_multi_robot(self, num=0):
        """Automatic scanning of robots in the network

        :param num:
        :return:
        """
        pass

    def reset_all_robot(self):
        for robot_obj in self._robots_list:
            robot_obj.reset()

    def number_id_by_sn(self, *args):
        """number id by SN

        :param args: [id, SN] id int, SN str
        :return:
        """
        robots_sn_dict = tool.get_robots_sn(self._robots_list)
        for robot_id, robot_sn in args:
            if robot_sn not in robots_sn_dict.keys():
                raise Exception("Robot SN {0} is not exist!".format(robot_sn))
            elif robot_id in self._robots_dict.keys():
                raise Exception("Id {0} cannot be reused!".format(robot_id))
            elif robot_sn in self._robots_dict.values():
                raise Exception("SN {0} has been numbered!".format(robot_sn))
            self._robots_dict[robot_id] = robots_sn_dict[robot_sn]
        logger.info("MultiRobot: number id by sn successfully")
        self._robots_num = len(self._robots_dict)
        return self._robots_num

    def build_group(self, robot_id_list):
        """build a group that contains input robots

        :param robot_list:
        :return:
        """
        pass

    def remove_group(self, group_list):
        """ remove group from MultiRobot obj

        :param group_list:
        :return:
        """
        for group in group_list:
            if group not in self._group_list:
                logger.warning("MultiRobotBase group {0} do not exist".format(
                    group._robots_id_in_group_list))
            else:
                self._group_list.remove(group)
                logger.info("MultiRobotBase: group {0} has removed".format(
                    group._robots_id_in_group_list))

    def run(self, *exec_list):
        """Execute the action from the input list

        :param exec_list: [robot_group, action_task]...
        :return:
        """
        _groups_exec_dict = {}  # key: robot_group obj, value: execute thread
        logger.info("MultiRobot: run exec_list: {0}".format(exec_list))
        if not type(exec_list) is tuple:
            tuple(exec_list)
            logger.info(
                "MultiRobot: run type(exec_list) is not tuple, exec_list: {0}".format(exec_list))
        for robot_group, group_task in exec_list:
            if robot_group not in self._group_list:
                raise Exception('Input group', robot_group, 'is not built')

            exec_thread = threading.Thread(target=group_task, args=(robot_group,))
            exec_thread.start()
            _groups_exec_dict[robot_group] = exec_thread

        for robot_group, exec_thread in _groups_exec_dict.items():
            exec_thread.join()
            logger.info("MultiRobotBase: run, Action is completed")


class MultiEP(MultiRobotBase):
    """ S1_EP"""
    def __init__(self):
        super().__init__()

    def initialize(self, proto_type=config.DEFAULT_PROTO_TYPE):
        """scan all robots and init its

        :param num:
        :return:
        """
        self._robots_list = self._scan_multi_robot(proto_type)
        if not self._robots_list:
            logger.error("MultiRobotBase: initialize. No robot was found!")
            raise Exception("No robot was found!")
        self._robots_num = len(self._robots_list)
        for robot_obj in self._robots_list:
            robot_obj.initialize(proto_type)

    def _scan_multi_robot(self, proto_type=config.DEFAULT_PROTO_TYPE):
        """ Automatic scanning of robots in the network

        :return:
        """
        robot_list = []
        ip_list = conn.scan_robot_ip_list(10)
        for i, ip in enumerate(ip_list):
            sdk_conn = conn.SdkConnection()
            proxy_addr = (ip, config.ROBOT_PROXY_PORT)
            proto = protocol.ProtoSetSdkConnection()
            proto._connection = 1
            proto._host = protocol.host2byte(9, 6)
            if config.LOCAL_IP_STR:
                proto._ip = config.LOCAL_IP_STR
            else:
                proto._ip = '0.0.0.0'
            proto._port = random.randint(config.ROBOT_SDK_PORT_MIN, config.ROBOT_SDK_PORT_MAX)
            msg = protocol.Msg(robot.ROBOT_DEFAULT_HOST, protocol.host2byte(9, 0), proto)
            result, local_ip = sdk_conn.switch_remote_route(msg, proxy_addr)
            proto._ip = local_ip
            logger.info("request connection ip:{0} port:{1}".format(proto._ip, proto._port))
            if result:
                conn1 = conn.Connection((proto._ip, proto._port), (ip, config.ROBOT_DEVICE_PORT),
                                        protocol=proto_type)
                logger.info("connection {0}".format(conn1))
                cli = client.Client(9, 6, conn1)
                rob = robot.Robot(cli)
                robot_list.append(rob)
        return robot_list

    def build_group(self, robot_id_list):
        """build a group that contains input robots

        :param robot_id_list:
        :return:
        """
        check_result, robot_id = tool.check_robots_id(robot_id_list, self._robots_dict)
        if not check_result:
            raise Exception("Robot Id %d is not exist" % robot_id)
        robot_group = multi_group.RMGroup(robot_id_list, self._robots_dict)
        robot_group.initialize()
        self._group_list.append(robot_group)
        logger.info("MultiRobot: build_group successfully, group.robots_in_group_list : {0}".format(
            robot_group._robots_id_in_group_list))
        return robot_group

    def set_all_robots_mode(self, mode="gimbal_lead"):
        """

        :param mode: free, gimbal_lead, chassis_lead
        :return:
        """
        all_result = True
        for robot_id, robot_obj in self._robots_dict.items():
            result = robot_obj.set_robot_mode(mode)
            all_result = result and all_result
            if not result:
                print("Id %s : Set robot mode failed" % robot_id)
            else:
                print("Mode setup for all robots was successful")
        return all_result

    def number_id(self):
        """Manually number of all the robots entered at initialization.

        The program will block in this function before the numbering is completed

        return: the number of successful cars
        """
        robot_id = 0
        for robot_obj in self._robots_list:
            self._robots_dict[robot_id] = robot_obj
            self._number_prompt(robot_id, robot_obj)
            robot_id += 1
        return robot_id


class MultiDrone(MultiRobotBase):

    def __init__(self):
        self.robot_num = 0
        self._client = tool.TelloClient()
        self.tello_action = None
        self._robot_host_list = []
        self._group_list = []
        self._robot_id_dict = {}
        self._robot_sn_dict = {}
        self._robot_host_dict = {}

    def initialize(self, robot_num=0):
        self.robot_num = robot_num
        self._client.start()
        self._robot_host_list = self._client.scan_multi_robot(robot_num)

    def close(self):
        self._client.close()

    def _scan_multi_robot(self, num=0):
        self.initialize(num)
        _robot_ip_list = [host[0] for host in self._robot_host_list]
        return _robot_ip_list

    @staticmethod
    def reset_all_robot():
        logger.warning("Drone obj does not support this api \napi name:{}\napi location:{}"
                       .format(sys._getframe().f_code.co_name, sys._getframe().f_lineno))

    @staticmethod
    def all_robots():
        logger.warning("Drone obj does not support this api \napi name:{}\napi location:{}"
                       .format(sys._getframe().f_code.co_name, sys._getframe().f_lineno))

    @property
    def robots_num(self):
        return len(self._robot_host_list)

    def run(self, *exec_list):
        _groups_exec_dict = {}
        robot_group_host_list = []
        for robot_group, group_task in exec_list:
            if robot_group not in self._group_list:
                raise Exception('Input group', robot_group, 'is not built')
            self.tello_action = multi_module.TelloAction(self._client, self._robot_id_dict, self._robot_sn_dict,
                                                         self._robot_host_dict)
            exec_thread = threading.Thread(target=group_task, args=(self.tello_action.action_group(robot_group),))
            _groups_exec_dict[robot_group] = exec_thread
            robot_group_host_list.append(robot_group.robot_group_host_list)

        # don't allow the same drone run in different group
        result = tool.check_group_host(robot_group_host_list)
        if result is False:
            # todo BUG: low probability to has same id in one single group in number_id_to_all_drone api
            raise Exception("different running groups has same id")

        for robot_group, exec_thread in _groups_exec_dict.items():
            # todo 多task同步待添加
            exec_thread.start()

        for robot_group, exec_thread in _groups_exec_dict.items():
            exec_thread.join()
        logger.info("MultiRobotBase: run, Action is completed")

    def build_group(self, robot_id_group_list):
        check_result, robot_id = tool.check_robots_id(robot_id_group_list, self._robot_id_dict)
        if not check_result:
            raise Exception("Robot Id %d is not exist" % robot_id)
        tello_groups = multi_group.TelloGroup(self._client, robot_id_group_list,
                                              self._robot_id_dict, self._robot_sn_dict)
        self._group_list.append(tello_groups)
        return tello_groups

    def send_command(self, text, host_list=None):
        if host_list is None:
            host_list = self._robot_host_list
        for host in host_list:
            proto = tool.TelloProtocol(text, host)
            self._client.send(proto)

    def _get_sn(self, timeout=0):
        self.send_command("sn?")
        cur_time = time.time()
        while self._client.queue.qsize() < self.robot_num:
            if time.time() - cur_time > timeout:
                raise Exception("get sn timeout")

        while not self._client.queue.empty():
            proto = self._client.queue.get()
            if proto.text is None:
                raise Exception("recv data is None")
            self._robot_sn_dict[proto.text] = proto.host  # find host by sn
            time.sleep(0.1)   # Tello BUG that reply ok in sn? command response

        return self._robot_sn_dict

    def number_id_by_sn(self, *id_sn: list, timeout=3):
        if not isinstance(id_sn, tuple) and not isinstance(id_sn, list):
            raise Exception("input type must be list or tuple")

        self._get_sn(timeout)
        for id_, sn in id_sn:
            host = self._robot_sn_dict.get(sn, None)
            if host is None:
                raise Exception("Tello {} does not exits".format(sn))
            if self._robot_id_dict.get(id_, None) is not None:
                # one single id correspond to one single sn
                raise Exception("id: {} has already exited".format(id_))
            self._robot_id_dict[id_] = sn  # find sn by id
            self._robot_host_dict[host] = [id_]  # find id by host

    def number_id_to_all_drone(self, timeout=10):
        # number all drone num that initialize by self.initialize() from 0 to oo
        self._get_sn(timeout)
        for id_, item in enumerate(self._robot_sn_dict.items()):
            sn, host = item
            self._robot_id_dict[id_] = sn  # find sn by id
            self._robot_host_dict[host] = [id_]  # find id by host
