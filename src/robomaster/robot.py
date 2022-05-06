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


import os
import threading
import netifaces
import socket
import netaddr
import time
from netaddr import IPNetwork
from . import protocol
from . import logger
from . import action
from . import client
from . import conn
from . import gimbal
from . import chassis
from . import camera
from . import blaster
from . import vision
from . import servo
from . import config
from . import dds
from . import led
from . import battery
from . import robotic_arm
from . import sensor
from . import gripper
from . import armor
from . import flight
from . import uart
from . import ai_module

__all__ = ['Robot', 'RobotPlaySoundAction', 'Drone', 'FREE', 'GIMBAL_LEAD', 'CHASSIS_LEAD',
           'SOUND_ID_ATTACK', 'SOUND_ID_SHOOT', 'SOUND_ID_SCANNING', 'SOUND_ID_RECOGNIZED',
           'SOUND_ID_GIMBAL_MOVE', 'SOUND_ID_COUNT_DOWN']


MODULE_CHASSIS = 'chassis'
MODULE_GIMBAL = 'gimbal'
MODULE_LED = 'led'
MODULE_CAMERA = 'camera'
MODULE_BATTERY = 'battery'
MODULE_GRIPPER = 'gripper'
MODULE_VISION = 'vision'
MODULE_BLASTER = 'blaster'
MODULE_DDS = 'dds'
MODULE_DISTANCE_SENSOR = 'dis_sensor'
MODULE_ROBOTIC_ARM = 'robotic_arm'
MODULE_AI_MODULE = 'ai_module'

FREE = "free"
GIMBAL_LEAD = "gimbal_lead"
CHASSIS_LEAD = "chassis_lead"

SOUND_ID_ATTACK = 0x101
SOUND_ID_SHOOT = 0x102
SOUND_ID_SCANNING = 0x103
SOUND_ID_RECOGNIZED = 0x104
SOUND_ID_GIMBAL_MOVE = 0x105
SOUND_ID_COUNT_DOWN = 0x106

SOUND_ID_1C = 0x107
SOUND_ID_1C_SHARP = 0x108
SOUND_ID_1D = 0x109
SOUND_ID_1D_SHARP = 0x10A
SOUND_ID_1E = 0x10B
SOUND_ID_1F = 0x10C
SOUND_ID_1F_SHARP = 0x10D
SOUND_ID_1G = 0x10e
SOUND_ID_1A = 0x110
SOUND_ID_1A_SHARP = 0x111
SOUND_ID_1B = 0x112
SOUND_ID_2C = 0x113
SOUND_ID_2C_SHARP = 0x114
SOUND_ID_2D = 0x115
SOUND_ID_2D_SHARP = 0x116
SOUND_ID_2E = 0x117
SOUND_ID_2F = 0x118
SOUND_ID_2F_SHARP = 0x119
SOUND_ID_2G = 0x11A
SOUND_ID_2G_SHARP = 0x11B
SOUND_ID_2A = 0x11C
SOUND_ID_2A_SHARP = 0x11D
SOUND_ID_2B = 0x11E
SOUND_ID_3C = 0x11F
SOUND_ID_3C_SHARP = 0x120
SOUND_ID_3D = 0x121
SOUND_ID_3D_SHARP = 0x122
SOUND_ID_3E = 0x123
SOUND_ID_3F = 0x124
SOUND_ID_3F_SHARP = 0x125
SOUND_ID_3G = 0x126
SOUND_ID_3G_SHARP = 0x127
SOUND_ID_3A = 0x128
SOUND_ID_3A_SHARP = 0x129
SOUND_ID_3B = 0x12A

ROBOT_DEFAULT_HOST = protocol.host2byte(9, 6)


class RobotPlaySoundAction(action.Action):
    _action_proto_cls = protocol.ProtoPlaySound
    _push_proto_cls = protocol.ProtoSoundPush
    _target = protocol.host2byte(9, 0)

    def __init__(self, sound_id, times, **kw):
        super().__init__(**kw)
        self._sound_id = sound_id
        self._play_times = times

    def __repr__(self):
        return "action_id:{0}, state:{1}, percent:{2}, sound_id:{3}".format(
            self._action_id, self._state, self._percent, self._sound_id)

    def encode(self):
        proto = self._action_proto_cls()
        proto.sound_id = self._sound_id
        proto.play_times = self._play_times
        return proto

    def update_from_push(self, proto):
        if proto.__class__ is not self._push_proto_cls:
            return

        self._percent = proto._percent
        self._update_action_state(proto._action_state)

        logger.info("{0} update_from_push: {1}".format(self.__class__.__name__, self))


class TelloTempInfoSubject(dds.Subject):
    name = dds.DDS_TELLO_TEMP

    def __init__(self):
        self._temp_l = 0
        self._temp_h = 0
        self._info_num = 2
        self._freq = protocol.TelloDdsProto.DDS_FREQ

    def temp_info(self):
        return self._temp_l, self._temp_h

    def data_info(self):
        return self._temp_l, self._temp_h

    def decode(self, buf):
        push_info = buf.split(';')
        found_info_num = 0
        for info in push_info:
            if protocol.TelloDdsProto.DDS_TEMP_L_FLAG in info:
                temp_l_str = info.split(':')[1]
                self._temp_l = int(temp_l_str)
                found_info_num += 1
            elif protocol.TelloDdsProto.DDS_TEMP_H_FLAG in info:
                temp_h_str = info.split(':')[1]
                self._temp_h = int(temp_h_str)
                found_info_num += 1
        if found_info_num == self._info_num:
            return True
        else:
            logger.debug("TelloTempInfoSubject: decode, found_info_num {0} is not match self._info_num {1}".format(
                found_info_num, self._info_num))
            return False


