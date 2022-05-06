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


import numpy
import audioop
import wave
import time
from . import module
from . import conn
from . import protocol
from . import logger
from . import media


__all__ = ['Camera', 'EPCamera', 'TelloCamera', 'STREAM_360P', 'STREAM_540P', 'STREAM_720P']

STREAM_360P = "360p"
STREAM_540P = "540p"
STREAM_720P = "720p"


class Camera(object):

    def __init__(self, robot):
        self._robot = robot
        self._client = robot.client
        self._video_enable = False
        self._audio_enable = False
        self._liveview = media.LiveView(robot)

    def start_video_stream(self, display=True):
        pass

    def stop_video_stream(self):
        pass

    def read_video_frame(self, timeout=3, strategy="pipeline"):
        """ 读取一帧视频流帧

        :param timeout: float: (0, inf)，超时时间，超过指定timeout时间后函数返回
        :param strategy: enum: ("pipeline", "newest") 读取帧策略：pipeline 流水线依次读取，newest 获取最新的一帧数据，\
        注意会清空老的数据帧队列
        :return: frame, 已解码的视频流帧字节流
        """
        return self._liveview.read_video_frame(timeout, strategy)

    def read_cv2_image(self, timeout=3, strategy="pipeline"):
        """ 读取一帧视频流帧

        :param timeout: float: (0, inf)，超时参数，在timeout时间内未获取到视频流帧，函数返回
        :param strategy: enum: ("pipeline", "newest")，读取帧策略：pipeline 依次读取缓存的帧信息，newest 获取最新的一帧\
        数据，会清空旧的数据帧
        :return: image

        """
        frame = self.read_video_frame(timeout, strategy)
        if frame is None:
            return None
        img = numpy.array(frame)
        return img


class TelloCamera(Camera):
    """ 教育无人机 摄像机模块 """

    def __init__(self, robot):
        super().__init__(robot)

    def __del__(self):
        self.stop()

    @property
    def conf(self):
        return self._robot.conf

    def start_video_stream(self, display=True):
        """ 开启视频流

        :param display: bool, 是否显示视频流
        :return: bool: 调用结果
        """
        self._video_stream(1)
        self._video_enable = True
        vs_addr = self.conf.video_stream_addr
        vs_proto = self.conf.video_stream_proto
        return self._liveview.start_video_stream(display,
                                                 addr=vs_addr,
                                                 ip_proto=vs_proto)

    def stop_video_stream(self):
        flag = self._liveview.stop_video_stream()
        self._video_stream(0)
        self._video_enable = False
        return flag

    def _video_stream(self, on_off=1):
        cmd = ""
        if on_off == 1:
            cmd = "streamon"
        elif on_off == 0:
            cmd = "streamoff"
        else:
            logger.warning("_video_stream")
            return False
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
                    return False
            else:
                logger.warning("TelloEduCamera: get_wifi failed.")
        except Exception as e:
            logger.warning("TelloEduCamera: get_wifi, send_sync_msg exception {0}".format(str(e)))
            return False

    def stop(self):
        if self._video_enable:
            self._stop_video_stream()
        if self._liveview:
            self._liveview.stop()

    def set_fps(self, fps):
        """ 设置飞机视频帧率

        :param fps: 需要设置的帧率，[high, middle, low]
        :return: bool: 设置结果
        """
        cmd = "setfps {0}".format(fps)
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
                logger.warning("Drone: set_fps failed")
            return False
        except Exception as e:
            logger.warning("Drone: set_fps, send_sync_msg exception {0}".format(str(e)))
            return False

    def set_bitrate(self, bitrate):
        """ 设置飞机传输码率

        :param bitrate: 需要设置的传输码率，[0, 6]
        :return: bool: 设置结果
        """
        cmd = "setbitrate {0}".format(bitrate)
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
                logger.warning("Drone: set_bitrate failed")
            return False
        except Exception as e:
            logger.warning("Drone: set_bitrate, send_sync_msg exception {0}".format(str(e)))
            return False

    def set_resolution(self, resolution):
        """ 设置飞机视频分辨率

        :param resolution: 需要设置的视频分辨率，[high, low]
        :return: bool: 设置结果
        """
        cmd = "setresolution {0}".format(resolution)
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
                logger.warning("Drone: set_resilution failed")
            return False
        except Exception as e:
            logger.warning("Drone: set_resilution, send_sync_msg exception {0}".format(str(e)))
            return False

    def set_down_vision(self, setting):
        """设置飞机图像源

        :param direction: 需要设置的图像源，[1, 0]
        :return: 设置结果
        """
        cmd = "downvision {0}".format(setting)
        print("cmd", cmd)
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
                logger.error("Drone: set_down_vision failed")
            return False
        except Exception as e:
            logger.error("Drone: set_down_vision, send_sync_msg exception {0}".format(str(e)))
            return False


