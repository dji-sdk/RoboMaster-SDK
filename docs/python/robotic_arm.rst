===================
Robotic Arm
===================

.. function:: robotic_arm_ctrl.move(x, y, wait_for_complete=True)

    :Description: Set the relative position of the robotic arm movement

    :param int32 x: Set the distance of the horizontal movement of the robotic arm. A positive number is forward movement, and a negative number is backward movement. The accuracy is 1 mm
    :param int32 y: Set the distance of the vertical movement of the robotic arm. A positive number is upward movement, and a negative number is downward movement. The accuracy is 1 mm
    :param bool wait_for_complete: Whether to wait for execution to complete. The default setting is True

    :return: N/A

    :Example: ``robotic_arm_ctrl.move(40, 50, True)``

    :Example description: Set the robotic arm to move forward by 40 mm and upward by 50 mm, and wait for the execution to complete

.. function:: robotic_arm_ctrl.moveto(x, y, wait_for_complete=True)

    :Description: Set the movement of the robotic arm to an absolute coordinate (the absolute coordinate system and range are not given?)

    :param int32 x: Set the coordinate value of the horizontal movement of the robotic arm, with an accuracy of 1 mm
    :param int32 y: Set the coordinate value of the vertical movement of the robotic arm, with an accuracy of 1 mm
    :param bool wait_for_complete: Whether to wait for execution to complete. The default setting is True

    :return: N/A

    :Example: ``robotic_arm_ctrl.moveto(40, 50, True)``

    :Example description: Set the robotic arm to move to the absolute coordinate (x = 40mm, y = 50mm), and wait for the execution to complete

.. function:: robotic_arm_ctrl.get_position()

    :Description: Obtain the position of the robotic arm

    :param void: N/A

    :return: The absolute coordinate of the robotic arm, with an accuracy of 1 mm
    :rtype: List [x, y]. x and y are int32 types

    :Example: ``[x, y] = robotic_arm_ctrl.get_position()``

    :Example description: Obtain the absolute position of the robotic arm

.. function:: robotic_arm_ctrl.recenter()

    :Description: Set the robotic arm to go back to the center (move to an absolute coordinate?)

    :param void: N/A

    :return: N/A

    :Example: ``robotic_arm_ctrl.recenter()``

    :Example description: Set the robotic arm to go back to the center

