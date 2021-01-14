===================
Mechanical Gripper
===================

.. function:: gripper_ctrl.open()

    :description: Controls the opening of the mechanical gripper

    :param void: None

    :return: None

    :example: ``gripper_ctrl.open()``

    :example description: Control the opening of the mechanical gripper

.. function:: gripper_ctrl.close()

    :description: Controls the closing of the mechanical gripper

    :param void: None

    :return: None

    :example: ``gripper_ctrl.close()``

    :example description: Control the closing of the mechanical gripper

.. function:: gripper_ctrl.stop()

    :description: Controls the stopping of the mechanical gripper

    :param void: None

    :return: None

    :example: ``gripper_ctrl.stop()``

    :example description: Control the stopping of the mechanical gripper

.. function:: gripper_ctrl.update_power_level(level)

    :description: Sets the force level of the gripper

    :param int level: The force level of the mechanical gripper, whose range is [1:4]. The default is 1.

    :return: None

    :example: ``gripper_ctrl.update_power_level(1)``

    :example description: Set the force level of the gripper to 1

.. function:: gripper_ctrl.is_closed()

    :description: Obtains the clamping state of the mechanical gripper

    :param void: None

    :return: The clamping state of the mechanical gripper. If the mechanical gripper is clamped, true is returned, otherwise false is returned.
    :rtype: bool

    :example: ``ret = gripper_ctrl.is_closed()``

    :example description: Obtain the clamping state of the mechanical gripper

.. function:: gripper_ctrl.is_open()

    :description: Obtains the open state of the mechanical gripper

    :param void: None

    :return: The open state of the mechanical gripper. If the mechanical gripper is fully opened, true is returned, otherwise false is returned.
    :rtype: bool

    :example: ``ret = gripper_ctrl.is_open()``

    :example description: Obtain the open state of the mechanical gripper

.. hint:: For the description of the module, refer to :doc:`Mechanical Arm and Mechanical Gripper<../extension_module/robotic_arm_and_gripper>`.