class TelloTofInfoSubject(dds.Subject):
    name = dds.DDS_TELLO_TOF

    def __init__(self):
        self._tof = 0
        self._info_num = 1
        self._freq = protocol.TelloDdsProto.DDS_FREQ

    def tof_info(self):
        return self._tof

    def data_info(self):
        return self._tof

    def decode(self, buf):
        push_info = buf.split(';')
        found_info_num = 0
        for info in push_info:
            if protocol.TelloDdsProto.DDS_TOF_FLAG in info:
                tof_str = info.split(':')[1]
                self._tof = int(tof_str)
                found_info_num += 1
        if found_info_num == self._info_num:
            return True
        else:
            logger.debug("TelloTofInfoSubject: decode, found_info_num {0} is not match self._info_num {1}".format(
                found_info_num, self._info_num))
            return False


class TelloDroneInfoSubject(dds.Subject):
    name = dds.DDS_TELLO_DRONE

    def __init__(self):
        self._high = 0
        self._baro = 0
        self._time = 0
        self._info_num = 3
        self._freq = protocol.TelloDdsProto.DDS_FREQ

    def drone_info(self):
        return self._high, self._baro, self._time

    def data_info(self):
        return self._high, self._baro, self._time

    def decode(self, buf):
        push_info = buf.split(';')
        found_info_num = 0
        for info in push_info:
            if info.startswith(protocol.TelloDdsProto.DDS_HIGH_FLAG):
                high_str = info.split(':')[1]
                self._high = int(high_str)
                found_info_num += 1
            elif protocol.TelloDdsProto.DDS_BARO_FLAG in info:
                baro_str = info.split(':')[1]
                self._baro = float(baro_str)
                found_info_num += 1
            elif protocol.TelloDdsProto.DDS_MOTOR_TIME_FLAG in info:
                logger.debug("TelloDroneInfoSubject: time_info {0}".format(info))
                time_str = info.split(':')[1]
                self._time = int(time_str)
                found_info_num += 1
        if found_info_num == self._info_num:
            return True
        else:
            logger.warning("TelloDroneInfoSubject: decode, found_info_num {0} is not match self._info_num {1}".format(
                found_info_num, self._info_num))
            return False


class TelloStatusSubject(dds.Subject):
    """ Tello 飞机的所有状态数据 """
    name = dds.DDS_TELLO_ALL

    def __init__(self):
        self._freq = protocol.TelloDdsProto.DDS_FREQ
        self._pad_mid = 0
        self._pad_x = 0
        self._pad_y = 0
        self._pad_z = 0
        self._pad_mpry = []
        self._pad_mpry_num = 3
        self._pitch = 0
        self._roll = 0
        self._yaw = 0
        self._vgx = 0
        self._vgy = 0
        self._vgz = 0
        self._templ = 0
        self._temph = 0
        self._tof = 0
        self._high = 0
        self._bat = 0
        self._baro = 0
        self._motor_time = 0
        self._agx = 0
        self._agy = 0
        self._agz = 0
        self._dds_proto = protocol.TelloDdsProto
        self._status_dict = {self._dds_proto.DDS_PAD_MID_FLAG: self._pad_mid,
                             self._dds_proto.DDS_PAD_X_FLAG: self._pad_x,
                             self._dds_proto.DDS_PAD_Y_FLAG: self._pad_y,
                             self._dds_proto.DDS_PAD_Z_FLAG: self._pad_z,
                             self._dds_proto.DDS_PAD_MPRY_FLAG: self._pad_mpry,
                             self._dds_proto.DDS_PITCH_FLAG: self._pitch,
                             self._dds_proto.DDS_ROLL_FLAG: self._roll,
                             self._dds_proto.DDS_YAW_FLAG: self._yaw,
                             self._dds_proto.DDS_VGX_FLAG: self._vgx,
                             self._dds_proto.DDS_VGY_FLAG: self._vgy,
                             self._dds_proto.DDS_VGZ_FLAG: self._vgz,
                             self._dds_proto.DDS_TEMP_L_FLAG: self._templ,
                             self._dds_proto.DDS_TEMP_H_FLAG: self._temph,
                             self._dds_proto.DDS_TOF_FLAG: self._tof,
                             self._dds_proto.DDS_HIGH_FLAG: self._high,
                             self._dds_proto.DDS_BATTERY_FLAG: self._bat,
                             self._dds_proto.DDS_BARO_FLAG: self._baro,
                             self._dds_proto.DDS_MOTOR_TIME_FLAG: self._motor_time,
                             self._dds_proto.DDS_AGX_FLAG: self._agx,
                             self._dds_proto.DDS_AGY_FLAG: self._agy,
                             self._dds_proto.DDS_AGZ_FLAG: self._agz}

    def decode(self, buf):
        """ 根据数据推送更新 drone 的状态数据
        """
        if dds.IS_AI_FLAG not in buf:
            push_data_list = buf.split(';')
            for info in push_data_list:
                if ':' not in info:
                    continue
                name, data = info.split(':')
                if name == self._dds_proto.DDS_PAD_MPRY_FLAG:
                    pad_mpry_info = data.split(',')
                    self._status_dict[name].clear()
                    for i in range(self._pad_mpry_num):
                        self._status_dict[name].append(float(pad_mpry_info[i]))
                else:
                    self._status_dict[name] = float(data)

    @property
    def freq(self):
        return self._freq

    @freq.setter
    def freq(self, in_freq):
        if in_freq == 1 or in_freq == 5 or in_freq == 10:
            self._freq = in_freq

    def pad_position(self):
        return self._status_dict[self._dds_proto.DDS_PAD_X_FLAG], \
               self._status_dict[self._dds_proto.DDS_PAD_Y_FLAG], \
               self._status_dict[self._dds_proto.DDS_PAD_Z_FLAG]

    def get_status(self, name):
        return self._status_dict[name]


