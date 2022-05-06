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


import socket
import binascii
import traceback
import threading
import queue
import random
import time
import base64
from ftplib import FTP
from . import algo
from . import protocol
from . import logger
from . import config


CONNECTION_USB_RNDIS = 'rndis'
CONNECTION_WIFI_AP = 'ap'
CONNECTION_WIFI_STA = 'sta'
CONNECTION_PROTO_TCP = 'tcp'
CONNECTION_PROTO_UDP = 'udp'

__all__ = ['Connection']


def get_local_ip():
    """
    获取本地ip地址

    :return:返回本地ip
    """
    if config.LOCAL_IP_STR is not None:
        return config.LOCAL_IP_STR
    else:
        return socket.gethostbyname(socket.gethostname())


def get_sn_form_data(data):
    """ 从 data 中获取 sn 字段

    :param data:
    :return:
    """
    data = data.split(b'\x00')
    recv_sn = data[0]
    recv_sn = recv_sn.decode(encoding='utf-8')
    return recv_sn


def scan_robot_ip(user_sn=None, timeout=3.0):
    """ 扫描机器人的IP地址

    :return: 机器人的IP地址
    """
    try:
        # if user specifies SN
        if user_sn:
            # check the validity of input SN
            if config.ROBOT_SN_LEN != len(user_sn):
                raise Exception("The length of SN is invalid!")
            find_robot = False
            robot_ip = None
            start = time.time()
            while not find_robot:
                end = time.time()
                if end - start > timeout:
                    break
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.bind(("0.0.0.0", config.ROBOT_BROADCAST_PORT))
                s.settimeout(1)
                data, ip = s.recvfrom(1024)
                recv_sn = get_sn_form_data(data)
                logger.info("conn: scan_robot_ip, data:{0}, ip:{1}".format(recv_sn, ip))
                if recv_sn == user_sn:
                    robot_ip = ip[0]
                    find_robot = True
            if robot_ip:
                return robot_ip
            else:
                logger.error("Cannot found robot based on the specified SN!")
                return None
        else:
            # for compatibility with previous versions.
            config.ROBOT_BROADCAST_PORT = 45678
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.bind(("0.0.0.0", config.ROBOT_BROADCAST_PORT))
            s.settimeout(timeout)
            data, ip = s.recvfrom(1024)
            logger.info("conn: scan_robot_ip, data:{0}, ip:{1}".format(binascii.hexlify(data), ip))
            return ip[0]
    except Exception as e:
        logger.error("scan_robot_ip: exception {0}".format(e))
        return None


def scan_robot_ip_list(timeout=3.0):
    """ 扫描局域网内的机器人IP地址

    :param timeout: 超时时间
    :return: list，扫描到的小车IP列表
    """
    ip_list = []
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("0.0.0.0", config.ROBOT_BROADCAST_PORT))
    except Exception as e:
        logger.warning("scan_robot_ip_list: exception {0}".format(e))
        return ip_list

    start = time.time()
    while True:
        end = time.time()
        if end-start > timeout:
            break
        s.settimeout(1)
        try:
            data, ip = s.recvfrom(1024)
        except Exception as e:
            logger.warning("scan_robot_ip_list: socket recv, {0}".format(e))
            continue
        logger.info("conn: scan_robot_ip, data:{0}, ip:{1}".format(data[:-1].decode(encoding='utf-8'), ip))
        if ip[0] not in ip_list:
            ip_list.append(ip[0])
            logger.info("conn: scan_robot_ip_list, ip_list:{0}".format(ip_list))
            print("find robot sn:{0}, ip:{1}".format(str(data[:-1].decode(encoding='utf-8')), ip[0]))
    return ip_list


