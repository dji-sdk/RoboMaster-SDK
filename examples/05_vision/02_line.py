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


class PointInfo:

    def __init__(self, x, y, theta, c):
        self._x = x
        self._y = y
        self._theta = theta
        self._c = c

    @property
    def pt(self):
        return int(self._x * 1280), int(self._y * 720)

    @property
    def color(self):
        return 255, 255, 255


line = []


def on_detect_line(line_info):
    number = len(line_info)
    line.clear()
    line_type = line_info[0]
    print('line_type', line_type)
    for i in range(1, number):
        x, y, ceta, c = line_info[i]
        line.append(PointInfo(x, y, ceta, c))


if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    ep_vision = ep_robot.vision
    ep_camera = ep_robot.camera

    ep_camera.start_video_stream(display=False)
    result = ep_vision.sub_detect_info(name="line", color="blue", callback=on_detect_line)

    for i in range(0, 500):
        img = ep_camera.read_cv2_image(strategy="newest", timeout=0.5)
        for j in range(0, len(line)):
            cv2.circle(img, line[j].pt, 3, line[j].color, -1)
        cv2.imshow("Line", img)
        cv2.waitKey(1)
    cv2.destroyAllWindows()
    result = ep_vision.unsub_detect_info(name="line")
    cv2.destroyAllWindows()
    ep_camera.stop_video_stream()
    ep_robot.close()
