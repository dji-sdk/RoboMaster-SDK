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
import traceback
import netifaces
import netaddr
from netaddr import IPNetwork
import socket
import queue
import threading
from . import logger
from robomaster import conn
from robomaster import config


def get_func_name():
    """
    Get the name of the calling function
    :return: calling-function`s name
    """
    return traceback.extract_stack()[-2][2]


def get_robots_sn(robots_list):
    """
    Get the sn for the robots_list,
    :param robots_list: which robots need to get sn
    :return: robots_sn_dict = {sn:robot_obj, ...}
    """
    robots_sn_dict = {}
    for robot_obj in robots_list:
        sn = robot_obj.get_sn()
        robots_sn_dict[sn] = robot_obj
    return robots_sn_dict


def check_robot_id(robot_id, robots_dict):
    """
    check to see if the robot id exists
    :param robot_id:
    :param robots_dict: the dict to search
    :return:
    """
    return robot_id in list(robots_dict.keys())


def check_robots_id(robots_id_list, robots_dict):
    """
    check to see if the robots id in input list exist
    :param robots_id_list:
    :param robots_dict: the dict to search
    :return: False, robot_id : robot_id do not exists
    :return: True, robot_id  : all robots id exist
    """
    for robot_id in robots_id_list:
        if not check_robot_id(robot_id, robots_dict):
            return False, robot_id
    return True, -1


def check_group_host(robot_group_host_list):
    if len(robot_group_host_list) == 0:
        logger.warning("‘run’ obj should have at least 1 param to run")
        return True
    total_lenth = 0
    _first_set = set(robot_group_host_list[0])
    for robot_group_host in robot_group_host_list:
        _first_set = _first_set.union(set(robot_group_host))
        total_lenth += len(robot_group_host)
    return len(_first_set) == total_lenth


def get_subnets():
    """
    Look through the machine's internet connection and
    returns subnet addresses and server ip
    :return: list[str]: subnets
             list[str]: addr_list
    """
    subnets = []
    ifaces = netifaces.interfaces()
    addr_list = []
    for myiface in ifaces:
        addrs = netifaces.ifaddresses(myiface)

        if socket.AF_INET not in addrs:
            continue
        # Get ipv4 stuff
        ipinfo = addrs[socket.AF_INET][0]
        address = ipinfo['addr']
        netmask = ipinfo['netmask']
        broadcast = ipinfo['broadcast']

        # special subnet
        if config.LOCAL_IP_STR is not None:
            target_broadcast = config.LOCAL_IP_STR.rsplit('.', 1)[0] + '.255'
            if target_broadcast != broadcast:
                continue

        # limit range of search. This will work for router subnets
        if netmask != '255.255.255.0':
            continue

        # Create ip object and get
        cidr = netaddr.IPNetwork('%s/%s' % (address, netmask))
        network = cidr.network
        subnets.append((network, netmask))
        addr_list.append(address)
    return subnets, addr_list


class TelloProtocol(object):

    def __init__(self, text=None, host=None, encoding='utf-8'):
        self._text = text
        self._host = host
        self.encoding = encoding

        self.init()

    def init(self):
        if self._text is None:
            logger.warning("Connection: recv buff None.")
            return
        if isinstance(self._text, bytes):
            if self._text == 204 or self._text == 255:
                logger.warning("decode_msg: recv invalid data, buff {0}".format(self._text))
                # drone has bug that reply error data 0xcc，43907 has bug that reply error data 0xff
                self._text = None
                return
            else:
                self._text = self._decode()
        elif isinstance(self._text, str):
            self._text = self._encode()

    @property
    def text(self):
        return self._text

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        self._host = value

    @text.setter
    def text(self, value):
        self._text = value

    def _encode(self):
        return self._text.encode(self.encoding)

    def _decode(self):
        return self._text.decode(self.encoding, 'ignore')


