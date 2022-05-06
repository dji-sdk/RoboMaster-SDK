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
import random
import struct
import binascii
from abc import abstractmethod
from . import algo
from . import logger


""" struct 速查表
format  C               Python      size
x       pad byte        no value    0
c       char            string 1    1
b       signed char     integer     1
B       unsigned char   integer     1
?       bool            bool        1
h       short           integer     2
H       unsigned short  integer     2
i       int             integer     4
I       unsigned int    integer     4
l       long            integer     4
L       unsigned long   long        4
q       long long       long        8
Q       unsigned lonlon long        8
f       float           float       4
d       double          float       8
s       char[]          string
p       char[]          string
P       void*           long
"""

__all__ = ['Msg', 'TextMsg']

# 默认的 ID 取值范围
RM_SDK_FIRST_SEQ_ID = 10000
RM_SDK_LAST_SEQ_ID = 20000

# 协议 ACK 类型
DUSS_MB_ACK_NO = 0
DUSS_MB_ACK_NOW = 1
DUSS_MB_ACK_FINISH = 2

# 协议加密类型
DUSS_MB_ENC_NO = 0
DUSS_MB_ENC_AES128 = 1
DUSS_MB_ENC_CUSTOM = 2

# 协议类型
DUSS_MB_TYPE_REQ = 0
DUSS_MB_TYPE_PUSH = 1


def host2byte(host, index):
    return index * 32 + host


def byte2host(b):
    return (b & 0x1f), (b >> 5)


def make_proto_cls_key(cmdset, cmdid):
    return cmdset * 256 + cmdid


# registered protocol dict.
registered_protos = {}


class _AutoRegisterProto(type):
    """ help to automatically register Proto Class where ever they're defined """

    def __new__(mcs, name, bases, attrs, **kw):
        return super().__new__(mcs, name, bases, attrs, **kw)

    def __init__(cls, name, bases, attrs, **kw):
        super().__init__(name, bases, attrs, **kw)
        if name == 'ProtoData':
            return
        key = make_proto_cls_key(attrs['_cmdset'], attrs['_cmdid'])
        if key in registered_protos.keys():
            raise ValueError("Duplicate proto class %s" % (name))
        registered_protos[key] = cls


class ProtoData(metaclass=_AutoRegisterProto):
    _cmdset = None
    _cmdid = None
    _cmdtype = DUSS_MB_TYPE_REQ
    _req_size = 0
    _resp_size = 0

    def __init__(self, **kwargs):
        self._buf = None
        self._len = None

    def __repr__(self):
        return "<{0} cmset:0x{1:2x}, cmdid:0x{2:02x}>".format(self.__class__.__name__, self._cmdset, self._cmdid)

    @property
    def cmdset(self):
        return self._cmdset

    @cmdset.setter
    def cmset(self, value):
        self._cmdset = value

    @property
    def cmdid(self):
        return self._cmdid

    @cmdid.setter
    def cmdid(self, value):
        self._cmdid = value

    @property
    def cmdkey(self):
        if self._cmdset is not None and self._cmdid is not None:
            return self._cmdset * 256 + self._cmdid
        else:
            return None

    @abstractmethod
    def pack_req(self):
        """ 协议对象打包发送数据为字节流

        :return: 字节流数据
        """
        return b''

    # @abstractmethod
    def unpack_req(self, buf, offset=0):
        """ 从字节流解包

        :param buf：字节流数据
        :param offset：字节流数据偏移量
        :return：True 解包成功；False 解包失败
        """
        return True

    # @abstractmethod
    def pack_resp(self):
        """ 协议对象打包

        :return：字节流数据
        """
        pass

    # return True when retcode == zero
    # return False when restcode is not zero
    # raise exceptions when internal error occur.
    def unpack_resp(self, buf, offset=0):
        """ 从字节流解包为返回值和相关属性

        :param buf：字节流数据
        :param offset：字节流数据偏移量
        :return: bool: 调用结果
        """
        self._retcode = buf[offset]
        if self._retcode == 0:
            return True
        else:
            return False


class MsgBase(object):
    _next_seq_id = RM_SDK_FIRST_SEQ_ID

    def __init__(self):
        pass


class Msg(MsgBase):

    def __init__(self, sender=0, receiver=0, proto=None):
        self._len = 13  # default length, msg header and crc.
        self._sender = sender
        self._receiver = receiver
        self._attri = 0
        self._cmdset = None
        self._cmdid = None

        self._is_ack = False  # True or False
        self._need_ack = 2  # 0 for no need, 1 for ack now, 2 for need when finish.
        if self.__class__._next_seq_id == RM_SDK_LAST_SEQ_ID:
            self.__class__._next_seq_id = RM_SDK_FIRST_SEQ_ID
        else:
            self.__class__._next_seq_id += 1
        self._seq_id = self._next_seq_id
        self._proto = proto
        if self._proto:
            self._cmdset = self._proto.cmdset
            self._cmdid = self._proto.cmdid
            if self._proto._cmdtype == DUSS_MB_TYPE_PUSH:
                self._need_ack = 0
        self._buf = None

    def __repr__(self):
        return "<Msg sender:0x{0:02x}, receiver:0x{1:02x}, cmdset:0x{2:02x}, cmdid:0x{3:02x}, len:{4:d}, \
seq_id:{5:d}, is_ack:{6:d}, need_ack:{7:d}>".format(self._sender, self._receiver, self._cmdset, self._cmdid,
                                                    self._len, self._seq_id, self._is_ack, self._need_ack)

    @property
    def cmdset(self):
        return self._cmdset

    @property
    def cmdid(self):
        return self._cmdid

    @property
    def is_ack(self):
        return self._is_ack

    @property
    def receiver(self):
        host, index = byte2host(self._receiver)
        return "{0:02d}{1:02d}".format(host, index)

    @property
    def sender(self):
        host, index = byte2host(self._sender)
        return "{0:02d}{1:02d}".format(host, index)

    def pack(self, is_ack=False):
        """ Msg 消息打包

        :param is_ack: bool: 是否是ack消息
        :return: bytearray，消息字节流
        """
        self._len = 13
        try:
            if self._proto:
                data_buf = b''
                if is_ack:
                    self._neek_ack = False
                    data_buf = self._proto.pack_resp()
                else:
                    self._neek_ack = (self._proto._cmdtype == DUSS_MB_TYPE_REQ)
                    data_buf = self._proto.pack_req()
                self._len += len(data_buf)
        except Exception as e:
            logger.warning("Msg: pack, cmset:0x{0:02x}, cmdid:0x{1:02x}, proto: {2}, "
                           "exception {3}".format(self.cmdset, self.cmdid, self._proto.__class__.__name__, e))

        self._buf = bytearray(self._len)
        self._buf[0] = 0x55
        self._buf[1] = self._len & 0xff
        self._buf[2] = (self._len >> 8) & 0x3 | 4
        crc_h = algo.crc8_calc(self._buf[0:3])

        # attri = is_ack|need_ack|enc
        self._attri = 1 << 7 if self._is_ack else 0
        self._attri += self._need_ack << 5
        self._buf[3] = crc_h
        self._buf[4] = self._sender
        self._buf[5] = self._receiver
        self._buf[6] = self._seq_id & 0xff
        self._buf[7] = (self._seq_id >> 8) & 0xff
        self._buf[8] = self._attri

        if self._proto:
            self._buf[9] = self._proto.cmdset
            self._buf[10] = self._proto.cmdid
            self._buf[11:11 + len(data_buf)] = data_buf
        else:
            raise Exception("Msg: pack Error.")

        # calc whole msg crc16
        crc_m = algo.crc16_calc(self._buf[0:self._len - 2])
        struct.pack_into('<H', self._buf, self._len - 2, crc_m)

        logger.debug("Msg: pack, len:{0}, seq_id:{1}, buf:{2}".format(
            self._len, self._seq_id, binascii.hexlify(self._buf)))
        return self._buf

    # unpack proto after recv msg, raise excpetion when error occur.
    def unpack_protocol(self):
        """ 从自身的buf数据解码协议及协议内容。
        """
        key = make_proto_cls_key(self._cmdset, self._cmdid)
        if key in registered_protos.keys():
            self._proto = registered_protos[key]()
            try:
                if self._is_ack:
                    if not self._proto.unpack_resp(self._buf):
                        logger.warning("Msg: unpack_protocol, msg:{0}".format(self))
                        return False
                else:
                    if not self._proto.unpack_req(self._buf):
                        logger.warning("Msg: unpack_protocol, msg:{0}".format(self))
                        return False
                return True
            except Exception as e:
                logger.warning("Msg: unpack_protocol, {0} failed e {1}".format(self._proto.__class__.__name__, e))
                raise
        else:
            logger.info("Msg: unpack_protocol, cmdset:0x{0:02x}, cmdid:0x{1:02x}, class is not registerin registered_\
protos".format(self._cmdset, self._cmdid))
            pass
        logger.warning("Msg: unpack_protocol, not registered_protocol, cmdset:0x{0:02x}, cmdid:0x{1:02x}".format(
            self._cmdset, self._cmdid))
        return False

    def get_proto(self):
        return self._proto