class EPCamera(module.Module, Camera):
    """ EP 摄像机模块 """

    _host = protocol.host2byte(1, 0)

    def __init__(self, robot):
        module.Module.__init__(self, robot)
        Camera.__init__(self, robot)
        self._conf = robot.conf

    def __del__(self):
        self.stop()

    @property
    def conf(self):
        """ 相机参数配置 """
        return self._conf

    @property
    def audio_stream_addr(self):
        """ 机器人音频流地址

        :return: tuple:(ip, port)，机器人音频流地址
        """
        return self._robot.ip, self.conf.audio_stream_port

    @property
    def video_stream_addr(self):
        """ 机器人视频流地址

        :return: tuple:(ip, port)：机器人视频流地址 """
        return self._robot.ip, self.conf.video_stream_port

    def start_video_stream(self, display=True, resolution="720p"):
        """ 开启视频流

        :param display: bool，是否显示视频流
        :param resolution: enum: ("360p", "540p", "720p")，设置图传分辨率尺寸
        :return: bool：调用结果
        """
        result = self._stream_sdk(1, resolution)
        if not result:
            logger.error("Camera: start_video_stream, stream_sdk(1) failed!")
            return False
        result = self._video_stream(1, resolution)
        if not result:
            logger.error("Camera: start_video_stream, video_stream(1) failed!")
            return False
        self._video_enable = True
        return self._liveview.start_video_stream(display,
                                                 self.video_stream_addr,
                                                 self.conf.video_stream_proto)

    def stop_video_stream(self):
        """ 停止视频流

        :return: bool: 调用结果
        """
        result = self._video_stream(0)
        if not result:
            logger.warning("Camera: stop_video_stream, _video_stream(0) failed!")
        self._video_enable = False

        if not self._video_enable and not self._audio_enable:
            self._stream_sdk(0)
        return self._liveview.stop_video_stream()

    def start_audio_stream(self):
        """ 开启音频流

        """
        result = self._stream_sdk(1)
        if not result:
            logger.error("Camera: start_audio_stream, _stream_sdk(1) failed!")
            return False
        result = self._audio_stream(1)
        if not result:
            logger.error("Camera: start_audio_stream, _audio_stream(1) failed.")
            return False
        self._audio_enable = True

        if not self._video_enable and not self._audio_enable:
            self._stream_sdk(0)

        return self._liveview.start_audio_stream(self.audio_stream_addr,
                                                 self.conf.audio_stream_proto)

    def stop_audio_stream(self):
        """ 停止音频流

        :return：bool: 调用结果
        """
        result = self._audio_stream(0)
        if not result:
            logger.warning("Camera: start_audio_stream, _audio_stream(1) failed.")
        self._audio_enable = False
        if not self._video_enable and not self._audio_enable:
            self._stream_sdk(0)
        return self._liveview.stop_audio_stream()

    def read_audio_frame(self, timeout=1):
        """ 读取一段音频流信息

        :param timeout: float: (0, inf)，超时时间，超过指定timeout时间后函数返回
        :return: data, 已解码的音频流帧字节流
        """
        return self._liveview.read_audio_frame(timeout)

    def record_audio(self, save_file="output.wav", seconds=5, sample_rate=48000):
        """ 录制音频，保存到本地，支持wav格式，单通道

        :param save_file: 本地文件路径，目前仅支持wav格式
        :param seconds: 录制时间
        :param sample_rate: 采样率
        :return: bool: 调用结果
        """
        self.start_audio_stream()
        start = time.time()
        try:
            wf = wave.open(save_file, 'wb')
            wf.setparams((1, 2, sample_rate, 0, 'NONE', 'Uncompressed'))
            frames = []
            while True:
                if time.time() - start >= seconds:
                    break
                audio_frame = self.read_audio_frame()
                if sample_rate == 48000:
                    wf.writeframes(audio_frame)
                else:
                    frames.append(audio_frame)

            if sample_rate != 48000:
                data = b''.join(frames)
                converted = audioop.ratecv(data, 2, 1, 48000, sample_rate, None)
                wf.writeframes(converted[0])
            wf.close()
        except Exception as e:
            logger.error("Camera: record_audio, exception {0}".format(e))
            return False
        finally:
            self.stop_audio_stream()
        return True

    def _stream_sdk(self, on_off=1, resolution="720p"):
        """ 控制媒体流sdk模式

        :param on_off: 1 表示进入SDK模式，0 表示退出SDK模式
        """
        conn_type = self._robot.conn_type

        proto = protocol.ProtoStreamCtrl()
        # 1 表示SDK控制模式
        proto._ctrl = 1
        # 0 表示WiFi， 1 表示RNDIS
        if conn_type is conn.CONNECTION_WIFI_AP or conn_type is conn.CONNECTION_WIFI_STA:
            proto._conn_type = 0
        elif conn_type is conn.CONNECTION_USB_RNDIS:
            proto._conn_type = 1
        else:
            logger.error("Camera: _stream_sdk, conn_type:{0} is not "
                         "supported.".format(conn_type))
        proto._state = on_off
        if resolution == "720p":
            proto._resolution = 0
        elif resolution == "360p":
            proto._resolution = 1
        elif resolution == "540p":
            proto._resolution = 2
        else:
            proto._resolution = 0
            logger.warning("Camera, _video_stream, unsupported resolution {0}".format(resolution))
        return self._send_sync_proto(proto)

    def _video_stream(self, on_off=1, resolution="720p"):
        proto = protocol.ProtoStreamCtrl()
        # 2 表示视频流控制模式
        proto._ctrl = 2
        if resolution == "720p":
            proto._resolution = 0
        elif resolution == "360p":
            proto._resolution = 1
        elif resolution == "540p":
            proto._resolution = 2
        else:
            proto._resolution = 0
            logger.warning("Camera, _video_stream, unsupported resolution {0}".format(resolution))

        conn_type = self._robot.conn_type
        if conn_type is conn.CONNECTION_WIFI_AP or conn_type is conn.CONNECTION_WIFI_STA:
            proto._conn_type = 0
        elif conn_type is conn.CONNECTION_USB_RNDIS:
            proto._conn_type = 1
        else:
            logger.error("Camera: _video_stream, conn_type:{0} is not supported.".format(conn_type))
        proto._state = on_off
        return self._send_sync_proto(proto)

    def _audio_stream(self, on_off=1):
        proto = protocol.ProtoStreamCtrl()
        # 3 表示视音频流控制模式
        proto._ctrl = 3
        conn_type = self._robot.conn_type
        if conn_type is conn.CONNECTION_WIFI_AP or conn_type is conn.CONNECTION_WIFI_STA:
            proto._conn_type = 0
        elif conn_type is conn.CONNECTION_USB_RNDIS:
            proto._conn_type = 1
        else:
            logger.error("Camera: _audio_stream, conn_type:{0} is not supported.".format(conn_type))
        proto._state = on_off
        return self._send_sync_proto(proto)

    def stop(self):
        """ 停止 """
        if self._video_enable:
            self.stop_video_stream()
        if self._audio_enable:
            self.stop_audio_stream()
        if self._liveview:
            self._liveview.stop()

    def take_photo(self):
        """ 拍照

        :return: bool: 调用结果
        """

        proto = protocol.ProtoTakePhoto()
        return self._send_sync_proto(proto)

    def _set_zoom(self, zoom=1.0):
        """ 设置变焦参数

        :param zoom: 变焦值
        :return: bool: 调用结果
        """
        proto = protocol.ProtoSetZoom()
        proto._zoom = zoom
        return self._send_sync_proto(proto)
