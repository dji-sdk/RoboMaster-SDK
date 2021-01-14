===================
Blaster
===================

.. function:: ir_blaster_ctrl.set_fire_count(count)

    :description: Sets the emission frequency of infrared beams, i.e., the number of infrared beams emitted per second

    :param int color_enum: The emission frequency, i.e. the number of infrared beams emitted per second, whose range is [1:8]

    :return: None

    :example: ``ir_blaster_ctrl.set_fire_count(4)``

    :example description: Set the emission frequency of infrared beams to 4

.. function:: ir_blaster_ctrl.fire_once()

    :description: Instructs the blaster to emit a single infrared beam

    :param void: None

    :return: None

    :example: ``ir_blaster_ctrl.fire_once()``

    :example description: Instruct the blaster to emit a single infrared beam

.. function:: ir_blaster_ctrl.fire_continuous()

    :description: Instructs the blaster to continuously emit infrared beams

    :param void: None

    :return: None

    :example: ``ir_blaster_ctrl.fire_continuous()``

    :example description: Instruct the blaster to continuously emit infrared beams

.. function:: ir_blaster_ctrl.stop()

    :description: Stops infrared beam emission

    :param void: None

    :return: None

    :example: ``ir_blaster_ctrl.stop()``

    :example description: Stop infrared beam emission