class TextMsg(MsgBase):
    IS_DDS_FLAG = ";mpry:"

    def __init__(self, proto=None):
        self._buf = None
        self._len = 0
        self._need_ack = 0
        if self.__class__._next_seq_id == RM_SDK_LAST_SEQ_ID:
            self.__class__._next_seq_id = RM_SDK_FIRST_SEQ_ID
        else:
            self.__class__._next_seq_id += 1
        self._seq_id = self._next_seq_id
        self._proto = proto

    def __repr__(self):
        return "<{0}, {1}>".format(self.__class__.__name__, self._proto.resp)

    def pack(self):
        if self._proto:
            data_buf = self._proto.pack_req()
        """pack the proto to msg"""
        self._buf = data_buf
        return self._buf

    def unpack_protocol(self):
        self._proto = TextProtoDrone()
        if not self._proto.unpack_resp(self._buf):
            logger.warining("TextMsg: unpack_protocol, msg:{0}".format(self))
            return False
        return True

    def get_proto(self):
        return self._proto

    def get_buf(self):
        return self._buf


def decode_msg(buff, protocol="v1"):
    if protocol == "v1":
        if len(buff) < 4:
            logger.info("decode_msg, recv buf is not enouph.")
            return None, buff

        if buff[0] != 0x55:
            logger.warning("decode_msg, magic number is invalid.")
            return None, buff

        if algo.crc8_calc(buff[0:3]) != buff[3]:
            logger.warning("decode_msg, crc header check failed.")
            return None, buff

        msg_len = (buff[2] & 0x3) * 256 + buff[1]
        if len(buff) < msg_len:
            logger.warning("decode_msg, msg data is not enough, msg_len:{0}, buf_len:{1}".format(msg_len, len(buff)))
            return None, buff

        # unpack from byte array.
        msg = Msg(buff[9], buff[10])
        msg._len = msg_len
        msg._seq_id = buff[7] * 256 + buff[6]
        msg._attri = buff[8]
        msg._sender = buff[4]
        msg._receiver = buff[5]
        msg._cmdset = int(buff[9])
        msg._cmdid = int(buff[10])
        msg._is_ack = msg._attri & 0x80 != 0
        msg._need_ack = (msg._attri & 0x60) >> 5
        msg._buf = buff[11:msg._len - 2]
        left_buf = buff[msg_len:]
        return msg, left_buf

    elif protocol == "text":
        # unpack
        msg = TextMsg()
        # filter out '\0xcc'
        if buff[0] == 204:
            logger.warning("decode_msg: recv invalid data, buff {0}".format(buff))
            return None, bytearray()
        else:
            msg._buf = buff.decode(encoding='utf-8')
            msg._len = len(msg._buf)
            return msg, bytearray()


################################################################################
class ProtoGetVersion(ProtoData):
    _cmdset = 0
    _cmdid = 1
    _resp_size = 30

    def __init__(self):
        self._aa = 0
        self._bb = 1
        self._cc = 0
        self._dd = 0
        self._build = 1
        self._version = 0
        self._minor = 1
        self._major = 0
        self._cmds = 0
        self._rooback = 0
        self._retcode = 0

    def pack_req(self):
        return b''

    def unpack_resp(self, buf, offset=0):
        if len(buf) < self._resp_size:
            raise Exception("buf length is not enouph.")

        self._retcode = buf[0]
        if self._retcode != 0:
            return False
        self._aa = buf[0]
        self._bb = buf[1]
        self._cc = buf[2]
        self._dd = buf[3]
        return True


class ProtoGetProductVersion(ProtoData):
    _cmdset = 0
    _cmdid = 0x4f
    _resp_size = 9

    def __init__(self):
        self._file_type = 4
        self._version = None

    def pack_req(self):
        buf = bytearray(self._resp_size)
        buf[0] = self._file_type
        buf[5] = 0xff
        buf[6] = 0xff
        buf[7] = 0xff
        buf[8] = 0xff
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        if self._retcode == 0:
            cc, bb, aa = struct.unpack_from("<HBB", buf, 9)
            self._version = "{0:02d}.{1:02d}.{2:04d}".format(aa, bb, cc)
            return True
        else:
            self._version = None
            logger.warning("ProtoGetProductVersion, unpack_resp, retcode {0}".format(self._retcode))
            return False


class ProtoGetSn(ProtoData):
    _cmdset = 0x0
    _cmdid = 0x51
    _req_size = 1

    def __init__(self):
        self._type = 1

    def pack_req(self):
        buf = bytearray(self._req_size)
        buf[0] = self._type
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[offset]
        if self._retcode == 0:
            self._length = buf[offset + 1]
            self._sn = buf[offset + 3:self._length + offset + 3].decode('utf-8', 'ignore')
            return True
        else:
            return False


class ProtoTakePhoto(ProtoData):
    _cmdset = 0x2
    _cmdid = 0x1
    _req_size = 1

    def __init__(self):
        self._type = 1

    def pack_req(self):
        buf = bytearray(self._req_size)
        buf[0] = self._type
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        if self._retcode == 0:
            return True
        else:
            return False


class ProtoSetZoom(ProtoData):
    _cmdset = 0x2
    _cmdid = 0x34
    _req_size = 5

    def __init__(self):
        self._digital_enable = 1
        self._digital_zoom = 1.0
        self._digital_type = 1
        self._digital_value = 1

    def pack_req(self):
        buf = bytearray(self._req_size)
        buf[0] = self._digital_enable << 3 | self._digital_type
        struct.pack_into("<h", buf, 4, self._digital_value)
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        if self._retcode == 0:
            return True
        else:
            return False


class ProtoGetZoom(ProtoData):
    _cmdset = 0x2
    _cmdid = 0x35

    def __init__(self):
        pass

    def pack_req(self):
        return b''

    def unpack_resp(self, buf, offset=0):
        return True