class TelloConnection(object):

    def __init__(self, local_ip=conn.get_local_ip(), local_port=8889):
        self.local_ip = local_ip
        self.local_port = local_port
        self._sock = None
        self.client_recieve_thread_flag = False   # for client recieve
        self._robot_host_list = []    # for scan robot

    def start(self):
        try:
            local_addr = (self.local_ip, self.local_port)
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket for sending cmd
            self._sock.bind(local_addr)
        except Exception as e:
            logger.warning("udpConnection: create, host_addr:{0}, exception:{1}".format(self.local_ip, e))
            raise

    def pre_close(self):
        if len(self._robot_host_list) > 0:
            for host in self._robot_host_list:
                self.send(TelloProtocol("command", host))
        else:
            logger.warning("no exit host")

    def close(self):
        if self._sock:
            self.pre_close()    # send command to shut down recv
            time.sleep(1)
            self._sock.close()

    def recv(self):
        try:
            if self._sock:
                data, host = self._sock.recvfrom(2048)
            else:
                raise Exception("socket used before assign")
        except Exception as e:
            logger.warning("Connection: recv, exception:{0}".format(e))
            raise
        proto = TelloProtocol(data, host)
        return proto

    def send(self, proto):
        try:
            if self._sock:
                self._sock.sendto(proto.text, proto.host)
        except Exception as e:
            logger.warning("Connection: send, exception:{0}".format(e))
            raise

    def _scan_host(self, num):
        """Find avaliable ip list in server's subnets

        :param num: Number of Tello this method is expected to find
        :return: None
        """
        logger.info('[Start_Searching]Searching for %s available Tello...\n' % num)

        subnets, address = get_subnets()
        possible_addr = []

        for subnet, netmask in subnets:
            for ip in IPNetwork('%s/%s' % (subnet, netmask)):
                # skip local and broadcast
                if str(ip).split('.')[3] == '0' or str(ip).split('.')[3] == '255':
                    continue
                possible_addr.append(str(ip))

        while len(self._robot_host_list) < num:
            logger.info('[Still_Searching]Trying to find Tello in subnets...\n')

            # delete already fond Tello ip
            for tello_host in self._robot_host_list:
                if tello_host[0] in possible_addr:
                    possible_addr.remove(tello_host[0])
            # skip server itself
            for ip in possible_addr:
                if ip in address:
                    continue
                self._sock.sendto(b'command', (ip, self.local_port))
            if len(self._robot_host_list) >= num:
                break
        return self._robot_host_list

    def scan_multi_robot(self, num=0):
        """ Automatic scanning of robots in the network

        :param num:
        :return:
        """
        receive_thread = threading.Thread(target=self._scan_receive_task, args=(num, ), daemon=True)
        receive_thread.start()
        robot_host_list = self._scan_host(num)
        receive_thread.join()
        return robot_host_list

    def _scan_receive_task(self, num):
        """Listen to responses from the Tello when scan the devices.

        :param:num:
        """
        while len(self._robot_host_list) < num:
            try:
                resp, ip = self._sock.recvfrom(1024)
                logger.info("FoundTello: from ip {1}_receive_task, recv msg: {0}".format(resp, ip))
                ip = ''.join(str(ip[0]))
                if resp.upper() == b'OK' and ip not in self._robot_host_list:
                    logger.info('FoundTello: Found Tello.The Tello ip is:%s\n' % ip)
                    self._robot_host_list.append((ip, self.local_port))
            except socket.error as exc:
                logger.error("[Exception_Error]Caught exception socket.error : {0}\n".format(exc))
        self.client_recieve_thread_flag = True
        logger.info("FoundTello: has finished, _scan_receive_task quit!")


class TelloClient(object):
    def __init__(self):
        self._conn = TelloConnection()
        self.queue = queue.Queue()
        self.receive_thread = threading.Thread(target=self.recv, daemon=True)
        self.receive_thread_flag = True

    def start(self):
        self._conn.start()
        self.receive_thread.start()

    def close(self):
        self.receive_thread_flag = False
        self._conn.client_recieve_thread_flag = True
        if self._conn:
            self._conn.close()
        self.receive_thread.join(10)

    def recv(self):
        while not self._conn.client_recieve_thread_flag:
            pass
        logger.info("recv thread start!")
        while self.receive_thread_flag:
            proto = self._conn.recv()
            self.queue.put(proto)
        logger.info("recv thread quit!")

    def send(self, proto):
        self._conn.send(proto)

    def scan_multi_robot(self, num):
        return self._conn.scan_multi_robot(num)


class TelloStatus(object):

    FLIGHT_ACTION_SET = {"error", "ok", 'out of range', "error No valid marker", "error Not joystick",
                         "error Auto Land", "error No valid imu", "error, high temp", "error Motor stop"}

    EXT_ACTION_SET = {"led ok", "matrix ok", 'unknow command: led', "unknow command: mled", "command error: 254"}

    def __init__(self, cur_action):
        self.cur_action = cur_action

    @staticmethod
    def judge(proto):
        data = proto.text
        host = proto.host
        if data is None:
            if host is None:
                logger.waring("socket closed")
        else:
            _last_two_words = data.strip()[-2:]
            if _last_two_words != "ok":
                # judge reply contains ok or battery
                try:
                    float(_last_two_words)   # battery obj
                except ValueError:
                    logger.warning("reply false: {}".format(data))
            else:
                logger.debug("DRONE reply：{}".format(data))


class TelloThread(threading.Thread):

    def __init__(self, target, *args, **kwargs):
        threading.Thread.__init__(self)
        self.args = args
        self.kw = kwargs
        self.result = None
        self.target = target

    def run(self):
        self.result = self.target(*self.args, **self.kw)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None