class RobotBase(object):
    _product = "NotSpecific"

    def __init__(self, cli=None, conf=config.ep_conf):
        self._client = cli
        self._modules = {}

    @property
    def client(self):
        return self._client

    @property
    def product(self):
        return self._product


class Drone(RobotBase):
    """ 教育系列无人机 """

    def __init__(self, cli=None):
        self._robot_host_list = []
        self._conf = config.te_conf
        self.local_ip = None
        self.local_port = self._conf.default_sdk_addr[1]
        self.status_sub = None
        self._sock = None
        super().__init__(cli)

    @property
    def conf(self):
        return self._conf

    @property
    def flight(self):
        return self.get_module("Flight")

    @property
    def action_dispatcher(self):
        return self._action_dispatcher

    @property
    def battery(self):
        return self.get_module("TelloBattery")

    @property
    def camera(self):
        return self.get_module("TelloCamera")

    @property
    def dds(self):
        return self.get_module("TelloSubscriber")

    @property
    def sensor(self):
        return self.get_module("TelloDistanceSensor")

    @property
    def led(self):
        return self.get_module("TelloLed")

    @property
    def ai_module(self):
        return self.get_module("TelloAI")

    def get_module(self, name):
        return self._modules[name]

    def _scan_modules(self):
        _flight = flight.Flight(self)
        _camera = camera.TelloCamera(self)
        _battery = battery.TelloBattery(self)
        _ai_module = ai_module.TelloAI(self)
        _dds = dds.TelloSubscriber(self)
        _dds.start()
        _sensor = sensor.TelloDistanceSensor(self)
        _led = led.TelloLed(self)

        self._status_sub = TelloStatusSubject()
        self._status_sub.freq = protocol.TelloDdsProto.DDS_FREQ
        _dds.add_subject_info(self._status_sub, None, None, None)

        self._modules[_flight.__class__.__name__] = _flight
        self._modules[_camera.__class__.__name__] = _camera
        self._modules[_battery.__class__.__name__] = _battery
        self._modules[_ai_module.__class__.__name__] = _ai_module
        self._modules[_dds.__class__.__name__] = _dds
        self._modules[_sensor.__class__.__name__] = _sensor
        self._modules[_led.__class__.__name__] = _led

    def get_subnets(self):
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

    def _scan_host(self, timeout=10):
        """Find avaliable ip list in server's subnets

        :param num: Number of Tello this method is expected to find
        :return: None
        """
        logger.info('[Start_Searching]Searching for available Tello...\n')

        subnets, address = self.get_subnets()
        possible_addr = []

        for subnet, netmask in subnets:
            for ip in IPNetwork('%s/%s' % (subnet, netmask)):
                # skip local and broadcast
                if str(ip).split('.')[3] == '0' or str(ip).split('.')[3] == '255':
                    continue
                possible_addr.append(str(ip))
        last_time = time.time()
        while len(self._robot_host_list) < 10:
            # delete already fond Tello ip
            for tello_host in self._robot_host_list:
                if tello_host[0] in possible_addr:
                    possible_addr.remove(tello_host[0])
            # skip server itself
            for ip in possible_addr:
                if ip in address:
                    continue
                self._sock.sendto(b'command', (ip, 8889))
            if len(self._robot_host_list) >= 1:
                break
            if timeout < time.time() - last_time:
                raise logger.error("Drone: can not find the drone robot")
        return self._robot_host_list

    def scan_drone_robot(self):
        """ Automatic scanning of robots in the network

        :param num:
        :return:
        """
        receive_thread = threading.Thread(target=self._scan_receive_task, daemon=True)
        receive_thread.start()
        robot_host_list = self._scan_host()
        receive_thread.join()
        return robot_host_list

    def _scan_receive_task(self):
        """Listen to responses from the Tello when scan the devices.

        :param:num:
        """
        while len(self._robot_host_list) < 1:
            try:
                resp, ip = self._sock.recvfrom(1024)
                logger.info("FoundTello: from ip {1}_receive_task, recv msg: {0}".format(resp, ip))
                ip = ''.join(str(ip[0]))
                if resp.upper() == b'OK' and ip not in self._robot_host_list:
                    self._robot_host_list.append((ip, self.local_port))
                    logger.info('FoundTello: Found Tello.The Tello ip is:%s\n' % ip)
            except socket.error as exc:
                logger.error("[Exception_Error]Caught exception socket.error : {0}\n".format(exc))
        self.client_recieve_thread_flag = True
        logger.info("FoundTello: has finished, _scan_receive_task quit!")

    def start(self):
        try:
            if config.LOCAL_IP_STR:
                self.local_ip = config.LOCAL_IP_STR
            else:
                self.local_ip = conn.get_local_ip()
            local_addr = (self.local_ip, self.local_port)
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket for sending cmd
            self._sock.bind(local_addr)
        except Exception as e:
            logger.warning("udpConnection: create, host_addr:{0}, exception:{1}".format(self.local_ip, e))
            raise

    def search_stop(self):
        self._sock.close()

    def initialize(self, conn_type=config.DEFAULT_CONN_TYPE):
        if not self._client:
            default_sdk_addr = self._conf.default_sdk_addr
            video_stream_addr = self._conf.video_stream_addr
            if conn_type == 'ap':
                if config.LOCAL_IP_STR:
                    self._conf.default_sdk_addr = (config.LOCAL_IP_STR, default_sdk_addr[1])
                    self._conf.video_stream_addr = (config.LOCAL_IP_STR, video_stream_addr[1])
                else:
                    local_ip = conn.get_local_ip()
                    self._conf.default_sdk_addr = (local_ip, default_sdk_addr[1])
                    self._conf.video_stream_addr = (local_ip, video_stream_addr[1])
                logger.info("Drone: initialize, the connection uses local addr {0}".format(self._conf.default_sdk_addr))
                self._client = client.TextClient(self._conf)
            elif conn_type == 'sta':
                if config.LOCAL_IP_STR:
                    self._conf.default_sdk_addr = (config.LOCAL_IP_STR, default_sdk_addr[1])
                    self._conf.video_stream_addr = (config.LOCAL_IP_STR, video_stream_addr[1])
                else:
                    local_ip = conn.get_local_ip()
                    self._conf.default_sdk_addr = (local_ip, default_sdk_addr[1])
                    self._conf.video_stream_addr = (local_ip, video_stream_addr[1])
                if config.ROBOT_IP_STR:
                    self._conf.default_robot_addr = (config.ROBOT_IP_STR, self._conf.default_cmd_addr[1])
                    logger.info(
                        "Drone: initialize, the connection uses local addr {0}".format(self._conf.default_sdk_addr))
                    self._client = client.TextClient(self._conf)
                else:
                    self.start()
                    robot_addr = self.scan_drone_robot()
                    self.search_stop()
                    self._conf.default_robot_addr = (str(robot_addr[0][0]), self._conf.default_cmd_addr[1])
                    logger.info(
                        "Drone: initialize, the  connection uses local addr {0}".format(self._conf.default_sdk_addr))
                    self._client = client.TextClient(self._conf)
            else:
                logger.error("Drone: unknown connect type {0}".format(conn_type))

        try:
            self._client.start()
        except Exception as e:
            logger.error("Drone: Connection Create Failed.")
            raise e

        self._action_dispatcher = action.ActionDispatcher(self.client)
        self._action_dispatcher.initialize()
        self._scan_modules()
        return self._enable_sdk(1)

    def _enable_sdk(self, on_off=1):
        proto = protocol.TextProtoDrone()
        proto.text_cmd = ""
        if on_off == 1:
            proto.text_cmd = "command"
        elif on_off == 0:
            logger.warning("not support on_off:{0}".format(on_off))
            return True
        else:
            logger.warning("Drone: not support on_off:{0}".format(on_off))
            return False
        msg = protocol.TextMsg(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
        except Exception as e:
            logger.warning("Drone: _enable_sdk exception {0}".format(str(e)))
            return False
        if resp_msg:
            resp_proto = resp_msg.get_proto()
        else:
            return False
        if resp_proto.get_status():
            logger.info("Drone: _enable_sdk, The drone SDK is enabled")
            return True
        else:
            return False

    def close(self):
        """ 停止drone对象 """
        self._enable_sdk(0)
        self._client.stop()
        self.dds.stop()
        logger.info("Drone close")

    def send_command(self):
        return self._enable_sdk(1)

    def get_sdk_version(self):
        """ 获取SDK版本号

        :return: string: 版本号
        """
        cmd = "sdk?"
        proto = protocol.TextProtoDrone()
        proto.text_cmd = cmd
        msg = protocol.TextMsg(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                if proto:
                    return proto.resp
                else:
                    return None
            else:
                logger.warning("Drone: get_sdk_version failed.")
        except Exception as e:
            logger.warning("Drone: get_sdk_version, send_sync_msg exception {0}".format(str(e)))
            return None

    def get_wifi_version(self):
        """ 获取WIFI版本号

        :return: string: 版本号
        """
        cmd = "wifiversion?"
        proto = protocol.TextProtoDrone()
        proto.text_cmd = cmd
        msg = protocol.TextMsg(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                if proto:
                    return proto.resp
                else:
                    return None
            else:
                logger.warning("Drone: get_wifi_version failed.")
        except Exception as e:
            logger.warning("Drone: get_wifi_version, send_sync_msg exception {0}".format(str(e)))
            return None

    def get_ssid(self):
        """ 获取SSID名称

        :return: string: ssid名称
        """
        cmd = "ssid?"
        proto = protocol.TextProtoDrone()
        proto.text_cmd = cmd
        msg = protocol.TextMsg(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                if proto:
                    return proto.resp
                else:
                    return None
            else:
                logger.warning("Drone: get_ssid failed.")
        except Exception as e:
            logger.warning("Drone: get_ssid, send_sync_msg exception {0}".format(str(e)))
            return None

    def get_drone_version(self):
        """ 获取飞机固件版本号

        :return: string: 版本号
        """
        cmd = "version?"
        proto = protocol.TextProtoDrone()
        proto.text_cmd = cmd
        msg = protocol.TextMsg(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                if proto:
                    return "drone" + proto.resp
                else:
                    return None
            else:
                logger.warning("Drone: get_drone_version failed.")
        except Exception as e:
            logger.warning("Drone: get_drone_version, send_sync_msg exception {0}".format(str(e)))
            return None

    def get_esp32_version(self):
        """ 获取esp32版本号

        :return: string: 版本号
        """
        cmd = "EXT version?"
        proto = protocol.TextProtoDrone()
        proto.text_cmd = cmd
        msg = protocol.TextMsg(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                if proto:
                    return proto.resp.split(" ")[1]
                else:
                    return None
            else:
                logger.warning("Drone: get_esp32_version failed.")
        except Exception as e:
            logger.warning("Drone: get_esp32_version, send_sync_msg exception {0}".format(str(e)))
            return None

    def get_hardware(self):
        """ 获取飞机硬件信息
        本命令仅支持SDK版本号>=30
        可通过hardware?指令查询是否有接WIFI拓展模块，没接拓展模块返回TELLO，接了拓展模块返回RMTT。

        :return: string: 硬件信息
        """
        cmd = "hardware?"
        proto = protocol.TextProtoDrone()
        proto.text_cmd = cmd
        msg = protocol.TextMsg(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                if proto:
                    return proto.resp
                else:
                    return None
            else:
                logger.warning("Drone: get_hardware failed.")
        except Exception as e:
            logger.warning("Drone: get_hardware, send_sync_msg exception {0}".format(str(e)))
            return None

    def get_sn(self):
        """ 获取飞机sn号

        :return: string: 飞机的SN号
        """
        cmd = "sn?"
        proto = protocol.TextProtoDrone()
        proto.text_cmd = cmd
        msg = protocol.TextMsg(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                if proto:
                    return proto.resp
                else:
                    return None
            else:
                logger.warning("Drone: get_sn failed.")
        except Exception as e:
            logger.warning("Drone: get_sn, send_sync_msg exception {0}".format(str(e)))
            return None

    def get_wifi(self):
        """ 获取wifi信噪比

        :return: float: wifi的信噪比数值
        """
        cmd = 'wifi?'
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
                logger.warning("Drone: get_wifi failed.")
        except Exception as e:
            logger.warning("Drone: get_wifi, send_sync_msg exception {0}".format(str(e)))
            return None

    def get_motor_time(self):
        """ 获取电机运行时间

        :return: string: 电机的运行时间
        """
        cmd = "time?"
        proto = protocol.TextProtoDrone()
        proto.text_cmd = cmd
        msg = protocol.TextMsg(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                if proto:
                    return proto.resp
                else:
                    return None
            else:
                logger.warning("Drone: get motor time failed.")
        except Exception as e:
            logger.warning("Drone: get_motor_time, send_sync_msg exception {0}".format(str(e)))
            return None

    def get_height(self):
        """ 获取飞机相对高度

        :return: string: 飞机相对高度
        """
        cmd = "height?"
        proto = protocol.TextProtoDrone()
        proto.text_cmd = cmd
        msg = protocol.TextMsg(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                if proto:
                    return proto.resp
                else:
                    return None
            else:
                logger.warning("Drone: get_height failed.")
        except Exception as e:
            logger.warning("Drone: get_height, send_sync_msg exception {0}".format(str(e)))
            return None

    def get_temp(self):
        """ 获取飞机机身温度

        :return: dict: 飞机机身温度
        """
        cmd = "temp?"
        proto = protocol.TextProtoDrone()
        proto.text_cmd = cmd
        msg = protocol.TextMsg(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                if proto:
                    return proto.proresp
                else:
                    return None
            else:
                logger.warning("Drone: get_temp failed.")
        except Exception as e:
            logger.warning("Drone: get_temp, send_sync_msg exception {0}".format(str(e)))
            return None

    def get_attitude(self):
        """ 获取飞机三轴姿态信息

        :return: dict: 飞机三轴姿态信息
        """
        cmd = "attitude?"
        proto = protocol.TextProtoDrone()
        proto.text_cmd = cmd
        msg = protocol.TextMsg(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                if proto:
                    return proto.proresp
                else:
                    return None
            else:
                logger.warning("Drone: get_attitude failed.")
        except Exception as e:
            logger.warning("Drone: get_attitude, send_sync_msg exception {0}".format(str(e)))
            return None

    def get_baro(self):
        """ 获取电机气压计高度

        :return: float: 电机气压计高度
        """
        cmd = "baro?"
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
                logger.warning("Drone: get_baro failed.")
        except Exception as e:
            logger.warning("Drone: get_baro, send_sync_msg exception {0}".format(str(e)))
            return None

    def get_acceleration(self):
        """ 获取飞机三轴加速度值

        :return: dict: 飞机三轴加速度值
        """
        cmd = "acceleration?"
        proto = protocol.TextProtoDrone()
        proto.text_cmd = cmd
        msg = protocol.TextMsg(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                if proto:
                    return proto.proresp
                else:
                    return None
            else:
                logger.warning("Drone: get_acceleration failed.")
        except Exception as e:
            logger.warning("Drone: get_acceleration, send_sync_msg exception {0}".format(str(e)))
            return None

    def set_wifichannel(self, channel):
        """ 设置飞机WIFI信道

        :param channel: 需要设置的信道
        :return: bool: 设置结果
        """
        cmd = "wifisetchannel {0}".format(channel)
        proto = protocol.TextProtoDrone()
        proto.text_cmd = cmd
        msg = protocol.TextMsg(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                if proto:
                    if proto.resp.lower().startswith(protocol.TextProtoData.SUCCESSFUL_RESP_FLAG):
                        return True
                    else:
                        logger.warning("Drone: resp {0}".format(proto.resp))
                logger.warning("Drone: set_wifichannel failed")
            return False
        except Exception as e:
            logger.warning("Drone: set_wifichannel, send_sync_msg exception {0}".format(str(e)))
            return False

    def config_sta(self, ssid, password):
        """ 设置飞机的连接模式为组网模式

        :param ssid: 路由器的账号
        :param password: 路由器的密码
        :return: bool: 设置结果
        """
        cmd = "ap {0} {1}".format(ssid, password)
        proto = protocol.TextProtoDrone()
        proto.text_cmd = cmd
        msg = protocol.TextMsg(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                if proto:
                    if proto.resp.lower().startswith(protocol.TextProtoData.SUCCESSFUL_RESP_FLAG):
                        return True
                    else:
                        logger.warning("Drone: resp {0}".format(proto.resp))
            logger.warning("Drone: config_sta failed")
            return False

        except Exception as e:
            logger.warning("Drone: config_sta, send_sync_msg exception {0}".format(str(e)))
            return False

    def sub_temp(self, freq=5, callback=None, *args, **kw):
        """ 订阅飞机温度信息

        :param freq: 订阅数据的频率, 1HZ, 5HZ, 10HZ
        :param callback: 传入数据处理的回掉函数
        :param args: 回调函数参数
        :param kw: 回调函数参数
        :return: 返回订阅结果
        """
        sub = self.dds
        subject = TelloTempInfoSubject()
        subject.freq = freq
        return sub.add_subject_info(subject, callback, args, kw)

    def unsub_temp(self):
        """ 取消订阅温度信息。

        :return: 返回取消订阅结果。
        """
        sub_dds = self.dds
        return sub_dds.del_subject_info(dds.DDS_TELLO_TEMP)

    def sub_tof(self, freq=5, callback=None, *args, **kw):
        """ 订阅飞机tof信息

        :param freq: 订阅数据的频率, 1HZ, 5HZ, 10HZ
        :param callback: 传入数据处理的回掉函数
        :param args: 回调函数参数
        :param kw: 回调函数参数
        :return: 返回订阅结果
        """
        sub = self.dds
        subject = TelloTofInfoSubject()
        subject.freq = freq
        return sub.add_subject_info(subject, callback, args, kw)

    def unsub_tof(self):
        """ 取消订阅tof信息

        :return: 返回取消订阅结果
        """
        sub_dds = self.dds
        return sub_dds.del_subject_info(dds.DDS_TELLO_TOF)

    def sub_drone_info(self, freq=5, callback=None, *args, **kw):
        """ 订阅飞机高度、气压计、电机运行时间信息

        :param freq: 订阅数据的频率, 1HZ, 5HZ, 10HZ
        :param callback: 传入数据处理的回掉函数
        :param args: 回调函数参数
        :param kw: 回调函数参数
        :return: 返回订阅结果
        """
        sub = self.dds
        subject = TelloDroneInfoSubject()
        subject.freq = freq
        return sub.add_subject_info(subject, callback, args, kw)

    def unsub_drone_info(self):
        """ 取消订阅飞机高度、气压计、电机运行时间信息

        :return: 返回取消订阅结果
        """
        sub_dds = self.dds
        return sub_dds.del_subject_info(dds.DDS_TELLO_DRONE)

    def _sub_drone_all_status(self, freq=10, callback=None, *args, **kw):
        """ 订阅飞机所有状态数据

        :param freq: 订阅数据的频率, 1HZ, 5HZ, 10HZ
        :param callback: function:传入数据处理的回掉函数
        :param args: 回调函数参数
        :param kw: 回调函数参数
        :return: 状态订阅结果
        """
        sub = self.dds
        subject = TelloStatusSubject()
        subject.freq = freq
        return sub.add_subject_info(subject, callback, args, kw)

    def _unsub_drone_all_status(self):
        """ 取消订阅飞机所有状态

        :return: 取消状态订阅结果
        """
        sub_dds = self.dds
        return sub_dds.del_subject_info(dds.DDS_TELLO_ALL)

    def get_status(self, name):
        """ 获取飞机指定的状态

        :param name: string:需要获取的状态名，可列表["MID", "x", "y", "z", "mpry", "pitch", "roll", "yaw", "vgx", "vgy",
                            "vgz", "templ", "temph", "tof", "h", "bat", "baro", "time", "agx", "agy", "agz"]，详细介绍
                            参考SDK使用文档
        :return: name对应状态的数据值，DDS_PAD_MPRY_FLAG 对应状态的返回值为长度为3的list，分别代表的在飞机相对挑战卡的pitch、yaw、row值，
                 其他状态返回的都是float数据
        """
        return self._status_sub.get_status(name)


class Robot(RobotBase):
    """ RoboMaster EP 机甲大师 机器人 """
    _product = "EP"
    _sdk_host = ROBOT_DEFAULT_HOST

    def __init__(self, cli=None):
        self._config = config.ep_conf
        super().__init__(cli)
        self._sdk_conn = conn.SdkConnection()
        self._send_heart_beat_timer = None
        self._running = False
        self._initialized = False
        self._conn_type = config.DEFAULT_CONN_TYPE
        self._proto_type = config.DEFAULT_PROTO_TYPE
        self._ftp = conn.FtpConnection()
        self._modules = {}
        self._audio_id = 0

    def __del__(self):
        self.close()

        if self is None:
            return

        for name in list(self._modules.keys()):
            if self._modules[name]:
                del self._modules[name]

    def _start_heart_beat_timer(self):
        if self._running:
            self._send_heart_beat_msg()

    def _stop_heart_beat_timer(self):
        if self._send_heart_beat_timer:
            self._send_heart_beat_timer.cancel()
            self._send_heart_beat_timer = None

    def _send_heart_beat_msg(self):
        proto = protocol.ProtoSdkHeartBeat()
        msg = protocol.Msg(self.client.hostbyte, protocol.host2byte(9, 0), proto)
        try:
            self.client.send_msg(msg)
        except Exception as e:
            logger.warning("Robot: send heart beat msg failed, exception {0}".format(e))
        if self._running:
            self._send_heart_beat_timer = threading.Timer(1, self._send_heart_beat_msg)
            self._send_heart_beat_timer.start()

    @property
    def conf(self):
        return self._config

    @property
    def action_dispatcher(self):
        return self._action_dispatcher

    @property
    def ip(self):
        return self.client.remote_addr[0]

    @property
    def conn_type(self):
        return self._conn_type

    @property
    def proto_type(self):
        return self._proto_type

    @property
    def chassis(self):
        """ 获取底盘模块对象 """
        return self.get_module("Chassis")

    @property
    def gimbal(self):
        """ 获取云台模块对象 """
        return self.get_module("Gimbal")

    @property
    def blaster(self):
        """ 获取水弹枪模块对象 """
        return self.get_module("Blaster")

    @property
    def led(self):
        """ 获取灯效控制模块对象 """
        return self.get_module("Led")

    @property
    def vision(self):
        """ 获取智能识别模块对象 """
        return self.get_module("Vision")

    @property
    def battery(self):
        """ 获取电池模块对象 """
        return self.get_module("Battery")

    @property
    def camera(self):
        """ 获取相机模块对象 """
        return self.get_module("EPCamera")

    @property
    def robotic_arm(self):
        """ 获取机械臂模块对象 """
        return self.get_module("RoboticArm")

    @property
    def dds(self):
        return self.get_module("Subscriber")

    @property
    def servo(self):
        return self.get_module("Servo")

    @property
    def sensor(self):
        return self.get_module("DistanceSensor")

    @property
    def sensor_adaptor(self):
        return self.get_module("SensorAdaptor")

    @property
    def gripper(self):
        return self.get_module("Gripper")

    @property
    def armor(self):
        return self.get_module("Armor")

    @property
    def uart(self):
        return self.get_module("Uart")

    @property
    def ai_module(self):
        return self.get_module("AiModule")

    @property
    def is_initialized(self):
        return self._initialized

    def _scan_modules(self):
        _gimbal = gimbal.Gimbal(self)
        _chassis = chassis.Chassis(self)
        _camera = camera.EPCamera(self)
        _blaster = blaster.Blaster(self)
        _vision = vision.Vision(self)
        _dds = dds.Subscriber(self)
        _dds.start()
        _led = led.Led(self)
        _battery = battery.Battery(self)
        _servo = servo.Servo(self)
        _dis_sensor = sensor.DistanceSensor(self)
        _sensor_adaptor = sensor.SensorAdaptor(self)
        _robotic_arm = robotic_arm.RoboticArm(self)
        _gripper = gripper.Gripper(self)
        _armor = armor.Armor(self)
        _uart = uart.Uart(self)
        _uart.start()
        _ai_module = ai_module.AiModule(self)

        self._modules[_gimbal.__class__.__name__] = _gimbal
        self._modules[_chassis.__class__.__name__] = _chassis
        self._modules[_camera.__class__.__name__] = _camera
        self._modules[_blaster.__class__.__name__] = _blaster
        self._modules[_vision.__class__.__name__] = _vision
        self._modules[_dds.__class__.__name__] = _dds
        self._modules[_led.__class__.__name__] = _led
        self._modules[_battery.__class__.__name__] = _battery
        self._modules[_servo.__class__.__name__] = _servo
        self._modules[_robotic_arm.__class__.__name__] = _robotic_arm
        self._modules[_dis_sensor.__class__.__name__] = _dis_sensor
        self._modules[_sensor_adaptor.__class__.__name__] = _sensor_adaptor
        self._modules[_gripper.__class__.__name__] = _gripper
        self._modules[_armor.__class__.__name__] = _armor
        self._modules[_uart.__class__.__name__] = _uart
        self._modules[_ai_module.__class__.__name__] = _ai_module

    def get_module(self, name):
        """ 获取模块对象

        :param name: 模块名称，字符串，如：chassis, gimbal, led, blaster, camera, battery, vision, etc.
        :return: 模块对象
        """
        return self._modules[name]

    def initialize(self, conn_type=config.DEFAULT_CONN_TYPE, proto_type=config.DEFAULT_PROTO_TYPE, sn=None):
        """ 初始化机器人

        :param conn_type: 连接建立类型: ap表示使用热点直连；sta表示使用组网连接，rndis表示使用USB连接
        :param proto_type: 通讯方式: tcp, udp

        注意：如需修改默认连接方式，可在conf.py中指定DEFAULT_CONN_TYPE
        """
        self._proto_type = proto_type
        self._conn_type = conn_type
        if not self._client:
            logger.info("Robot: try to connection robot.")
            conn1 = self._wait_for_connection(conn_type, proto_type, sn)
            if conn1:
                logger.info("Robot: initialized with {0}".format(conn1))
                self._client = client.Client(9, 6, conn1)
            else:
                logger.info("Robot: initialized, try to use default Client.")
                try:
                    self._client = client.Client(9, 6)
                except Exception as e:
                    logger.error("Robot: initialized, can not create client, return, exception {0}".format(e))
                    return False

        try:
            self._client.start()
        except Exception as e:
            logger.error("Robot: Connection Create Failed.")
            raise e

        self._action_dispatcher = action.ActionDispatcher(self.client)
        self._action_dispatcher.initialize()
        # Reset Robot, Init Robot Mode.
        self._scan_modules()

        # set sdk mode and reset
        self._enable_sdk(1)
        self.reset()

        self._ftp.connect(self.ip)

        # start heart beat timer
        self._running = True
        self._start_heart_beat_timer()
        self._initialized = True
        return True

    def close(self):
        self._ftp.stop()
        if self._initialized:
            self._enable_sdk(0)
            self._stop_heart_beat_timer()
        for name in list(self._modules.keys()):
            if self._modules[name]:
                self._modules[name].stop()
        if self.client:
            self._client.stop()
        if self._sdk_conn:
            self._sdk_conn.close()
        self._initialized = False
        logger.info("Robot close")

    def _wait_for_connection(self, conn_type, proto_type, sn=None):
        result, local_addr, remote_addr = self._sdk_conn.request_connection(self._sdk_host, conn_type, proto_type, sn)
        if not result:
            logger.error("Robot: Connection Failed, Please Check Hareware Connections!!! "
                         "conn_type {0}, host {1}, target {2}.".format(conn_type, local_addr, remote_addr))
            return None
        return conn.Connection(local_addr, remote_addr, protocol=proto_type)

    def reset(self):
        """ 重置机器人到初始默认状态 """
        #  dds reset
        self._sub_node_reset()
        self._sub_add_node()
        self.set_robot_mode(mode=FREE)
        self.vision.reset()

    def reset_robot_mode(self):
        proto = protocol.ProtoSetRobotMode()
        proto._mode = 0
        msg = protocol.Msg(self._client.hostbyte, protocol.host2byte(9, 0), proto)

        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                return True
            return False
        except Exception as e:
            logger.warning("Robot: set_robot_mode, send_sync_msg exception {0}".format(str(e)))
            return False

    def set_robot_mode(self, mode=GIMBAL_LEAD):
        """ 设置机器人工作模式

        :param mode: 机器人工作模式: free表示自由模式；chassis_lead表示云台跟随底盘模式；gimbal_lead表示底盘跟随云台模式
        :return: bool: 调用结果
        """
        proto = protocol.ProtoSetRobotMode()
        if mode == FREE:
            proto._mode = 0
        elif mode == GIMBAL_LEAD:
            proto._mode = 1
            self.reset_robot_mode()
        elif mode == CHASSIS_LEAD:
            proto._mode = 2
            self.reset_robot_mode()
        else:
            logger.warning("Robot: set_robot_mode, unsupported mode = {0}".format(mode))
        msg = protocol.Msg(self._client.hostbyte, protocol.host2byte(9, 0), proto)

        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                return True
            return False
        except Exception as e:
            logger.warning("Robot: set_robot_mode, send_sync_msg exception {0}".format(str(e)))
            return False

    def get_robot_mode(self):
        """ 获取机器人工作模式

        :return: 自由模式返回free; 底盘跟随云台模式返回gimbal_lead；云台跟随底盘模式返回chassis_lead
        """
        mode = None
        msg = protocol.Msg(self._client.hostbyte, protocol.host2byte(9, 0), protocol.ProtoGetRobotMode())
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                if proto._retcode != 0:
                    raise Exception("get robot mode error.")
                    return None
                if proto._mode == 0:
                    mode = FREE
                elif proto._mode == 1:
                    mode = GIMBAL_LEAD
                elif proto._mode == 2:
                    mode = CHASSIS_LEAD
                else:
                    logger.info("Robot: get_robot_mode, unsupported mode:{0}".format(proto._mode))
                return mode
            else:
                raise Exception('get_robot_mode failed, resp is None.')
        except Exception as e:
            logger.warning("Robot: get_robot_mode, send_sync_msg e {0}".format(e))
            return None

    def _enable_sdk(self, enable=1):
        """ 进入和退出SDK模式

        :param enable: 进入或退出SDK模式，1 为进入SDK模式，0 为退出SDK模式
        """
        if not self.client:
            return

        proto = protocol.ProtoSetSdkMode()
        proto._enable = enable
        msg = protocol.Msg(self._client.hostbyte, protocol.host2byte(9, 0), proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                return True
            else:
                logger.warning("Robot: enable_sdk error.")
                return False
        except Exception as e:
            logger.warning("Robot: enable_sdk, send_sync_msg exception {0}".format(str(e)))
            return False

    def get_version(self):
        """ 获取机器人固件版本号信息

        :return: 版本字符串，如："01.01.0305"
        """
        proto = protocol.ProtoGetProductVersion()
        msg = protocol.Msg(self._client.hostbyte, protocol.host2byte(8, 1), proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                return proto._version
            else:
                logger.warning("Robot: get_version failed.")
                return None
        except Exception as e:
            logger.warning("Robot: get_version, send_sync_msg exception {0}".format(str(e)))
            return None

    def get_sn(self):
        """ 获取机器人硬件SN信息

        :return: 硬件SN字符串，如："3JKDH2T0011000"
        """
        proto = protocol.ProtoGetSn()
        msg = protocol.Msg(self._client.hostbyte, protocol.host2byte(8, 1), proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                if proto:
                    return proto._sn
                else:
                    return None
            else:
                logger.warning("Robot: get_sn failed.")
                return None
        except Exception as e:
            logger.warning("Robot: get_sn, send_sync_msg exception {0}".format(str(e)))
            return None

    def _sub_add_node(self):
        proto = protocol.ProtoSubscribeAddNode()
        proto._node_id = self._client.hostbyte
        msg = protocol.Msg(self._client.hostbyte, protocol.host2byte(9, 0), proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg is not None:
                return True
            else:
                logger.warning("Robot: enable_dds err.")
        except Exception as e:
            logger.warning("Robot: enable_dds, send_sync_msg exception {0}".format(str(e)))
            return False

    def _sub_node_reset(self):
        proto = protocol.ProtoSubNodeReset()
        proto._node_id = self._client.hostbyte
        msg = protocol.Msg(self._client.hostbyte, protocol.host2byte(9, 0), proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                return True
            else:
                logger.warning("Robot: reset dds node fail!")
                return False
        except Exception as e:
            logger.warning("Robot: reset_dds, send_sync_msg exception {0}".format(str(e)))
            return False

    def play_audio(self, filename):
        """ 播放本地音频文件

        :param filename: 播放音效的文件名，目前仅支持单通道，48KHz采样的wav格式文件
        :return: action对象
        """

        if not os.path.exists(filename):
            logger.error("Robot: play_audio, file {0} is not exists!".format(filename))
            return None

        self._audio_id = (self._audio_id + 1) % 10
        upload_file = "/python/sdk_audio_{0}.wav".format(self._audio_id)
        self._ftp.upload(filename, upload_file)
        logger.info("upload file {0} to target {1}".format(filename, upload_file))
        sound_id = 0xE0 + (self._audio_id % 10)
        return self.play_sound(sound_id, times=1)

    def play_sound(self, sound_id, times=1):
        """ 播放系统音效

        :param sound_id: 系统音效ID值
        :param times: 播放次数
        :return: action对象
        """
        action1 = RobotPlaySoundAction(sound_id, times)
        self._action_dispatcher.send_action(action1)
        return action1
