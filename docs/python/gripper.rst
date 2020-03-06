===================
Gripper
===================

.. function:: gripper_ctrl.open()

    :Description: Control the gripper to open

    :param void: None

    :return: None

    :Example: ``gripper_ctrl.open()``

    :Example description: Control the gripper to open

.. function:: gripper_ctrl.close()

    :Description: Control the gripper to close

    :param void: None

    :return: None

    :Example: ``gripper_ctrl.close()``

    :Example description: Control the gripper to close

.. function:: gripper_ctrl.stop()

    :Description: Control the gripper to stop moving

    :param void: None

    :return: None

    :Example: ``gripper_ctrl.stop()``

    :Example description: Control the gripper to stop moving

.. function:: gripper_ctrl.update_power_level(level)

    :Description: Set the force of the gripper

    :param int level: The force of the gripper. The range is [1:4], and the default is 1

    :return: None

    :Example: ``gripper_ctrl.update_power_level(1)``

    :Example description: Set the force of the gripper to 1

.. function:: gripper_ctrl.is_closed()

    :Description: Obtain the clamping state of the gripper

    :param void: None

    :return: The clamping state of the gripper. If the gripper is clamped, it returns true; otherwise, it returns false
    :rtype: bool

    :Example: ``ret = gripper_ctrl.is_closed()``

    :Example description: Obtain the clamping state of the gripper

.. function:: gripper_ctrl.is_open()

    :Description: Obtain the opening state of the gripper

    :param void: None

    :return: The opening state of the gripper. If the gripper is fully open, it returns true; otherwise, it returns false
    :rtype: bool

    :Example: ``ret = gripper_ctrl.is_open()``

    :Example description: Obtain the opening state of the gripper
