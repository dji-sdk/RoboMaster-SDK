===================
Mechanical Arm
===================

.. function:: robotic_arm_ctrl.move(x, y, wait_for_complete=True)

    :description: Sets the relative movement position of the mechanical arm

    :param int32 x: Set the horizontal movement distance of the mechanical arm. A positive number indicates forward movement, and a negative number indicates backward movement. The accuracy is 1 mm.
    :param int32 y: Set the vertical movement distance of the mechanical arm. A positive number indicates upward movement, and a negative number indicates downward movement. The accuracy is 1 mm.
    :param bool wait_for_complete: Whether to wait for execution to be completed. The default value is True.

    :return: None

    :example: ``robotic_arm_ctrl.move(40, 50, True)``

    :example description: Set the mechanical arm to move 20 mm forward and 30 mm upward, and wait for execution to be completed

.. function:: robotic_arm_ctrl.moveto(x, y, wait_for_complete=True)

    :description: Sets the absolute coordinates of mechanical arm movement

    :param int32 x: Set the coordinates of horizontal arm movement, with an accuracy of 1 mm
    :param int32 y: Set the coordinates of vertical arm movement, with an accuracy of 1 mm
    :param bool wait_for_complete: Whether to wait for execution to be completed. The default value is True.

    :return: None

    :example: ``robotic_arm_ctrl.moveto(40, 50, True)``

    :example description: Set the absolute coordinates of the mechanical arm to (x=40mm, y=50mm) and wait for the execution to be completed

.. function:: robotic_arm_ctrl.get_position()

    :description: Obtains the position of the mechanical arm

    :param void: None

    :return: The absolute coordinates of the mechanical arm, with an accuracy of 1 mm
    :rtype: An [x, y] list, where x and y are of int32 type

    :example: ``[x, y] = robotic_arm_ctrl.get_position()``

    :example description: Obtain the absolute coordinates of the mechanical arm

.. function:: robotic_arm_ctrl.recenter()

    :description: Recenters the mechanical arm

    :param void: None

    :return: None

    :example: ``robotic_arm_ctrl.recenter()``

    :example description: Recenter the mechanical arm

.. hint:: For a description of the module, refer to :doc:`Mechanical Arm and Mechanical Gripper<../extension_module/robotic_arm_and_gripper>`.