===================
Armor plate
===================

.. py:function:: def ir_hit_detection_event(msg):

    :Description: When the robot detects that it is being attacked by infrared beams, programs in the function are run

    :param msg: Message parameters in the function

    :return: None

    :Example:
.. code-block:: python
    :linenos:

    #When the robot detects that it is being attacked by infrared beams, programs in the function are run

    def ir_hit_detection_event(msg):
        pass

.. function:: armor_ctrl.cond_wait(condition_enum)

    :Description: When the robot is attacked by infrared beams, the next command is executed

    :param condition_enum: The ``rm_define.cond_ir_hit_detection`` event type indicates that the robot is being attacked by infrared beams

    :return: None

    :Example: ``armor_ctrl.cond_wait(rm_define.cond_ir_hit_detection)``

    :Example description: When the robot is attacked by infrared beams, the next command is executed

.. function:: armor_ctrl.check_condition(condition_enum)

    :Description: Judge whether the robot is being attacked by infrared beams

    :param condition_enum: The ``rm_define.cond_ir_hit_detection`` event type indicates that the robot is being attacked by infrared beams

    :return: Whether the robot is attacked by infrared beams or not. It returns true when attacked, otherwise it returns false.
    :rtype: bool

    :Example: ``if armor_ctrl.check_condition(rm_define.cond_ir_hit_detection):``

    :Example description: If the robot is attacked by infrared beams, the next command is executed
