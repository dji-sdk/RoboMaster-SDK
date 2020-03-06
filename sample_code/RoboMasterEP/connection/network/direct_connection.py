#! python3

import robot_connection

WIFI_DIRECT_CONNECTION_IP = '192.168.2.1'

robot = robot_connection.RobotConnection(WIFI_DIRECT_CONNECTION_IP)

if not robot.open():
    print('open fail')
    exit(1)

robot.send_data('command')
print('send data to robot   : command')
recv = robot.recv_ctrl_data(5)
print('recv data from robot : %s'%recv)


robot.send_data('version')
print('send data to robot   : version ?')
recv = robot.recv_ctrl_data(5)
print('recv data from robot : %s'%recv)

robot.send_data('quit')
print('send data to robot   : quit')
recv = robot.recv_ctrl_data(5)
print('recv data from robot : %s'%recv)

robot.close()
