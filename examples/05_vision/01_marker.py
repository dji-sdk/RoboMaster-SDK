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


import cv2
import robomaster
from robomaster import robot
from robomaster import vision


class MarkerInfo:

    def __init__(self, x, y, w, h, info):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._info = info

    @property
    def pt1(self):
        return int((self._x - self._w / 2) * 1280), int((self._y - self._h / 2) * 720)

    @property
    def pt2(self):
        return int((self._x + self._w / 2) * 1280), int((self._y + self._h / 2) * 720)

    @property
    def center(self):
        return int(self._x * 1280), int(self._y * 720)

    @property
    def text(self):
        return self._info


markers = []


def on_detect_marker(marker_info):
    number = len(marker_info)
    markers.clear()
    for i in range(0, number):
        x, y, w, h, info = marker_info[i]
        markers.append(MarkerInfo(x, y, w, h, info))
        print("marker:{0} x:{1}, y:{2}, w:{3}, h:{4}".format(info, x, y, w, h))


if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    ep_vision = ep_robot.vision
    ep_camera = ep_robot.camera

    ep_camera.start_video_stream(display=False)
    result = ep_vision.sub_detect_info(name="marker", callback=on_detect_marker)

    for i in range(0, 500):
        img = ep_camera.read_cv2_image(strategy="newest", timeout=0.5)
        for j in range(0, len(markers)):
            cv2.rectangle(img, markers[j].pt1, markers[j].pt2, (255, 255, 255))
            cv2.putText(img, markers[j].text, markers[j].center, cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
        cv2.imshow("Markers", img)
        cv2.waitKey(1)
    cv2.destroyAllWindows()

    result = ep_vision.unsub_detect_info(name="marker")
    cv2.destroyAllWindows()
    ep_camera.stop_video_stream()
    ep_robot.close()
