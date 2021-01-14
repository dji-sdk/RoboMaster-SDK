===================
Sensor Adapter
===================

.. function:: sensor_adapter_ctrl.get_sensor_adapter_adc(board_id, port_num)

    :description: Obtains the ADC value of the analog pin for the corresponding port on the sensor adapter

    :param int board_id: The module number of the sensor adapter, whose range is [1:6]
    :param uint8 port_num: The number of the port on the sensor adapter, whose range is [1:2]
    :param bool wait_for_complete: Whether to wait for execution to be completed. The default value is True.

    :return: The ADC value of the analog pin for the corresponding port on the sensor adapter, whose range is [0:1023]
    :rtype: uint16

    :example: ``ret = sensor_adapter_ctrl.get_sensor_adapter_adc(1, 2)``

    :example description: Obtain the ADC value of the analog pin for port 2 on sensor adapter 1

.. function:: sensor_adapter_ctrl.get_sensor_adapter_pulse_period(board_id, port_num)

    :description: Obtains the pulse duration of the pin for the corresponding port on the sensor adapter

    :param int board_id: The module number of the sensor adapter, whose range is [1:6]
    :param uint8 port_num: The number of the port on the sensor adapter, whose range is [1:2]

    :return: The pulse duration of the pin for the corresponding port on the sensor adapter, with an accuracy of 1 ms
    :rtype: uint32

    :example: ``ret = sensor_adapter_ctrl.get_sensor_pulse_period(1, 2)``

    :example description: Obtain the pulse duration of the analog pin for port 2 on sensor adapter 1

.. function:: def sensor_adapter[board_id]_port[port_id]_[judge_type]_event(msg):

    :description: When the pulse on the pin of the corresponding port on the sensor adapter changes to high, low, or bidirectional, run the program in the function

    :param int board_id: The module number of the sensor adapter, whose range is [1:6]
    :param uint8 port_num: The number of the port on the sensor adapter, whose range is [1:2]
    :param judge_type: The trigger condition, which can be high, low, or trigger. These values indicate high level, low level, and bidirectional skipping respectively.

    :return: None

    :example:
.. code-block:: python
    :linenos:

    #When the pulse on the pin of port 2 on sensor adapter 1 changes to high, run the program in the function

    def sensor_adapter1_port2_high_event(msg):
        pass

.. function:: sensor_adapter_ctrl.cond_wait(rm_define.cond_sensor_adapter[board_id]_port[port_id]_[judge_type]_event)

    :description: When the pulse on the pin of the corresponding port on the waiting sensor adapter is high, low, or trigger, execute the next instruction

    :param int board_id: The module number of the sensor adapter, whose range is [1:6]
    :param uint8 port_num: The number of the port on the sensor adapter, whose range is [1:2]
    :param judge_type: The trigger condition, which can be high, low, or trigger. These values indicate high level, low level, and bidirectional skipping respectively.

    :return: None

    :example: ``sensor_adapter_ctrl.cond_wait(rm_define.cond_sensor_adapter1_port2_high_event)``

    :example description: When the pulse on the pin of port 2 on sensor adapter 1 is high, execute the next instruction

.. function:: sensor_adapter_ctrl.check_condition(rm_define.cond_sensor_adapter[board_id]_port[port_id]_[judge_type]_event)

    :description: Determines whether the pulse on the pin of the corresponding port on the sensor adapter is high, low, or trigger

    :param int board_id: The module number of the sensor adapter, whose range is [1:6]
    :param uint8 port_num: The number of the port on the sensor adapter, whose range is [1:2]
    :param judge_type: The trigger condition, which can be high, low, or trigger. These values indicate high level, low level, and bidirectional skipping respectively.

    :return: Whether the relevant conditions are satisfied. If yes, true is returned. If no, false is returned.
    :rtype: bool

    :example:
.. code-block:: python
    :linenos:

    #If the pulse on the pin of port 2 on sensor adapter 1 is trigger, execute the next instruction

    if sensor_adapter_ctrl.check_condition(rm_define.cond_sensor_adapter1_port2_trigger_event):
        pass

.. hint:: For the description of the module, refer to :doc:`Sensor Adapter<../extension_module/sensor_adapter>`.