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
import pyaudio
import threading
import robomaster
from robomaster import robot


def audio_playing_task(ep_robot):
    ep_camera = ep_robot.camera
    audio_player = pyaudio.PyAudio()
    playing_stream = audio_player.open(format=pyaudio.paInt16,
                                                   channels=1,
                                                   rate=48000,
                                                   output=True)
    while True:
        try:
            frame = ep_camera.read_audio_frame()
        except Exception as e:
            print("LiveView: playing_task, video_frame_queue is empty.")
            continue
        playing_stream.write(frame)
        playing_stream.stop_stream()
    playing_stream.close()


if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="rndis")

    ep_camera = ep_robot.camera

    audio_player = pyaudio.PyAudio()
    playing_stream = audio_player.open(format=pyaudio.paInt16,
                                       channels=1,
                                       rate=48000,
                                       output=True)

    ep_camera.start_audio_stream()
    playing_task = threading.Thread(target=audio_playing_task, args=(ep_robot,))
    time.sleep(20)
    ep_camera.stop_audio_stream()
    ep_robot.close()