class ProtoSetWhiteBalance(ProtoData):
    _cmdset = 0x2
    _cmdid = 0x2c
    _req_size = 5

    def __init__(self):
        self._type = 0  # 0 for auto, 6 for manual
        self._temp1 = 0
        self._temp2 = 0
        self._tint = 0

    def pack_req(self):
        buf = bytearray(self._req_size)
        buf[0] = self._type
        buf[1] = self._temp1
        buf[2] = self._temp2
        struct.pack_into("<h", buf, 3, self._tint)
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        if self._retcode == 0:
            return True
        else:
            return False


class ProtoFcSubInfoReq(ProtoData):
    _cmdset = 0x3
    _cmdid = 0x14
    _req_size = 5

    def __init__(self):
        self._bagid = 0
        self._freq = 10
        self._timestamp = 0
        self.data_num = 0
        self._uuid_list = []

    def pack_req(self):
        buf = bytearray(self._req_size + len(self.data_num * 4))
        buf[0] = self._bagid
        struct.pack_into("<H", buf, 1, self._freq)
        buf[3] = self._timestamp
        buf[4] = self._data_num
        for i, uuid in enumerate(self._uuid_list):
            struct.pack_into("<I", buf, 5 + i * 4, uuid)
        logger.debug("ProtoFcSubInfoReq, pack_req buf {0}".format(binascii.hexlify(buf)))
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        if self._retcode == 0:
            return True
        else:
            logger.warning("ProtoFcSubInfoReq: unpack_resp, retcode:{0}".format(self._retcode))
            return False


