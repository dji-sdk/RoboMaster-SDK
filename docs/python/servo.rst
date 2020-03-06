===================
Servo
===================

.. function:: servo_ctrl.get_angle(servo_id)

    :Description: Obtain the servo rotation angle

    :param uint8 servo_id: Servo number. The range is [1:4]

    :return: Servo angle, with an accuracy of 0.1 degrees
    :rtype: int32

    :Example: ``angle = servo_ctrl.get_angle(1)``

    :Example description: Obtain the rotation angle of servo 1

.. function:: servo_ctrl.set_angle(servo_id, angle, wait_for_complete=True)

    :Description: Set the servo rotation angle

    :param uint8 servo_id: Servo number. The range is [1:4]
    :param int32 angle: Rotation angle, with an accuracy of 0.1 degrees. A positive number indicates clockwise rotation, and a negative number indicates counterclockwise rotation
    :param bool wait_for_complete: Whether to wait for execution to complete. The default setting is True

    :return: None

    :Example: ``servo_ctrl.set_angle(1, 900, True)``

    :Example description: Set servo 1 to rotate 90° clockwise, and wait for the execution to complete

.. function:: servo_ctrl.recenter(servo_id, wait_for_complete=True)

    :Description: Set the servo to go back to center

    :param uint8 servo_id: Servo number. The range is [1:4]
    :param bool wait_for_complete: Whether to wait for execution to complete. The default setting is True

    :return: N/A

    :Example: ``servo_ctrl.recenter(1, True)``

    :Example description: Set servo 1 to go back to center, and wait for execution to complete

.. function:: servo_ctrl.set_speed(servo_id, speed)

    :Description: Set the servo rotation speed

    :param uint8 servo_id: Servo number. The range is [1:4]
    :param int32 speed: Rotation speed, with an accuracy is 1 degree per second. A positive number indicates clockwise rotation, and a negative number indicates counterclockwise rotation

    :return: None

    :Example: ``servo_ctrl.set_speed(1, 5)``

    :Example description: Set servo 1 to rotate clockwise at 5 degrees per second

