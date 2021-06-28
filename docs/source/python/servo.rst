===================
Servo
===================

.. function:: servo_ctrl.get_angle(servo_id)

    :description: Obtains the rotation angle of the servo

    :param uint8 servo_id: The number of the servo, whose range is [1:3]

    :return: The angle of the servo, with an accuracy of 0.1°
    :rtype: int32

    :example: ``angle = servo_ctrl.get_angle(1)``

    :example description: Obtain the rotation angle of servo 1

.. function:: servo_ctrl.set_angle(servo_id, angle, wait_for_complete=True)

    :description: Set the rotation angle of the servo

    :param uint8 servo_id: The number of the servo, whose range is [1:3]
    :param int32 angle: The rotation angle, with an accuracy of 0.1°. A positive number indicates clockwise rotation, and a negative number indicates counterclockwise rotation.
    :param bool wait_for_complete: Whether to wait for execution to be completed. The default value is True.

    :return: None

    :example: ``servo_ctrl.set_angle(1, 900, True)``

    :example description: Set servo 1 to rotate 90° clockwise and wait for execution to be completed

.. function:: servo_ctrl.recenter(servo_id, wait_for_complete=True)

    :description: Sets the servo back to normal

    :param uint8 servo_id: The number of the servo, whose range is [1:3]
    :param bool wait_for_complete: Whether to wait for execution to be completed. The default value is True.

    :return: None

    :example: ``servo_ctrl.recenter(1, True)``

    :example description: Set servo 1 back to normal and wait for execution to be completed

.. function:: servo_ctrl.set_speed(servo_id, speed)

    :description: Sets the rotation speed of the servo

    :param uint8 servo_id: The number of the servo, whose range is [1:3]
    :param int32 speed: The rotation speed, with an accuracy of 1 °/second. A positive number indicates clockwise rotation, and a negative number indicates counterclockwise rotation.

    :return: None

    :example: ``servo_ctrl.set_speed(1, 5)``

    :example description: Set servo 1 to rotate clockwise at a rotation speed of 5 °/second

.. hint:: For the description of the module, refer to :doc:`Servo<../extension_module/servo>`.
