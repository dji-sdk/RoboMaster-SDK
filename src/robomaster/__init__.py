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


import sys
if sys.version_info < (3, 6, 5):
    sys.exit('RoboMaster Sdk requires Python 3.6.5 or later')

import logging
import time

logger_name = "sdk"
logger = logging.getLogger(logger_name)
logger.setLevel(logging.ERROR)

fmt = "%(asctime)-15s %(levelname)s %(filename)s:%(lineno)d %(message)s"
formatter = logging.Formatter(fmt)
sh = logging.StreamHandler()
sh.setFormatter(formatter)
logger.addHandler(sh)


def enable_logging_to_file():
    logger.setLevel(logging.INFO)
    filename = "RoboMasterSDK_{0}_log.txt".format(time.strftime("%Y%m%d%H%M%S", time.localtime()))
    fh = logging.FileHandler(filename)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


__all__ = ['logger', 'protocol', 'config', 'version', 'action', 'conn', 'client', 'module',
           'robot', 'gimbal', 'chassis', 'gripper', 'blaster', 'camera', 'media', 'flight',
           'led', 'robotic_arm', 'vision', 'sensor', 'ai_module']