class BaseConnection(object):
    def __init__(self):
        self._sock = None
        self._buf = bytearray()
        self._host_addr = None
        self._target_addr = None
        self._proto_type = None
        self._proto = None

    def create(self):
        try:
            if self._proto_type == CONNECTION_PROTO_TCP:
                self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self._sock.bind(self._host_addr)
                self._sock.connect(self._target_addr)
                logger.info("TcpConnection, connect success {0}".format(self._host_addr))
            elif self._proto_type == CONNECTION_PROTO_UDP:
                self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self._sock.bind(self._host_addr)
                logger.info("UdpConnection, bind {0}".format(self._host_addr))
            else:
                logger.error("Connection: {0} unexpected connection param set".format(self._proto_type))
        except Exception as e:
            logger.warning("udpConnection: create, host_addr:{0}, exception:{1}".format(self._host_addr, e))
            raise

    def close(self):
        if self._sock:
            self._sock.close()

    def recv(self):
        try:
            if self._sock:
                data, host = self._sock.recvfrom(2048)
        except Exception as e:
            logger.warning("Connection: recv, exception:{0}".format(e))
            raise
        if data is None:
            logger.warning("Connection: recv buff None.")
            return None
        self._buf.extend(data)
        if len(self._buf) == 0:
            logger.warning("Connection: recv buff None.")
            return None

        msg, self._buf = protocol.decode_msg(self._buf, self._proto)
        if not msg:
            logger.warning("Connection: protocol.decode_msg is None.")
            return None
        else:
            if isinstance(msg, protocol.MsgBase):
                if not msg.unpack_protocol():
                    logger.warning("Connection: recv, msg.unpack_protocol failed, msg:{0}".format(msg))
            return msg

    def send(self, buf):
        try:
            if self._sock:
                self._sock.sendto(buf, self._target_addr)
        except Exception as e:
            logger.warning("Connection: send, exception:{0}".format(e))
            raise

    def send_self(self, buf):
        try:
            if self._sock:
                self._sock.sendto(buf, self._host_addr)
        except Exception as e:
            logger.warning("Connection: send, exception:{0}".format(e))
            raise


class Connection(BaseConnection):
    def __init__(self, host_addr, target_addr, proto="v1", protocol=CONNECTION_PROTO_UDP):
        self._host_addr = host_addr
        self._target_addr = target_addr
        self._proto = proto
        self._proto_type = protocol

        self._sock = None
        self._buf = bytearray()

    def __repr__(self):
        return "Connection, host:{0}, target:{1}".format(self._host_addr, self._target_addr)

    @property
    def target_addr(self):
        return self._target_addr

    @property
    def protocol(self):
        return self._proto


