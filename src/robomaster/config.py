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


__all__ = ['LOCAL_IP_STR', 'ROBOT_IP_STR', 'DEFAULT_PROTO_TYPE']


DEFAULT_CONN_TYPE = "ap"

# 指定本机IP地址 示例：LOCAL_IP_STR = "192.168.2.100"
LOCAL_IP_STR = None
# 指定产品IP地址 示例：ROBOT_IP_STR = "192.168.2.120"
ROBOT_IP_STR = None
# 设置连接方式 "tcp" or "udp" 示例：DEFAULT_PROTO_TYPE = "tcp"
DEFAULT_PROTO_TYPE = "udp"


class Config:
    _name = "Unknown"
    _product = "Unknown"
    _cmd_addr = None
    _cmd_proto = "v1"
    _sdk_addr = None
    _video_stream_addr = None
    _video_stream_port = None
    _video_stream_proto = "tcp"
    _audio_stream_addr = None
    _audio_stream_port = None

    def __init__(self, name):
        self._name = name

    @property
    def default_cmd_addr_port(self):
        return self.default_cmd_addr[1]

    @property
    def product(self):
        return self._product

    @product.setter
    def product(self, val):
        self._product = val

    @property
    def default_robot_addr(self):
        return self._cmd_addr

    @default_robot_addr.setter
    def default_robot_addr(self, val):
        self._cmd_addr = val

    @property
    def cmd_proto(self):
        return self._cmd_proto

    @cmd_proto.setter
    def cmd_proto(self, val):
        self._cmd_proto = val

    @property
    def default_cmd_addr(self):
        return self._cmd_addr

    @default_cmd_addr.setter
    def default_cmd_addr(self, val):
        self._cmd_addr = val

    @property
    def default_sdk_addr(self):
        return self._sdk_addr

    @default_sdk_addr.setter
    def default_sdk_addr(self, val):
        self._sdk_addr = val

    @property
    def video_stream_addr(self):
        return self._video_stream_addr

    @video_stream_addr.setter
    def video_stream_addr(self, val):
        self._video_stream_addr = val

    @property
    def video_stream_port(self):
        return self._video_stream_port

    @video_stream_port.setter
    def video_stream_port(self, val):
        self._video_stream_port = val

    @property
    def video_stream_proto(self):
        return self._video_stream_proto

    @video_stream_proto.setter
    def video_stream_proto(self, val):
        self._video_stream_proto = val

    @property
    def audio_stream_addr(self):
        return self._audio_stream_addr

    @audio_stream_addr.setter
    def audio_stream_addr(self, val):
        self._audio_stream_addr = val

    @property
    def audio_stream_port(self):
        return self._audio_stream_port

    @audio_stream_port.setter
    def audio_stream_port(self, val):
        self._audio_stream_port = val


te_conf = Config("TelloEduConfig")
te_conf.product = "TelloEdu"
te_conf.default_cmd_addr = ('192.168.10.1', 8889)
te_conf.cmd_proto = "text"
te_conf.default_sdk_addr = ('0.0.0.0', 8890)
te_conf.video_stream_addr = ('0.0.0.0', 11111)
te_conf.video_stream_proto = "udp"

ep_conf = Config("RoboMasterEPConfig")
ep_conf.product = "RoboMasterEP"
ep_conf.cmd_proto = "v1"
ep_conf.video_stream_addr = ()
ep_conf.video_stream_proto = "tcp"
ep_conf.video_stream_port = 40921
ep_conf.audio_stream_addr = ()
ep_conf.audio_stream_proto = "tcp"
ep_conf.audio_stream_port = 40922

ROBOT_SDK_PORT_MIN = 10100
ROBOT_SDK_PORT_MAX = 10500
ROBOT_DEVICE_PORT = 20020
ROBOT_PROXY_PORT = 30030
ROBOT_BROADCAST_PORT = 40927

ROBOT_SN_LEN = 14

ROBOT_DEFAULT_RNDIS_ADDR = ('192.168.42.2', ROBOT_DEVICE_PORT)
ROBOT_DEFAULT_WIFI_ADDR = ('192.168.2.1', ROBOT_DEVICE_PORT)

ROBOT_DEFAULT_LOCAL_RNDIS_ADDR = ('192.168.42.3', ROBOT_SDK_PORT_MIN)
ROBOT_DEFAULT_LOCAL_WIFI_ADDR = ('192.168.2.23', ROBOT_SDK_PORT_MIN)
