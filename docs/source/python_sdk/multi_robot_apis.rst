.. _multi_robot_apis:

#############################################
Summary of RoboMaster SDK Multi-device APIs
#############################################

Currently, most of the APIs supported by multiple devices are used in the same way as for standalone devices. Therefore, this document mainly summarizes the APIs currently supported by multiple devices. This document also describes the different interfaces used in multi-device and standalone scenarios.
For a detailed description of the parameter types, value ranges, and return values of other APIs, refer to the descriptions of APIs for standalone devices.

Summary of multi-device APIs
******************************

For EP robots
_______________

+-----------+--------------------------------------------+
| module    |   api                                      |
+-----------+--------------------------------------------+
| chassis   | drive_wheels(w1, w2, w3, w4, timeout)      |
|           +--------------------------------------------+
|           | drive_speed(x, y, z, timeout)              |
|           +--------------------------------------------+
|           | move(x, y, z, xy_speed, z_speed)           |
+-----------+--------------------------------------------+
| gimbal    | recenter(pitch_speed, yaw_speed)           |
|           +--------------------------------------------+
|           | suspend()                                  |
|           +--------------------------------------------+
|           | resume()                                   |
|           +--------------------------------------------+
|           | move(pitch, yaw, pitch_speed, yaw_speed)   |
|           +--------------------------------------------+
|           | moveto(pitch, yaw, pitch_speed, yaw_speed) |
+-----------+--------------------------------------------+
| blaser    | fire(fire_type, times)                     |
|           +--------------------------------------------+
|           | set_led(brightness, effect)                |
+-----------+--------------------------------------------+
| led       | set_led(comp, r, g, b, effect, freq)       |
+-----------+--------------------------------------------+
|robotic_arm|recenter()                                  |
|           +--------------------------------------------+
|           |move(x, y)                                  |
|           +--------------------------------------------+
|           |moveto(x, y)                                |
+-----------+--------------------------------------------+
|gripper    |open(power)                                 |
|Pending     +--------------------------------------------+
|           |close(power)                                |
|           +--------------------------------------------+
|           |pause()                                     |
+-----------+--------------------------------------------+
|           |play_sound(sound_id, times)                 |
+-----------+--------------------------------------------+



For education-series robots
______________________________

+---------+--------------------------------------------------------------+
| module  |   api                                                        |
+---------+--------------------------------------------------------------+
| flight  | takeoff()                                                    |
|         +--------------------------------------------------------------+
|         | land()                                                       |
|         +--------------------------------------------------------------+
|         | up(distance)                                                 |
|         +--------------------------------------------------------------+
|         | down(distance)                                               |
|         +--------------------------------------------------------------+
|         | forward(distance)                                            |
|         +--------------------------------------------------------------+
|         | backword(distance)                                           |
|         +--------------------------------------------------------------+
|         | left(distance)                                               |
|         +--------------------------------------------------------------+
|         | right(distance)                                              |
|         +--------------------------------------------------------------+
|         | rotate(angle)                                                |
|         +--------------------------------------------------------------+
|         | flip_forward()                                               |
|         +--------------------------------------------------------------+
|         | flip_backward()                                              |
|         +--------------------------------------------------------------+
|         | flip_left()                                                  |
|         +--------------------------------------------------------------+
|         | flip_right()                                                 |
|         +--------------------------------------------------------------+
|         | go(distance)                                                 |
|         +--------------------------------------------------------------+
|         | mission_pad_on()                                             |
|         +--------------------------------------------------------------+
|         | mission_pad_off()                                            |
|         +--------------------------------------------------------------+
|         | motor_on()                                                   |
|         +--------------------------------------------------------------+
|         | mortor_off()                                                 |
+---------+--------------------------------------------------------------+
|         | set_led(r, g, b)                                             |
|         +--------------------------------------------------------------+
| led     | set_led_blink(freq, r1, g1, b1, r2, g2, b2)                  |
|         +--------------------------------------------------------------+
|         | set_led_breath(freq, r, g, b)                                |
|         +--------------------------------------------------------------+
|         | set_mled_bright(bright)                                      |
|         +--------------------------------------------------------------+
|         | set_mled_boot(display_graph)                                 |
|         +--------------------------------------------------------------+
|         | set_mled_sc()                                                |
|         +--------------------------------------------------------------+
|         | set_mled_graph(display_graph)                                |
|         +--------------------------------------------------------------+
|         | set_mled_char(color, display_char)                           |
|         +--------------------------------------------------------------+
|         | set_mled_char_scroll(direction, color, freq, display_str)    |
|         +--------------------------------------------------------------+
|         | set_mled_char_scroll(direction, color, freq, display_graph)  |
+---------+--------------------------------------------------------------+
| battery | get_battery()                                                |
+---------+--------------------------------------------------------------+

The use of the following two interfaces with multiple devices is different from their use with a standalone device:

1. The `go()` command of the `flight` module::

    go(go_dict)

    Parameter: go_dict {robot_id1: [x1, y1, z1, speed1, mid1], robot_id2: [x2, y2, z2, speed2, mid2], ... }
          Where, "robot_id" indicates the number of the drone, "x", "y", and "z" respectively indicate the x, y, and z coordinates of the go command for a standalone device, "speed" indicates the movement speed of the go command, and "mid" indicates the challenge card number of the go command.

    Return value: the multi_action object

2. Commands for the `led` module::

    The command_dict parameter has been recently added. This parameter controls the led module of a standalone drone by using command_dict. Its function is similar to that of the go command.

    Parameter: command_dict {robot_id1: [*args], robot_id2: [*args], ... }
          Where, robot_id indicates the number of the drone, and *args are the parameters for each led module

    Return value: the multi_action object

3. `get_battery()` command of the `battery` module::

    get_battery()

    Parameter: none

    Print the ID of the drone and its battery level to the console.