class SdkConnection(BaseConnection):
    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def __del__(self):
        self.close()

    def switch_remote_route(self, msg, remote_addr, timeout=5):
        if not self._sock:
            return False, None

        buf = msg.pack()
        try:
            self._sock.settimeout(timeout)
            self._sock.sendto(buf, remote_addr)
            self._sock.settimeout(timeout)
            data, address = self._sock.recvfrom(1024)
            logger.debug("SdkConnection, data:{0}.".format(binascii.hexlify(data)))
            resp_msg, data = protocol.decode_msg(data)
            resp_msg.unpack_protocol()
            if resp_msg:
                prot = resp_msg.get_proto()
                if prot._retcode == 0:
                    if prot._state == 0:
                        logger.info("SdkConnection: accept connection.")
                    if prot._state == 1:
                        logger.error("SdkConnection: reject connection, service is busy!")
                        return False, None
                    if prot._state == 2:
                        logger.info("SdkConnection: got config ip:{0}".format(prot._config_ip))
                        return True, prot._config_ip
        except socket.timeout:
            logger.error("SdkConnection: RECV TimeOut!")
            raise
        except Exception as e:
            logger.warning("SdkConnection: switch_remote_route, exception:{0}, Please Check Connections.".format(e))
            logger.warning("SdkConnection:{0}".format(traceback.format_exc()))
            return False, None

    def request_connection(self, sdk_host, conn_type=None, proto_type=None, sn=None):
        if conn_type is None:
            logger.error("Not Specific conn_type!")
        logger.info("CONN TYPE is {0}".format(conn_type))
        local_addr = None
        remote_addr = None
        proto = protocol.ProtoSetSdkConnection()
        if conn_type is CONNECTION_WIFI_AP:
            proto._connection = 0
            if config.LOCAL_IP_STR:
                proto._ip = config.LOCAL_IP_STR
            else:
                proto._ip = '0.0.0.0'
            logger.info("Robot: request_connection, ap get local ip:{0}".format(proto._ip))
            proto._port = random.randint(config.ROBOT_SDK_PORT_MIN, config.ROBOT_SDK_PORT_MAX)
            proxy_addr = (config.ROBOT_DEFAULT_WIFI_ADDR[0], config.ROBOT_PROXY_PORT)
            remote_addr = config.ROBOT_DEFAULT_WIFI_ADDR
            local_addr = (proto._ip, proto._port)
        elif conn_type is CONNECTION_WIFI_STA:
            proto._connection = 1
            local_ip = '0.0.0.0'
            if config.LOCAL_IP_STR:
                local_ip = config.LOCAL_IP_STR
            proto.ip = local_ip
            proto._port = random.randint(config.ROBOT_SDK_PORT_MIN, config.ROBOT_SDK_PORT_MAX)
            logger.info("SdkConnection: request_connection with ip:{0}, port:{1}".format(local_ip, proto._port))
            if config.ROBOT_IP_STR:
                remote_ip = config.ROBOT_IP_STR
            else:
                remote_ip = scan_robot_ip(sn)
                if not remote_ip:
                    return False, None, None
            local_addr = (local_ip, proto._port)
            remote_addr = (remote_ip, config.ROBOT_DEVICE_PORT)
            proxy_addr = (remote_ip, config.ROBOT_PROXY_PORT)
        elif conn_type is CONNECTION_USB_RNDIS:
            proto._connection = 2
            proto._ip = config.ROBOT_DEFAULT_LOCAL_RNDIS_ADDR[0]
            proto._port = random.randint(config.ROBOT_SDK_PORT_MIN,
                                         config.ROBOT_SDK_PORT_MAX)
            proxy_addr = (config.ROBOT_DEFAULT_RNDIS_ADDR[0], config.ROBOT_PROXY_PORT)
            local_addr = (config.ROBOT_DEFAULT_LOCAL_RNDIS_ADDR[0], proto._port)
            remote_addr = config.ROBOT_DEFAULT_RNDIS_ADDR
        logger.info("SdkConnection: request_connection, local addr {0}, remote_addr {1}, "
                    "proxy addr {2}".format(local_addr, remote_addr, proxy_addr))
        proto._host = sdk_host
        if proto_type == CONNECTION_PROTO_TCP:
            proto._protocol = 1
        else:
            proto._protocol = 0

        msg = protocol.Msg(sdk_host, protocol.host2byte(9, 0), proto)
        try:
            result, local_ip = self.switch_remote_route(msg, proxy_addr)
            if result:
                if config.LOCAL_IP_STR:
                    local_ip = config.LOCAL_IP_STR
                local_addr = (local_ip, proto._port)
            else:
                return False, local_addr, remote_addr
            return result, local_addr, remote_addr
        except socket.timeout:
            logger.warning("SdkConnection: Connection Failed, please check hareware connections!!!")
            return False, local_addr, remote_addr
        except Exception as e:
            logger.warning("SdkConnection: request_connection, switch_remote_route exception {0}".format(str(e)))
            return False, local_addr, remote_addr


