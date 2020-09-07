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
import random
import threading
from netaddr import IPNetwork
import socket
from robomaster import protocol
from robomaster import conn
from robomaster import robot
from robomaster import client
from robomaster import config
from . import logger
from . import tool
from . import multi_group


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
            elif robot_id in self._robots_dict.keys(3):
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
        ip_list = conn.scan_robot_ip_list(3)
        for i, ip in enumerate(ip_list):
            sdk_conn = conn.SdkConnection()
            proxy_addr = (ip, config.ROBOT_PROXY_PORT)
            proto = protocol.ProtoSetSdkConnection()
            proto._connection = 1
            proto._host = protocol.host2byte(9, 6)
            if config.LOCAL_IP_STR:
                proto._ip = config.LOCAL_IP_STR
            else:
                proto._ip = conn.get_local_ip()
            proto._port = random.randint(config.ROBOT_SDK_PORT_MIN, config.ROBOT_SDK_PORT_MAX)
            msg = protocol.Msg(robot.ROBOT_DEFAULT_HOST, protocol.host2byte(9, 0), proto)

            result, local_ip = sdk_conn.switch_remote_route(msg, proxy_addr)
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
        super().__init__()
        self._scan_socket = None

    def build_group(self, robot_id_list):
        """build a group that contains input robots

        :param robot_id_list:
        :return:
        """
        check_result, robot_id = tool.check_robots_id(robot_id_list, self._robots_dict)
        if not check_result:
            raise Exception("Robot Id %d is not exist" % robot_id)
        robot_group = multi_group.TelloGroup(robot_id_list, self._robots_dict)
        robot_group.initialize()
        self._group_list.append(robot_group)
        logger.info("MultiRobot: build_group successfully, group.robots_in_group_list : {0}".format(
            robot_group._robots_id_in_group_list))
        return robot_group

    def _scan_ip(self, num):
        """Find avaliable ip list in server's subnets

        :param num: Number of Tello this method is expected to find
        :return: None
        """
        logger.info('[Start_Searching]Searching for %s available Tello...\n' % num)

        subnets, address = tool.get_subnets()
        possible_addr = []

        for subnet, netmask in subnets:
            for ip in IPNetwork('%s/%s' % (subnet, netmask)):
                # skip local and broadcast
                if str(ip).split('.')[3] == '0' or str(ip).split('.')[3] == '255':
                    continue
                possible_addr.append(str(ip))

        while len(self._robot_ip_list) < num:
            logger.info('[Still_Searching]Trying to find Tello in subnets...\n')

            # delete already fond Tello ip
            for tello_ip in self._robot_ip_list:
                if tello_ip in possible_addr:
                    possible_addr.remove(tello_ip)
            # skip server itself
            for ip in possible_addr:
                if ip in address:
                    continue
                self._scan_socket.sendto(b'command', (ip, 8889))
            if len(self._robot_ip_list) >= num:
                break
            time.sleep(2)
        return self._robot_ip_list

    def _scan_multi_robot(self, num=0):
        """ Automatic scanning of robots in the network

        :param num:
        :return:
        """
        if config.LOCAL_IP_STR:
            local_ip = config.LOCAL_IP_STR
        else:
            local_ip = conn.get_local_ip()
        local_port = 8889
        local_addr = (local_ip, local_port)
        self._scan_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket for sending cmd
        self._scan_socket.bind(local_addr)
        # thread for receiving cmd ack
        receive_thread = threading.Thread(target=self._receive_task, args=(num, ))
        # receive_thread.daemon = True
        receive_thread.start()
        robot_list = []
        # scan by number
        ip_list = self._scan_ip(num)
        for ip in ip_list:
            te_ap_conf = config.te_conf
            if config.LOCAL_IP_STR:
                local_ip = config.LOCAL_IP_STR
            else:
                local_ip = conn.get_local_ip()
            local_port = random.randint(config.ROBOT_SDK_PORT_MIN, config.ROBOT_SDK_PORT_MAX)
            local_addr = (local_ip, local_port)
            te_ap_conf.default_sdk_addr = (local_addr)
            te_ap_conf.default_cmd_addr = (ip, te_ap_conf.default_cmd_addr_port)
            logger.info("MultiDrone: _scan_multi_robot, dron ip {0} uses addr {1}".format(
                te_ap_conf.default_cmd_addr, local_addr))
            drone_client = client.TextClient(te_ap_conf)
            drone_obj = robot.Drone(drone_client)
            if not hasattr(robot.Drone, "ip_addr"):
                drone_obj.ip_addr = ip
                robot_list.append(drone_obj)
        self._scan_socket.close()
        return robot_list

    def _receive_task(self, num):
        """Listen to responses from the Tello when scan the devices.

        :param:num:
        """
        while len(self._robot_ip_list) < num:
            try:
                resp, ip = self._scan_socket.recvfrom(1024)
                logger.info("FoundTello: from ip {1}_receive_task, recv msg: {0}".format(resp, ip))
                ip = ''.join(str(ip[0]))
                if resp.upper() == b'OK' and ip not in self._robot_ip_list:
                    logger.info('FoundTello: Found Tello.The Tello ip is:%s\n' % ip)
                    self._robot_ip_list.append(ip)
            except socket.error as exc:
                logger.error("[Exception_Error]Caught exception socket.error : {0}\n".format(exc))
        logger.info("FoundTello: has finished, recv_task quit!")
