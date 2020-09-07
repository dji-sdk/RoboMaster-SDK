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


from . import conn
from . import logger
import threading
import queue
import libmedia_codec
import numpy
import cv2
import time


class LiveView(object):

    def __init__(self, robot):
        self._robot = robot
        self._video_stream_conn = conn.StreamConnection()
        self._video_decoder = libmedia_codec.H264Decoder()
        # disable logging
        self._video_decoder_thread = None
        self._video_display_thread = None
        self._video_frame_queue = queue.Queue(64)
        self._video_streaming = False
        self._displaying = False
        self._video_frame_count = 0

        self._audio_stream_conn = conn.StreamConnection()
        self._audio_decoder = libmedia_codec.OpusDecoder()
        self._audio_decoder_thread = None
        self._audio_playing_thread = None
        self._audio_frame_queue = queue.Queue(32)
        self._audio_streaming = False
        self._playing = False
        self._audio_frame_count = 0

    def __del__(self):
        self.stop()

    def stop(self):
        if self._video_streaming:
            self.stop_video_stream()
        if self._audio_streaming:
            self.stop_audio_stream()

    def start_video_stream(self, display=True, addr=None, ip_proto="tcp"):
        try:
            logger.info("Liveview: try to connect addr {0}, proto={1}".format(
                addr, ip_proto))
            self._video_stream_conn.connect(addr, ip_proto)
            self._video_streaming = True
            self._video_decoder_thread = threading.Thread(target=self._video_decoder_task)
            self._video_decoder_thread.start()
            if display:
                self._video_display_thread = threading.Thread(target=self._video_display_task)
                self._video_display_thread.start()
        except Exception as e:
            logger.error("Liveview: start_video_stream, exception {0}".format(e))
            return False
        return True

    def stop_video_stream(self):
        try:
            self._video_streaming = False
            self._displaying = False
            if self._video_stream_conn:
                self._video_stream_conn.disconnect()
            if self._displaying:
                if self._video_display_thread:
                    self._video_frame_queue.put(None)
                    self._video_display_thread.join()
            if self._video_decoder_thread:
                self._video_decoder_thread.join()
            self._video_frame_queue.queue.clear()
        except Exception as e:
            logger.error("LiveView: disconnect exception {0}".format(e))
            return False
        logger.info("LiveView: stop_video_stream stopped.")
        return True

    def read_video_frame(self, timeout=3, strategy="pipeline"):
        if strategy == "pipeline":
            return self._video_frame_queue.get(timeout=timeout)
        elif strategy == "newest":
            while self._video_frame_queue.qsize() > 1:
                self._video_frame_queue.get(timeout=timeout)
            return self._video_frame_queue.get(timeout=timeout)
        else:
            logger.warning("LiveView: read_video_frame, unsupported strategy:{0}".format(strategy))
            return None

    def _h264_decode(self, data):
        res_frame_list = []
        frames = self._video_decoder.decode(data)
        for frame_data in frames:
            (frame, width, height, ls) = frame_data
            if frame:
                frame = numpy.fromstring(frame, dtype=numpy.ubyte, count=len(frame), sep='')
                frame = (frame.reshape((height, width, 3)))
                res_frame_list.append(frame)
        return res_frame_list

    def _video_decoder_task(self):
        self._video_streaming = True
        logger.info("Liveview: _video_decoder_task, started!")
        while self._video_streaming:
            data = b''
            # 获取一帧h264 数据
            buf = self._video_stream_conn.read_buf()
            if not self._video_streaming:
                break
            if buf:
                data += buf
                frames = self._h264_decode(data)
                for frame in frames:
                    try:
                        self._video_frame_count += 1
                        if self._video_frame_count % 30 == 1:
                            logger.info("LiveView: video_decoder_task, get frame {0}.".format(self._video_frame_count))
                        self._video_frame_queue.put(frame, timeout=2)
                    except Exception as e:
                        logger.warning("LiveView: _video_decoder_task, decoder queue is full, e {}.".format(e))
                        continue
        logger.info("LiveView: _video_decoder_task, quit.")

    def _video_display_task(self, name="RoboMaster LiveView"):
        self._displaying = True
        logger.info("Liveview: _video_display_task, started!")
        while self._displaying & self._video_streaming:
            try:
                frame = self._video_frame_queue.get()
                if frame is None:
                    logger.warning("LiveView: _video_display_task, get frame None.")
                    if not self._displaying:
                        break
            except Exception as e:
                logger.warning("LiveView: display_task, video_frame_queue is empty, e {0}".format(e))
                continue
            img = numpy.array(frame)
            cv2.imshow(name, img)
            cv2.waitKey(1)
        logger.info("LiveView: _video_display_task, quit.")

    def read_audio_frame(self, timeout=1):
        return self._audio_frame_queue.get(timeout=timeout)

    def start_audio_stream(self, addr=None, ip_proto="tcp"):
        try:
            logger.info("LiveView: try to connect addr:{0}, ip_proto:{1}".format(
                addr, ip_proto))
            self._audio_stream_conn.connect(addr, ip_proto)
            self._audio_decoder_thread = threading.Thread(
                target=self._audio_decoder_task)
            self._audio_decoder_thread.start()
        except Exception as e:
            logger.error("LiveView: start_audio_stream, exception {0}".format(e))
            return False
        return True

    def stop_audio_stream(self):
        try:
            logger.info("LiveView: stop_audio_stream stopping...")
            self._audio_streaming = False
            if self._audio_decoder_thread:
                self._audio_decoder_thread.join()
            self._audio_stream_conn.disconnect()
            self._video_frame_queue.queue.clear()
            # make sure the robot is disconnected
            time.sleep(0.5)
        except Exception as e:
            logger.error("LiveView: disconnect exception {0}".format(e))
            return False
        logger.info("LiveView: stop_video_stream stopped.")
        return True

    def _audio_decoder_task(self):
        self._audio_streaming = True
        while self._audio_streaming:
            data = b''

            buf = self._audio_stream_conn.read_buf()
            if buf:
                data += buf

                if len(data) != 0:
                    frame = self._audio_decoder.decode(data)
                    if frame:
                        try:
                            self._audio_frame_count += 1
                            logger.info("LiveView: audio_decoder_task, get frame {0}.".format(self._audio_frame_count))
                            self._audio_frame_queue.put(frame, timeout=1)
                        except Exception as e:
                            if not self._audio_streaming:
                                break
                            logger.warning("LiveView: _audio_decoder_task, audio_frame_queue full, e {0}!".format(e))
                            continue
        logger.info("LiveView: _audio_decoder_task, quit.")
