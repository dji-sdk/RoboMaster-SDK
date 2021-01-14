===================
Armor Plate
===================

.. py:function:: def ir_hit_detection_event(msg):

    :description: After detecting the robot is under attack by infrared beams, run the program in the function

    :param msg: Message parameter in the function

    :return: None

    :example:
.. code-block:: python
    :linenos:

    #After detecting that the robot is under attack by infrared beams, run the program in the function.

    def ir_hit_detection_event(msg):
        pass

.. function:: armor_ctrl.cond_wait(condition_enum)

    :description: When the waiting robot is under attack by infrared beams, execute the next instruction

    :param condition_enum: Event type, ``rm_define.cond_ir_hit_detection'' indicates that the robot is under attack by infrared beams

    :return: None

    :example: ``armor_ctrl.cond_wait(rm_define.cond_ir_hit_detection)``

    :example description: When the waiting robot is under attack by infrared beams, execute the next instruction

.. function:: armor_ctrl.check_condition(condition_enum)

    :description: Determine whether the robot is under attack by infrared beams

    :param condition_enum: Event type, ``rm_define.cond_ir_hit_detection'' indicates that the robot is under attack by infrared beams

    :return: Whether the robot is under attack by infrared beams. If yes, true is returned. If no, false is returned.
    :rtype: bool

    :example: ``if armor_ctrl.check_condition(rm_define.cond_ir_hit_detection):``

    :example description: If the robot is under attack by infrared beams, execute the next instruction