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


import traceback
import netifaces
import netaddr
import socket
import threading


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

        # limit range of search. This will work for router subnets
        if netmask != '255.255.255.0':
            continue

        # Create ip object and get
        cidr = netaddr.IPNetwork('%s/%s' % (address, netmask))
        network = cidr.network
        subnets.append((network, netmask))
        addr_list.append(address)
    return subnets, addr_list


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
