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
import robomaster
from robomaster import robot
import cv2


if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    ep_camera = ep_robot.camera

    # 每次获取最新的1帧图像显示，并停留1秒
    ep_camera.start_video_stream(display=False)
    for i in range(0, 10):
        img = ep_camera.read_cv2_image(strategy="newest")
        cv2.imshow("Robot", img)
        cv2.waitKey(1)
        time.sleep(1)
    cv2.destroyAllWindows()
    ep_camera.stop_video_stream()

    ep_robot.close()
