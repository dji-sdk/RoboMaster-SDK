#! python3

import robot_connection

robot = robot_connection.RobotConnection()

robot_ip = robot.get_robot_ip(10)

if robot_ip:
    print('robot ip: %s'%robot_ip)
    robot.update_robot_ip(robot_ip)

if not robot.open():
    print('open fail')
    exit(1)

robot.send_data('command')
print('send data to robot   : command')
recv = robot.recv_ctrl_data(5)
print('recv data from robot : %s'%recv)


robot.send_data('version ?')
print('send data to robot   : version ?')
recv = robot.recv_ctrl_data(5)
print('recv data from robot : %s'%recv)

robot.send_data('quit')
print('send data to robot   : quit')
recv = robot.recv_ctrl_data(5)
print('recv data from robot : %s'%recv)