class StreamConnection(object):

    def __init__(self):
        self._sock = None
        self._sock_queue = queue.Queue(32)
        self._sock_recv = None
        self._recv_count = 0
        self._receiving = False

    def __del__(self):
        if self._sock:
            self._sock.close()

    def connect(self, addr, ip_proto="tcp"):
        try:
            if ip_proto == "tcp":
                self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self._sock.settimeout(3)
                logger.info("StreamConnection: try to connect {0}".format(addr))
                time.sleep(0.1)
                self._sock.connect(addr)
            elif ip_proto == "udp":
                self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self._sock.bind(addr)
            else:
                logger.error("StreamConnection: ip_proto:{0} not supperted.".format(ip_proto))
        except Exception as e:
            logger.error("StreamConnection: connect addr {0}, exception {1}".format(addr, e))
            return False
        self._sock_recv = threading.Thread(target=self._recv_task)
        self._sock_recv.start()
        logger.info("StreamConnection {0} successfully!".format(addr))
        return True

    def disconnect(self):
        self._receiving = False
        self._sock_queue.put(None)
        if self._sock_recv:
            self._sock_recv.join()
        self._sock.close()
        self._sock_queue.queue.clear()
        self._recv_count = 0
        logger.info("StreamConnection: disconnected")

    def _recv_task(self):
        self._receiving = True
        logger.info("StreamConnection: _recv_task, Start to receiving Data...")
        while self._receiving:
            try:
                if self._sock is None:
                    break
                data, addr = self._sock.recvfrom(4096)
                if not self._receiving:
                    break
                self._recv_count += 1
                if self._sock_queue.full():
                    logger.warning("StreamConnection: _recv_task, sock_data_queue is full.")
                    self._sock_queue.get()
                else:
                    logger.debug("StreamConnection: _recv_task, recv {0}, len:{1}, data:{2}".format(
                                  self._recv_count, len(data), data))
                    self._sock_queue.put(data)
            except socket.timeout:
                logger.warning("StreamConnection: _recv_task， recv data timeout!")
                continue
            except Exception as e:
                logger.error("StreamConnection: recv, exceptions:{0}".format(e))
                self._receiving = False
                return

    def read_buf(self, timeout=2):
        try:
            buf = self._sock_queue.get(timeout=timeout)
            return buf
        except Exception as e:
            logger.warning("StreamConnection: read_buf, exception {0}".format(e))
            return None


class ConnectionHelper:
    def __init__(self):
        self._appid = str(random.randint(10000, 20000))
        self._ssid = ""
        self._password = ""
        self._sta_info = protocol.STAConnInfo()

    def build_qrcode_string(self, ssid="", password=""):
        self._ssid = ssid
        self._password = password
        self._sta_info.set_info(ssid, password, self._appid)
        buf = self._sta_info.pack()
        buf = algo.simple_encrypt(buf)
        return bytes.decode(base64.b64encode(buf), encoding='utf-8')

    def get_qrcode_string(self):
        buf = self._sta_info.pack()
        buf = algo.simple_encrypt(buf)
        return bytes.decode(base64.b64encode(buf), encoding='utf-8')

    def wait_for_connection(self):
        try:
            config.ROBOT_BROADCAST_PORT = 45678
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.bind(("0.0.0.0", config.ROBOT_BROADCAST_PORT))
            s.settimeout(360)
            logger.info("waiting for connections...")
            while True:
                data, ip = s.recvfrom(1024)
                if data:
                    decode_buf = algo.simple_encrypt(data)
                    conn_info = protocol.STAConnInfo()
                    if conn_info.unpack(decode_buf):
                        if conn_info._recv_appid == self._appid:
                            s.sendto(self._appid.encode(encoding='utf-8'), ip)
                            return True
                        else:
                            logger.debug("skip data!")
                    else:
                        logger.warning("wait_for_connection unpack failed!")
        except Exception as e:
            logger.warning("recv_task: exception {0}".format(e))
            return False


class FtpConnection:

    def __init__(self):
        self._ftp = FTP()
        self._target = None
        self._bufsize = 1024
        self._ftp.set_debuglevel(0)

    def connect(self, ip):
        self._target = ip
        logger.info("FtpConnection: connect ip: {0}".format(ip))
        return self._ftp.connect(ip, 21)

    def upload(self, src_file, target_file):
        try:
            fp = open(src_file, 'rb')
            self._ftp.storbinary("STOR " + target_file, fp, self._bufsize)
            fp.close()
        except Exception as e:
            logger.warning("FtpConnection: upload e {0}".format(e))

    def stop(self):
        if self._ftp:
            self._ftp.close()