class ProtoChassisStickOverlay(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0x28
    _req_size = 1

    def __init__(self):
        self._mode = 0

    def pack_req(self):
        buf = bytearray(self._req_size)
        buf[0] = self._mode
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[offset]
        if self._retcode == 0:
            return True
        else:
            logger.warning("ProtoChassisStickOverlay: unpack_resp, retcode:{0}".format(self._retcode))
            return False


class ProtoGimbalCtrlSpeed(ProtoData):
    _cmdset = 0x4
    _cmdid = 0xc
    _req_size = 8
    _cmdtype = DUSS_MB_TYPE_PUSH

    def __init__(self):
        self._yaw_speed = 0
        self._roll_speed = 0
        self._pitch_speed = 0
        self._ctrl_byte = 0xdc
        self._ctrl_byte_extend = 0
        self._err_yaw_limit = 0
        self._err_roll_limit = 0
        self._err_pitch_limit = 0
        self._auth = 0
        self._prior = 0

    def pack_req(self):
        buf = bytearray(self._req_size)
        struct.pack_into("<hhh", buf, 0, self._yaw_speed, self._roll_speed, self._pitch_speed)
        buf[6] = self._ctrl_byte
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[offset]
        if self._retcode == 0:
            return True
        else:
            logger.warning("ProtoGimbalCtrlSpeed: unpack_resp, retcode:{0}".format(self._retcode))
            return False


class ProtoArmorHitEvent(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0x2
    _resp_size = 0

    def __init__(self):
        self._index = 0
        self._type = 0
        self._mic_value = 0
        self._acc_value = 0
        self._data_buf = None

    def pack_req(self):
        return b''

    def unpack_req(self, buf, offset=0):
        self._index = buf[0] >> 4
        self._type = buf[0] & 0xf
        self._mic_value, self._mic_len = struct.unpack('<HH', buf[1:])
        self._data_buf = [self._index, self._type, self._mic_value]
        return True


class ProtoIrHitEvent(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0x10
    _resp_size = 0

    def __init__(self):
        self._skill_id = 0
        self._role_id = 0
        self._recv_dev = 0
        self._recv_ir_pin = 0
        self._data_buf = None

    def pack_req(self):
        return b''

    def unpack_req(self, buf, offset=0):
        self._role_id = buf[0] >> 4
        self._skill_id = buf[0] & 0xf
        self._recv_dev, self._recv_ir_pin = struct.unpack('<BB', buf[1:])
        self._data_buf = [self._skill_id, self._role_id, self._recv_dev, self._recv_ir_pin]
        return True


class ProtoGameMsgEvent(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0xd6
    _resp_size = 0

    def __init__(self):
        self._len = 0
        self._buf = []
        self._data_buf = None

    def pack_req(self):
        return b''

    def unpack_req(self, buf, offset=0):
        self._len = buf[1]
        self._buf = buf[2:]
        self._data_buf = [self._len, self._buf]
        return True


class ProtoSetArmorParam(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0x7
    _resp_size = 19

    def __init__(self):
        self._armor_mask = 0
        self._voice_energy_en = 0
        self._voice_energy_ex = 0
        self._voice_len_max = 0
        self._voice_len_min = 0
        self._voice_len_silence = 0
        self._voice_peak_count = 0
        self._voice_peak_min = 0
        self._voice_peak_ave = 0
        self._voice_peak_final = 0

    def pack_req(self):
        buf = bytearray(self._resp_size)
        struct.pack_into('<BHHHHHHHHH', buf, 0, self._armor_mask, self._voice_energy_en,
                         self._voice_energy_ex, self._voice_len_max, self._voice_len_min,
                         self._voice_len_silence, self._voice_peak_count, self._voice_peak_min,
                         self._voice_peak_ave, self._voice_peak_final)
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        if self._retcode == 0:
            return True
        else:
            return False


class ProtoChassisWheelSpeed(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0x26
    _req_size = 4

    def __init__(self):
        self._w1_spd = 0
        self._w2_spd = 0
        self._w3_spd = 0
        self._w4_spd = 0

    def pack_req(self):
        buf = bytearray(self._req_size)
        buf[0] = self._w1_spd
        buf[1] = self._w2_spd
        buf[2] = self._w3_spd
        buf[3] = self._w4_spd
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        if self._retcode == 0:
            return True
        else:
            return False


class ProtoSetSystemLed(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0x33
    _req_size = 15

    def __init__(self):
        self._comp_mask = 0x3f
        self._led_mask = 0xff
        self._ctrl_mode = 0
        self._effect_mode = 0
        self._r = 0xff
        self._g = 0xff
        self._b = 0xff
        self._loop = 0
        self._t1 = 100
        self._t2 = 100

    def pack_req(self):
        buf = bytearray(self._req_size)
        struct.pack_into("<I", buf, 0, self._comp_mask)
        struct.pack_into("<h", buf, 4, self._led_mask)
        buf[6] = self._ctrl_mode << 4 | self._effect_mode
        buf[7] = self._r
        buf[8] = self._g
        buf[9] = self._b
        buf[10] = self._loop
        struct.pack_into("<hh", buf, 11, self._t1, self._t2)
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        if self._retcode == 0:
            return True
        else:
            return False


class ProtoSetRobotMode(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0x46
    _req_size = 1

    def __init__(self):
        self._mode = 1

    def pack_req(self):
        buf = bytearray(self._req_size)
        buf[0] = self._mode
        return buf

    def unpack_resp(self, buff, offset=0):
        self._retcode = buff[0]
        if self._retcode == 0:
            return True
        else:
            return False


class ProtoGetRobotMode(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0x47

    def __init__(self):
        self._mode = 0

    def pack_req(self):
        return b''

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[offset]
        if self._retcode == 0:
            self._mode = buf[offset + 1]
            return True
        else:
            return False


class ProtoBlasterFire(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0x51
    _req_size = 1

    def __init__(self):
        self._type = 0
        self._times = 0

    def pack_req(self):
        buf = bytearray(self._req_size)
        buf[0] = self._type << 4 | self._times
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        if self._retcode == 0:
            return True
        else:
            return False


class ProtoBlasterSetLed(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0x55
    _req_size = 9
    _cmdtype = DUSS_MB_TYPE_PUSH

    def __init__(self):
        self._mode = 7
        self._effect = 0
        self._r = 0xff
        self._g = 0xff
        self._b = 0xff
        self._times = 1
        self._t1 = 100
        self._t2 = 100

    def pack_req(self):
        buf = bytearray(self._req_size)
        buf[0] = self._mode << 4 | self._effect
        buf[1] = self._r
        buf[2] = self._g
        buf[3] = self._b
        buf[4] = self._times
        struct.pack_into("<HH", buf, 5, self._t1, self._t2)
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        if self._retcode == 0:
            return True
        else:
            return False


class ProtoSetSdkMode(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0xd1
    _req_size = 1

    def __init__(self):
        self._enable = 1

    def pack_req(self):
        buf = bytearray(self._req_size)
        buf[0] = self._enable
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[offset]
        if self._retcode == 0:
            return True
        else:
            return False


class ProtoStreamCtrl(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0xd2
    _req_size = 3

    def __init__(self):
        self._ctrl = 1
        self._conn_type = 0
        self._state = 1
        self._resolution = 0

    def pack_req(self):
        buf = bytearray(self._req_size)
        buf[0] = self._ctrl
        buf[1] = self._conn_type << 4 | self._state
        buf[2] = self._resolution
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        if self._retcode == 0:
            return True
        else:
            return False


class ProtoSetSdkConnection(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0xd4
    _req_size = 10

    def __init__(self):
        self._control = 0
        self._host = 0
        self._connection = 0
        self._protocol = 0
        self._ip = '0.0.0.0'
        self._port = 10010

    def pack_req(self):
        buf = bytearray(self._req_size)
        buf[0] = self._control
        buf[1] = self._host
        buf[2] = self._connection
        buf[3] = self._protocol
        ip_bytes = bytes(map(int, self._ip.split('.')))
        buf[4:8] = ip_bytes
        struct.pack_into("<H", buf, 8, self._port)
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        if self._retcode == 0:
            self._state = buf[1]
            if self._state == 2:
                self._config_ip = "{0:d}.{1:d}.{2:d}.{3:d}".format(buf[2], buf[3], buf[4], buf[5])
            return True
        else:
            return False


class ProtoSdkHeartBeat(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0xd5
    _req_size = 0

    def __init__(self):
        pass

    def pack_req(self):
        return b''

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        if self._retcode == 0:
            return True
        else:
            return False


class ProtoAiModuleEvent(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0xea
    _resp_size = 0

    def __init__(self):
        self._id = 0
        self._x = 0
        self._y = 0
        self._w = 0
        self._h = 0
        self._c = 0
        self._info = []
        self._num = 0
        self._data_buf = None

    def pack_req(self):
        return b''

    def unpack_req(self, buf, offset=0):
        self._len = len(buf)-15
        self._num = round(self._len/8)
        for i in range(0, self._num):
            self._id, self._x, self._y, self._w, self._h, self._c = struct.unpack('<BHBHBB', buf[13+i*8:21+i*8])
            self._info.append([self._id, self._x, self._y, self._w, self._h, self._c])
        self._data_buf = self._num, self._info
        return True


class ProtoUwbModuleEvent(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0xdb
    _resp_size = 0

    def __init__(self):
        self._id = 0
        self._pox_x = 0
        self._pox_y = 0
        self._pox_z = 0
        self._vel_x = 0
        self._vel_y = 0
        self._vel_z = 0
        self._eop_x = 0
        self._eop_y = 0
        self._eop_z = 0
        self._data_buf = None

    def pack_req(self):
        return b''

    def unpack_req(self, buf, offset=0):
        self._id, self._pox_x, self._pox_y, self._pox_z, self._vel_x, self._vel_y,\
            self._vel_z, self._eop_x, self._eop_y, self._eop_z = struct.unpack('<BffffffBBB', buf)
        self._data_buf = [self._id, self._pox_x, self._pox_y, self._pox_z, self._vel_x, self._vel_y,
                          self._vel_z, self._eop_x, self._eop_y, self._eop_z]
        return True


class ProtoGimbalSetWorkMode(ProtoData):
    _cmdset = 0x4
    _cmdid = 0x4c
    _req_size = 2

    def __init__(self):
        self._workmode = 0
        self._recenter = 0

    def pack_req(self):
        buf = bytearray(self._req_size)
        buf[0] = self._workmode
        buf[1] = self._recenter
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        if self._retcode == 0:
            return True
        else:
            return False


class ProtoGimbalCtrl(ProtoData):
    _cmdset = 0x4
    _cmdid = 0xd
    _req_size = 2

    def __init__(self):
        self._order_code = 0x2ab5

    def pack_req(self):
        buf = bytearray(self._req_size)
        struct.pack_into("<H", buf, 0, self._order_code)
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        if self._retcode == 0:
            return True
        else:
            return False


class ProtoPlaySound(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0xb3
    _req_size = 10

    def __init__(self):
        self._action_id = 0
        self._push_freq = 2
        self._task_ctrl = 0
        self._sound_id = 0
        self._play_ctrl = 1  # 0： 停止播放 1：打断式播放 2：融合播放 3：忽略式播放
        self._interval = 0
        self._play_times = 0

        self._retcode = None
        self._accept = None

    def pack_req(self):
        buf = bytearray(self._req_size)
        buf[0] = self._action_id
        buf[1] = self._task_ctrl | self._push_freq << 2
        struct.pack_into('<I', buf, 2, self._sound_id)
        buf[6] = self._play_ctrl
        struct.pack_into('<H', buf, 7, self._interval)
        buf[9] = self._play_times
        logger.debug("ProtoPlaySound: pack_req, buf: {0}".format(binascii.hexlify(buf)))
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[offset]
        logger.debug(
            "ProtoPlaySound unpack_resp, buf : {0}, self._retcode: {1}".format(binascii.hexlify(buf), self._retcode))
        if self._retcode == 0:
            self._accept = buf[offset + 1]
            return True
        else:
            return False

    @property
    def sound_id(self):
        return self._sound_id

    @sound_id.setter
    def sound_id(self, value):
        self._sound_id = value

    @property
    def play_times(self):
        return self._play_times

    @play_times.setter
    def play_times(self, value):
        self._play_times = value


class ProtoSoundPush(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0xb4

    def __init__(self):
        self._action_id = 0
        self._percent = 0
        self._reserved = 0
        self._error_reason = 0
        self._action_state = 0
        self._sound_id = 0

    def pack_req(self):
        return b''

    # ack push
    def unpack_req(self, buf, offset=0):
        self._action_id = buf[0]
        self._percent = buf[1]
        self._error_reason = buf[2] >> 2 & 0x03
        self._action_state = buf[2] & 0x03
        self._sound_id = struct.unpack_from('<I', buf, 3)
        logger.debug("ProtoSoundPush unpack_req, buf {0}".format(binascii.hexlify(buf)))
        return True

    def unpack_resp(self, buf, offset=0):
        self._action_id = buf[offset]
        self._percent = buf[offset + 1]
        self._error_reason = buf[offset + 2] >> 2 & 0x03
        self._action_state = buf[offset + 2] & 0x03
        self._sound_id = struct.unpack_from('<I', buf, offset + 3)
        logger.debug("ProtoSoundPush unpack_resp, buf {0}".format(binascii.hexlify(buf)))
        return True

    @property
    def percent(self):
        return self._percent

    @percent.setter
    def percent(self, value):
        self._percent = value

    @property
    def sound_id(self):
        return self._sound_id

    @sound_id.setter
    def sound_id(self, value):
        self._sound = value


class ProtoGimbalRotate(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0xb0
    _req_size = 17

    def __init__(self):
        self._action_id = 0
        self._action_ctrl = 0  # 0 for start, 1 for cancel
        self._push_freq = 2  # 0 for 1Hz, 1 for 5Hz, 2 for 10Hz
        self._coordinate = 3
        self._pitch_valid = 1  # 1 for valid, 0 for invalid.
        self._yaw_valid = 1
        self._roll_valid = 0
        self._error = 0
        self._pitch = 0  # Unit: 0.1 degree
        self._roll = 0  # Unit: 0.1 degree
        self._yaw = 0  # Unit: 0.1 degree
        self._yaw_speed = 30
        self._roll_speed = 0
        self._pitch_speed = 30

    def pack_req(self):
        buf = bytearray(self._req_size)
        buf[0] = self._action_id
        buf[1] = self._action_ctrl | (self._push_freq << 2)
        buf[2] = self._yaw_valid | (self._roll_valid << 1) | (self._pitch_valid << 2) | (self._coordinate << 3)
        struct.pack_into('<hhh', buf, 3, self._yaw, self._roll, self._pitch)
        struct.pack_into('<HHHH', buf, 9, self._error, self._yaw_speed, self._roll_speed, self._pitch_speed)
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[offset]
        if self._retcode == 0:
            self._accept = buf[offset + 1]
            return True
        else:
            return False


class ProtoGimbalActionPush(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0xb1
    _cmdtype = DUSS_MB_TYPE_PUSH

    def __init__(self):
        self._action_id = 0
        self._percent = 0
        self._action_state = 0
        self._yaw = 0
        self._roll = 0
        self._pitch = 0

    def pack_req(self):
        return b''

    def unpack_req(self, buf, offset=0):
        self._action_id = buf[offset]
        self._percent = buf[offset + 1]
        self._action_state = buf[offset + 2] & 0x3
        self._yaw, self._roll, self._pitch = struct.unpack_from('<hhh', buf, offset + 3)
        return True

    def unpack_resp(self, buf, offset=0):
        self._action_id = buf[offset]
        self._percent = buf[offset + 1]
        self._action_state = buf[offset + 2] & 0x3
        self._yaw, self._roll, self._pitch = struct.unpack_from('<hhh', buf, offset + 3)
        return True


class ProtoGimbalRecenter(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0xb2
    _req_size = 9

    def __init__(self):
        self._action_id = 0
        self._action_ctrl = 0
        self._push_freq = 2
        self._pitch_valid = 1
        self._roll_valid = 0
        self._yaw_valid = 1
        self._yaw_speed = 100
        self._roll_speed = 0
        self._pitch_speed = 100

    def pack_req(self):
        buf = bytearray(self._req_size)
        buf[0] = self._action_id
        buf[1] = self._action_ctrl | (self._push_freq << 2)
        buf[2] = self._yaw_valid | (self._roll_valid << 1) | (self._pitch_valid << 2)
        struct.pack_into("<HHH", buf, 3, self._yaw_speed, self._roll_speed, self._pitch_speed)
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[offset]
        if self._retcode == 0:
            self._accept = buf[offset + 1]
            return True
        else:
            return False


class ProtoVisionDetectStatus(ProtoData):
    _cmdset = 0x0a
    _cmdid = 0xa5

    def __init__(self):
        self._vision_type = 0

    def pack_req(self):
        return b''

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        if self._retcode == 0:
            self._vision_type = buf[1] | buf[2] << 8
            return True
        else:
            logger.warning("ProtoVisionDetectType: unpack_resp, error")
            return False


class ProtoVisionSetColor(ProtoData):
    _cmdset = 0x0a
    _cmdid = 0xab
    _req_size = 2

    def __init__(self):
        self._type = 0
        self._color = 0

    def pack_req(self):
        buf = bytearray(self._req_size)
        buf[0] = self._type
        buf[1] = self._color
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        if self._retcode == 0:
            return True
        else:
            logger.warning("ProtoVisionSetColor: unpack_resp, retcode {0}".format(self._retcode))
            return False


class ProtoPositionMove(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0x25
    _req_size = 13

    def __init__(self):
        self._action_id = 0
        self._freq = 2
        self._action_ctrl = 0
        self._ctrl_mode = 0
        self._axis_mode = 0
        self._pos_x = 0
        self._pos_y = 0
        self._pos_z = 0
        self._vel_xy_max = 0
        self._agl_omg_max = 300

    def pack_req(self):
        buf = bytearray(self._req_size)
        buf[0] = self._action_id
        buf[1] = self._action_ctrl | self._freq << 2
        buf[2] = self._ctrl_mode
        buf[3] = self._axis_mode
        struct.pack_into('<hhh', buf, 4, self._pos_x, self._pos_y, self._pos_z)
        buf[10] = self._vel_xy_max
        struct.pack_into('<h', buf, 11, self._agl_omg_max)
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[offset]
        if self._retcode == 0:
            self._accept = buf[offset + 1]
            return True
        else:
            logger.warning("ProtoPositionMove: unpack_resp, retcode:{0}".format(self._retcode))
            return False


class ProtoPositionPush(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0x2a

    def __init__(self):
        self._action_id = 0
        self._percent = 0
        self._action_state = 0
        self._pos_x = 0
        self._pos_y = 0
        self._pos_z = 0

    def pack_req(self):
        return b''

    # ack push.
    def unpack_req(self, buf, offset=0):
        self._action_id = buf[0]
        self._percent = buf[1]
        self._action_state = buf[2]
        self._pos_x, self._pos_y, self._pos_z = struct.unpack_from('<hhh', buf, 3)
        return True

    def unpack_resp(self, buf, offset=0):
        self._action_id = buf[offset]
        self._percent = buf[offset + 1]
        self._action_state = buf[offset + 2]
        self._pos_x, self._pos_y, self._pos_z = struct.unpack_from('<hhh', buf, offset + 3)
        return True


class ProtoSetWheelSpeed(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0x20
    _req_size = 8

    def __init__(self):
        self._w1_spd = 0
        self._w2_spd = 0
        self._w3_spd = 0
        self._w4_spd = 0

    def pack_req(self):
        buf = bytearray(self._req_size)
        struct.pack_into("<hhhh", buf, 0, self._w1_spd, self._w2_spd, self._w3_spd, self._w4_spd)
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        if self._retcode == 0:
            return True
        else:
            logger.warning("ProtoSetWheelSpeed: unpack_resp, retcode:{0}".format(self._retcode))
            return False


class ProtoChassisSetWorkMode(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0x19
    _req_size = 1

    def __init__(self):
        self._mode = 0

    def pack_req(self):
        buf = bytearray(self._req_size)
        buf[0] = self._mode
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        if self._retcode == 0:
            return True
        else:
            return False


class ProtoChassisSpeedMode(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0x21
    _req_size = 12
    _cmdtype = DUSS_MB_TYPE_PUSH

    def __init__(self):
        self._x_spd = float(0)
        self._y_spd = float(0)
        self._z_spd = float(0)

    def pack_req(self):
        buf = bytearray(self._req_size)
        struct.pack_into("<fff", buf, 0, self._x_spd, self._y_spd, self._z_spd)
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        if self._retcode == 0:
            return True
        else:
            return False


class ProtoChassisPwmPercent(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0x3c
    _req_size = 13
    _cmdtype = DUSS_MB_TYPE_REQ

    def __init__(self):
        self._mask = 0
        self._pwm1 = 0
        self._pwm2 = 0
        self._pwm3 = 0
        self._pwm4 = 0
        self._pwm5 = 0
        self._pwm6 = 0

    def pack_req(self):
        buf = bytearray(self._req_size)
        buf[0] = self._mask
        struct.pack_into('<HHHHHH', buf, 1, self._pwm1, self._pwm2, self._pwm3, self._pwm4, self._pwm5, self._pwm6)
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        if self._retcode == 0:
            return True
        else:
            return False


class ProtoChassisPwmFreq(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0x2b
    _req_size = 13
    _cmdtype = DUSS_MB_TYPE_REQ

    def __init__(self):
        self._mask = 0
        self._pwm1 = 0
        self._pwm2 = 0
        self._pwm3 = 0
        self._pwm4 = 0
        self._pwm5 = 0
        self._pwm6 = 0

    def pack_req(self):
        buf = bytearray(self._req_size)
        buf[0] = self._mask
        struct.pack_into('<HHHHHH', buf, 1, self._pwm1, self._pwm2, self._pwm3, self._pwm4, self._pwm5, self._pwm6)
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        if self._retcode == 0:
            return True
        else:
            return False


class ProtoChassisSerialSet(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0xc0
    _req_size = 6

    def __init__(self):
        self._baud_rate = 0
        self._data_bit = 0
        self._odd_even = 0
        self._stop_bit = 0
        self._tx_en = 0
        self._rx_en = 0
        self._rx_size = 0
        self._tx_size = 0
        self._config = 0
        self._fun_en = 0

    def pack_req(self):
        buf = bytearray(self._req_size)
        self._config = (self._stop_bit & 0x1) << 7 | \
                       (self._odd_even & 0x3) << 5 | \
                       (self._data_bit & 0x3) << 3 | \
                       (self._baud_rate & 0x7)

        self._fun_en = ((self._tx_en & 0x1) << 1) | (self._rx_en & 0x1)
        struct.pack_into('<BBHH', buf, 0, self._config, 0xff, self._rx_size, self._tx_size)
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        if self._retcode == 0:
            return True
        else:
            return False


class ProtoChassisSerialMsgSend(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0xc1
    _req_size = 3

    def __init__(self):
        self._msg_len = 0
        self._msg_type = 0x2
        self._msg_buf = []

    def pack_req(self):
        buf = bytearray(self._msg_len + self._req_size + 1)
        struct.pack_into('<BH', buf, 0, self._msg_type, self._msg_len)
        buf[3:len(buf) - 1] = self._msg_buf
        return buf[0:-1]

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        if self._retcode == 0:
            return True
        else:
            return False


class ProtoVisionDetectEnable(ProtoData):
    _cmdset = 0x0a
    _cmdid = 0xa3
    _req_size = 2

    def __init__(self):
        self._type = 0

    def pack_req(self):
        buf = bytearray(self._req_size)
        struct.pack_into("<H", buf, 0, self._type)
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        if self._retcode == 0:
            return True
        else:
            self._error = struct.unpack_from("<H", buf, 1)
            logger.warning("ProtoVisionDetectEnable: unpack_resp, error:{0}".format(self._error))
            return False


class ProtoVisionDetectInfo(ProtoData):
    _cmdset = 0x0a
    _cmdid = 0xa4

    def __init__(self):
        self._type = 0
        self._status = 0
        self._errcode = 0
        self._rect_info = []
        self._data_buf = None

    def pack_req(self):
        return b''

    def unpack_req(self, buf, offset=0):
        self._type = buf[0]
        self._status = buf[1]
        self._errcode = buf[6] | (buf[7] << 8)
        count = buf[8]
        if self._type == 0:  # shoulder
            for i in range(0, count):
                x, y, w, h, info = struct.unpack_from('<ffffI', buf, 9 + 20 * i)
                t = 5
                self._rect_info.append([round(x, t), round(y, t), round(w, t), round(h, t)])
        elif self._type == 1:  # person
            for i in range(0, count):
                x, y, w, h, _ = struct.unpack_from('<ffffI', buf, 9 + 20 * i)
                t = 5
                self._rect_info.append([round(x, t), round(y, t), round(w, t), round(h, t)])
        elif self._type == 2:  # gesture
            for i in range(0, count):
                x, y, w, h, info = struct.unpack_from('<ffffI', buf, 9 + 20 * i)
                t = 5
                self._rect_info.append([round(x, t), round(y, t), round(w, t), round(h, t), info])
        elif self._type == 4:  # line
            if count > 0:
                x, y, theta, C, info = struct.unpack_from("<ffffI", buf, 9)
                self._rect_info.append(info)
            else:
                self._rect_info.append(0)
            for i in range(0, count):
                x, y, theta, C, info = struct.unpack_from("<ffffI", buf, 9 + 20 * i)
                t = 7
                self._rect_info.append([round(x, t), round(y, t), round(theta, t), round(C, t)])
        elif self._type == 5:  # marker
            for i in range(0, count):
                x, y, w, h, info, distance = struct.unpack_from('<ffffHH', buf, 9 + 20 * i)
                t = 5
                self._rect_info.append([round(x, t), round(y, t), round(w, t), round(h, t), info])
        elif self._type == 7:  # robot
            for i in range(0, count):
                x, y, w, h, _ = struct.unpack_from('<ffffI', buf, 9 + 20 * i)
                t = 5
                self._rect_info.append([round(x, t), round(y, t), round(w, t), round(h, t)])
        else:
            logger.warning("unsupported type: {0}".format(self._type))
        self._data_buf = (self._type, self._errcode, self._rect_info)
        return True


class ProtoSubscribeAddNode(ProtoData):
    _cmdset = 0x48
    _cmdid = 0x01
    _req_size = 5

    def __init__(self):
        self._node_id = 0
        self._sub_vision = 0x03000000
        self._pub_node_id = 0

    def pack_req(self):
        buf = bytearray(self._req_size)
        struct.pack_into("<BI", buf, 0, self._node_id, self._sub_vision)
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        if self._retcode == 0 or self._retcode == 0x50:
            self._pub_node_id = buf[1]
            return True
        else:
            logger.warning("ProtoSubscribeAddNode: unpack_resp, retcode:{0}".format(self._retcode))
            return False


class ProtoSubNodeReset(ProtoData):
    _cmdset = 0x48
    _cmdid = 0x02
    _req_size = 1

    def __init__(self):
        self._node_id = 0

    def pack_req(self):
        buf = bytearray(self._req_size)
        buf[0] = self._node_id
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        if self._retcode == 0:
            return True
        else:
            return False


class ProtoDelMsg(ProtoData):
    _cmdset = 0x48
    _cmdid = 0x04
    _req_size = 3

    def __init__(self):
        self._node_id = 0
        self._msg_id = 0
        self._sub_mode = 0

    def pack_req(self):
        buf = bytearray(self._req_size)
        buf[0] = self._sub_mode
        buf[1] = self._node_id
        buf[2] = self._msg_id
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        if self._retcode == 0:
            return True
        else:
            return False


class ProtoAddSubMsg(ProtoData):
    _cmdset = 0x48
    _cmdid = 0x03
    _req_size = 7

    def __init__(self):
        self._node_id = 0
        self._msg_id = 0
        self._timestamp = 0
        self._stop_when_disconnect = 0
        self._sub_mode = 0
        self._sub_data_num = 0
        self._sub_uid_list = []
        self._sub_freq = 1
        self._pub_node_id = 0
        self._sub_mode = 0
        self._err_uid = 0

    def pack_req(self):
        req_size = self._req_size + self._sub_data_num * 8
        buf = bytearray(req_size)
        buf[0] = self._node_id
        buf[1] = self._msg_id
        buf[2] = (self._timestamp & 0x1) | (self._stop_when_disconnect & 0x2)
        buf[3] = self._sub_mode
        buf[4] = self._sub_data_num
        for i in range(0, self._sub_data_num):
            logger.info("ProtoSubMsg: UID:{0}".format(hex(self._sub_uid_list[i])))
            struct.pack_into("<Q", buf, 5 + 8 * i, self._sub_uid_list[i])
        struct.pack_into("<H", buf, 5 + 8 * self._sub_data_num, self._sub_freq)
        logger.info("ProtoSubMsg: pack_req, num:{0}, buf {1}".format(self._sub_data_num, binascii.hexlify(buf)))
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        self.pub_node_id = buf[1]
        self.ack_sub_mode = buf[2]
        self.ack_msg_id = buf[3]
        self.ack_err_uid_data = buf[4] | (buf[5] << 8) | (buf[6] << 16) | (buf[7] << 24)
        if self._retcode == 0:
            return True
        else:
            return False


class ProtoPushPeriodMsg(ProtoData):
    _cmdset = 0x48
    _cmdid = 0x8
    _type = DUSS_MB_TYPE_PUSH

    def __init__(self):
        self._sub_mode = 0
        self._msg_id = 0
        self._data_buf = None

    def pack_req(self):
        return b''

    def unpack_req(self, buf, offset=0):
        self._sub_mode = buf[0]
        self._msg_id = buf[1]
        self._data_buf = buf[2:]
        return True


class ProtoGripperCtrl(ProtoData):
    _cmdset = 0x33
    _cmdid = 0x11
    _req_size = 4

    def __init__(self):
        self._id = host2byte(27, 1)
        self._control = 0
        self._power = 330

    def pack_req(self):
        buf = bytearray(self._req_size)
        buf[0] = self._id
        buf[1] = self._control
        struct.pack_into("<H", buf, 2, self._power)
        logger.debug("ProtoGripperCtrl： buf:{0}".format(binascii.hexlify(buf)))
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        if self._retcode == 0:
            return True
        else:
            return False


class ProtoRoboticArmMove(ProtoData):
    _cmdset = 0x33
    _cmdid = 0x13
    _req_size = 15

    def __init__(self):
        self._id = host2byte(27, 2)
        self._type = 0
        self._mask = 0x3
        self._x = 0
        self._y = 0
        self._z = 0

    def pack_req(self):
        buf = bytearray(self._req_size)
        buf[0] = self._id
        buf[1] = self._type
        buf[2] = self._mask
        struct.pack_into('<iii', buf, 3, self._x, self._y, self._z)
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        if self._retcode == 0:
            return True
        else:
            return False


class ProtoRoboticArmGetPostion(ProtoData):
    _cmdset = 0x33
    _cmdid = 0x14
    _req_size = 1

    def __init__(self):
        self._id = 0x5b
        self._retcode = 0
        self._x = 0
        self._y = 0
        self._z = 0

    def pack_req(self):
        buf = bytearray(self._req_size)
        buf[0] = self._id
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        self._x, self._y, self._z = struct.unpack_from('<iii', buf, 1)
        return True


class ProtoSensorGetData(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0xf0
    _req_size = 1

    def __init__(self):
        self._port = 0

    def pack_req(self):
        buf = bytearray(self._req_size)
        buf[0] = self._port
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        self._port = buf[1]
        self._adc, self._io, self._time = struct.unpack_from('<HBI', buf, 2)
        if self._retcode == 0:
            return True
        else:
            return False


class ProtoServoModeSet(ProtoData):
    _cmdset = 0x33
    _cmdid = 0x16
    _req_size = 2

    def __init__(self):
        self._id = 0x19
        self._mode = 0

    def pack_req(self):
        buf = bytearray(self._req_size)
        buf[0] = self._id
        buf[1] = self._mode
        return buf


class ProtoServoControl(ProtoData):
    _cmdset = 0x33
    _cmdid = 0x17
    _req_size = 4

    def __init__(self):
        self._id = 0x19
        self._enable = 1
        self._value = 0

    def pack_req(self):
        buf = bytearray(self._req_size)
        buf[0] = self._id
        buf[1] = self._enable
        struct.pack_into('<H', buf, 2, self._value)
        return buf


class ProtoServoGetAngle(ProtoData):
    _cmdset = 0x33
    _cmdid = 0x15
    _req_size = 1

    def __init__(self):
        self._id = 0x19
        self._enable = 1
        self._value = 0
        self._retcode = 0
        self._angle = 0

    def pack_req(self):
        buf = bytearray(self._req_size)
        buf[0] = self._id
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[0]
        self._angle = (buf[1] + (buf[2] << 8) + (buf[3] << 16) + (buf[4] << 24)) / 10
        return True


class ProtoServoCtrlSet(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0xb7
    _req_size = 7

    def __init__(self):
        self._action_id = 0
        self._freq = 2
        self._action_ctrl = 0
        self._id = 0
        self._value = 0

    def pack_req(self):
        buf = bytearray(self._req_size)
        buf[0] = self._action_id
        buf[1] = self._action_ctrl | self._freq << 2
        buf[2] = host2byte(25, self._id)
        struct.pack_into('<i', buf, 3, self._value)
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[offset]
        if self._retcode == 0:
            self._accept = buf[offset + 1]
            return True
        else:
            logger.warning("ProtoServoCtrlSet: unpack_resp, retcode:{0}".format(self._retcode))
            return False


class ProtoServoCtrlPush(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0xb8

    def __init__(self):
        self._action_id = 0
        self._percent = 0
        self._action_state = 0
        self._value = 0

    def pack_req(self):
        return b''

    def unpack_req(self, buf, offset=0):
        self._action_id = buf[0 + offset]
        self._percent = buf[1 + offset]
        self._action_state = buf[2 + offset] & 0x3
        self._value = struct.unpack_from('<i', buf, 3 + offset)
        return True


class ProtoRoboticArmMoveCtrl(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0xb5
    _req_size = 17

    def __init__(self):
        self._action_id = 0
        self._freq = 2
        self._action_ctrl = 0
        self._id = host2byte(27, 2)
        self._mode = 0
        self._mask = 0x3
        self._x = 0
        self._y = 0
        self._z = 0

    def pack_req(self):
        buf = bytearray(self._req_size)
        buf[0] = self._action_id
        buf[1] = self._action_ctrl | self._freq << 2
        buf[2] = self._id
        buf[3] = self._mode
        buf[4] = self._mask
        struct.pack_into("<iii", buf, 5, self._x, self._y, self._z)
        return buf

    def unpack_resp(self, buf, offset=0):
        self._retcode = buf[offset]
        if self._retcode == 0:
            self._accept = buf[offset + 1]
            return True
        else:
            logger.warning("ProtoRoboticArmMoveCtrl: unpack_resp, retcode:{0}".format(self._retcode))
            return False


class ProtoRoboticArmMovePush(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0xb6

    def __init__(self):
        self._action_id = 0
        self._percent = 0
        self._action_state = 0
        self._x = 0
        self._y = 0
        self._z = 0

    def pack_req(self):
        return b''

    def unpack_req(self, buf, offset=0):
        self._action_id = buf[0 + offset]
        self._percent = buf[1 + offset]
        self._action_state = buf[2 + offset] & 0x3
        self._x, self._y = struct.unpack_from('<ii', buf, 3 + offset)
        return True


class ProtoRoboticAiInit(ProtoData):
    _cmdset = 0x3f
    _cmdid = 0xe9
    _req_size = 17

    def __init__(self):
        self._addr = 0x0103
        self._sender = 0x0103
        self._reciver = 0x0301
        self._seq_num = random.randint(0, 1000)
        self._cmd = 0x020d
        self._attr = 0

    def pack_req(self):
        self._buf = bytearray(self._req_size)
        self._len = 2
        self._buf[0] = 0xAA
        self._buf[1] = self._len & 0xff
        self._buf[2] = (self._len >> 8)
        crc_h = algo.crc8_calc(self._buf[0:3], 0x11)
        self._buf[3] = crc_h
        self._buf[4] = self._sender & 0xff
        self._buf[5] = (self._sender >> 8)
        self._buf[6] = self._reciver & 0xff
        self._buf[7] = (self._reciver >> 8)
        self._buf[8] = self._attr
        self._buf[9] = self._seq_num & 0xff
        self._buf[10] = (self._seq_num >> 8)
        self._buf[11] = self._cmd & 0xff
        self._buf[12] = (self._cmd >> 8)
        self._buf[13] = self._addr & 0xff
        self._buf[14] = (self._addr >> 8)
        crc_H = algo.crc16_calc(self._buf[0:self._req_size - 2], 0x4F19)
        self._buf[15] = crc_H & 0xff
        self._buf[16] = crc_H >> 8
        return self._buf

    def unpack_req(self, buf, offset=0):
        return True


class TextProtoData(object):
    SUCCESSFUL_RESP_FLAG = 'ok'

    def __init__(self):
        self._buf = None
        self._len = None
        self._text_cmd = None
        self._action_state = None
        self._resp = None
        self._percent = 0

    def __repr__(self):
        return "<{0}>".format(self.__class__.__name__)

    @property
    def text_cmd(self):
        return self._text_cmd

    @text_cmd.setter
    def text_cmd(self, cmd):
        self._text_cmd = cmd

    def pack_req(self):
        """ 协议对象打包发送数据为字节流。

        :return: 字节流数据。
        """
        logger.debug("TextProtoData: pack_req test_cmd {0}, type {1}".format(self.text_cmd, type(self.text_cmd)))
        self._buf = self.text_cmd
        return self._buf

    def unpack_req(self, buf, offset=0):
        """ 从字节流解包。

        :param buf：字节流数据。
        :param offset：字节流数据偏移量。
        :return：True 解包成功；False 解包失败。
        """
        self._action_state = buf
        self._resp = buf
        return True

    def pack_resp(self):
        """ 协议对象打包。

        :return：字节流数据。
        """
        pass

    def unpack_resp(self, buf, offset=0):
        """ 从字节流解包为返回值和相关属性。

        :param buf：字节流数据。
        :param offset：字节流数据偏移量。
        :return: True or False.
        """
        self._action_state = buf
        self._resp = buf
        return True

    def get_status(self):
        if self._resp:
            if self._resp == 'error':
                return False
            elif self._resp == 'ok':
                return True
            else:
                return False
        else:
            return False

    @property
    def resp(self):
        if self._resp is not None:
            return self._resp.strip()
        else:
            return self._resp

    @property
    def proresp(self):
        """ 针对acceleration?、attitude?、temp?命令的回复进行预处理。

        :return: dict.
        """
        msg_dict = dict()
        resp = self.resp

        if resp is None:
            return msg_dict

        if len(resp.split("~")) == 2:
            msg_dict["templ"] = int(resp.split("~")[0])
            msg_dict["temph"] = int(resp.split("~")[1][:-1])
        elif len(resp.split(";")) == 4:
            msg_list = resp.split(";")[:-1]
            for msg in msg_list:
                key, value = msg.split(":")
                msg_dict[key] = float(value)
        else:
            logger.warning("doesn't support sdk! proresp returns empty dict")
        return msg_dict


class TextProtoDrone(TextProtoData):

    def __init__(self):
        super().__init__()


class TextProtoDronePush(TextProtoData):
    def __init__(self):
        super().__init__()


class TelloDdsProto(object):
    DDS_PAD_MID_FLAG = "mid"
    DDS_PAD_X_FLAG = "x"
    DDS_PAD_Y_FLAG = "y"
    DDS_PAD_Z_FLAG = "z"
    DDS_PAD_MPRY_FLAG = "mpry"
    DDS_PITCH_FLAG = "pitch"
    DDS_ROLL_FLAG = "roll"
    DDS_YAW_FLAG = "yaw"
    DDS_VGX_FLAG = "vgx"
    DDS_VGY_FLAG = "vgy"
    DDS_VGZ_FLAG = "vgz"
    DDS_TEMP_L_FLAG = "templ"
    DDS_TEMP_H_FLAG = "temph"
    DDS_TOF_FLAG = "tof"
    DDS_HIGH_FLAG = "h"
    DDS_BATTERY_FLAG = "bat"
    DDS_BARO_FLAG = "baro"
    DDS_MOTOR_TIME_FLAG = "time"
    DDS_AGX_FLAG = "agx"
    DDS_AGY_FLAG = "agy"
    DDS_AGZ_FLAG = "agz"
    DDS_FREQ = 10

    def __init__(self):
        pass


class STAConnInfo:
    def __init__(self):
        self._ssid = ""
        self._password = ""
        self._cc = "CN"
        self._appid = ""
        self._bssid = None
        self._has_bssid = 0

        self._is_pairing = 0
        self._ip = None
        self._mac = None
        self.recv_appid = ""

    def set_info(self, ssid="", password="", id="", cc="CN"):
        self._ssid = ssid
        self._password = password
        self._appid = id
        self._cc = cc

    def pack(self):
        ssid_len = len(self._ssid)
        pwd_len = len(self._password)
        if self._has_bssid == 1:
            buf = bytearray(2 + 8 + 2 + ssid_len + pwd_len + 6)
        else:
            buf = bytearray(2 + 8 + 2 + ssid_len + pwd_len)
        buf[0] = ssid_len | (pwd_len & 0x3) << 6
        buf[1] = (pwd_len >> 2) | (self._has_bssid << 3)
        buf[2:10] = self._appid.encode(encoding="utf-8")
        buf[10:12] = self._cc.encode(encoding="utf-8")
        buf[12:12 + ssid_len] = self._ssid.encode(encoding="utf-8")
        buf[12 + ssid_len:12 + ssid_len + pwd_len] = self._password.encode(encoding="utf-8")
        if self._has_bssid == 1:
            buf[12 + ssid_len + pwd_len:] = self._bssid.encode(encoding="utf-8")
        return buf

    def unpack(self, buf):
        blank_byte = bytearray(1)
        sof, is_pairing = struct.unpack_from(">HI", buf)
        if sof != 0x5a5b:
            return False
        self._is_pairing = is_pairing & 0x1
        self._ip = "{0}.{1}.{2}.{3}".format(int(buf[6]), int(buf[7]), int(buf[8]), int(buf[9]))
        self._mac = "{0:2x}:{1:2x}:{2:2x}:{3:2x}:{4:2x}:{5:2x}".format(
            int(buf[10]), int(buf[11]), int(buf[12]), int(buf[13]), int(buf[14]), int(buf[15]))
        self._recv_appid = str(buf[16:23], encoding='utf-8').replace(str(blank_byte, encoding='utf-8'), "")
        return True
