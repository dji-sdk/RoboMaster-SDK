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
import struct
import robomaster
from robomaster import robot


if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    uart = ep_robot.uart

    uart.serial_param_set(baud_rate=0, data_bit=1, odd_even=0, \
                             stop_bit=0, rx_en=1, tx_en=1, rx_size=50, tx_size=50)

    send_dict = {'dict':'hello world','number':10 ,'symbol':'\n'}

    for i in range(1, 10):
        uart.serial_send_msg(send_dict)

    send_tuple = ('tuple', 'string', '123', 45, 'hello','\n')

    for i in range(1,10):
        uart.serial_send_msg(send_tuple)

    send_str = 'test for serial send'

    for i in range(1,10):
        uart.serial_send_msg(send_str)

    send_byte = bytearray(20)
    for i in range(1, 20):
        send_byte[i] = i

    for i in range(1,10):
        uart.serial_send_msg(send_byte)

    time.sleep(3)

    ep_robot.close()
