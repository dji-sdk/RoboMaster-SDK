===================
Blaster
===================

.. function:: ir_blaster_ctrl.set_fire_count(count)

    :Description: Set the emission frequency of infrared beams, i.e. the number of infrared beams emitted per second

    :param int color_enum: Emission frequency, i.e. the number of infrared beams emitted per second. The range is [1:8]

    :return: None

    :Example: ``ir_blaster_ctrl.set_fire_count(4)``

    :Example description: Set the emission frequency of infrared beams to 4

.. function:: ir_blaster_ctrl.fire_once()

    :Description: Control the blaster to emit infrared beams once only

    :param void: None

    :return: None

    :Example: ``ir_blaster_ctrl.fire_once()``

    :Example description: Control the blaster to emit infrared beams once only

.. function:: ir_blaster_ctrl.fire_continuous()

    :Description: Control the blaster to emit infrared beams continuously

    :param void: None

    :return: None

    :Example: ``ir_blaster_ctrl.fire_continuous()``

    :Example description: Control the blaster to emit infrared beams continuously

.. function:: ir_blaster_ctrl.stop()

    :Description: Stop emitting infrared beams

    :param void: None

    :return: None

    :Example: ``ir_blaster_ctrl.stop()``

    :Example description: Stop emitting infrared beams
