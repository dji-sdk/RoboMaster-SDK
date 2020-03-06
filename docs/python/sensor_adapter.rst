===================
Adaptor
===================

.. function:: sensor_adapter_ctrl.get_sensor_adapter_adc(board_id, port_num)

    :Description: Obtain the ADC value of the analog pin of the corresponding port of the sensor adaptor

    :param int board_id: Sensor adaptor number. The range is [1:6]
    :param uint8 port_num: The port number on the sensor adaptor. The range is [1:2]
    :param bool wait_for_complete: Whether to wait for execution to complete. The default setting is True

    :return: The ADC value of analog pin of the corresponding port of the sensor adaptor. The range is [0:1023]
    :rtype: uint16

    :Example: ``ret = sensor_adapter_ctrl.get_sensor_adapter_adc(1, 2)``

    :Example description: Obtain the ADC value of the analog pin of port 2 of sensor adaptor 1

.. function:: sensor_adapter_ctrl.get_sensor_adapter_pulse_period(board_id, port_num)

    :Description: Obtain the pulse duration of the corresponding port pin of the sensor adaptor

    :param int board_id: Sensor adaptor number. The range is [1:6]
    :param uint8 port_num: The port number on the sensor adaptor. The range is [1:2]

    :return: The pulse duration of the corresponding port pin of the sensor adaptor, with an accuracy of 1 ms
    :rtype: uint32

    :Example: ``ret = sensor_adapter_ctrl.get_sensor_pulse_period(1, 2)``

    :Example description: Obtain the pulse duration of port 2 pin of sensor adaptor 1

.. function:: def sensor_adapter[board_id]_port[port_id]_[judge_type]_event(msg):

    :Description: When it is detected that the corresponding port pin of the sensor adaptor jumps to high level/low level/bidirectional, the program in the function is run

    :param int board_id: Sensor adaptor number. The range is [1:6]
    :param uint8 port_num: The port number on the sensor adaptor. The range is [1:2]
    :param judge_type: Trigger condition, which can be high, low, and trigger, indicating high level, low level, or bidirectional jumping, respectively

    :return: N/A

    :Example:
.. code-block:: python
    :linenos:

    #When it is detected that the pin of port 2 of sensor adaptor 1 jumps to a high level, the program in the function is run

    def sensor_adapter1_port2_high_event(msg):
        pass

.. function:: sensor_adapter_ctrl.cond_wait(rm_define.cond_sensor_adapter[board_id]_port[port_id]_[judge_type]_event)

    :Description: When the pulse of the corresponding port pin of the sensor adaptor is high/low/jumping, the next command is executed

    :param int board_id: Sensor adaptor number. The range is [1:6]
    :param uint8 port_num: The port number on the sensor adaptor. The range is [1:2]
    :param judge_type: Trigger condition, which can be high, low, and trigger, indicating high level, low level, or bidirectional jumping, respectively

    :return: N/A

    :Example: ``sensor_adapter_ctrl.cond_wait(rm_define.cond_sensor_adapter1_port2_high_event)``

    :Example description: When the pin of port 2 of sensor adaptor 1 is at high level, the next command is executed

.. function:: sensor_adapter_ctrl.check_condition(rm_define.cond_sensor_adapter[board_id]_port[port_id]_[judge_type]_event)

    :Description: Judge whether the pulse of the corresponding port pin of the sensor adaptor is high/low/jumping

    :param int board_id: Sensor adaptor number. The range is [1:6]
    :param uint8 port_num: The port number on the sensor adaptor. The range is [1:2]
    :param judge_type: Trigger condition, which can be high, low, and trigger, indicating high level, low level, or bidirectional jumping, respectively

    :return: Whether it satisfies the condition or not. When it does, it returns true; otherwise, it returns false.
    :rtype: bool

    :Example:
.. code-block:: python
    :linenos:

    #If the port 2 pin of sensor adaptor 1 is jumping, the next command is executed

    if sensor_adapter_ctrl.check_condition(rm_define.cond_sensor_adapter1_port2_trigger_event):
        pass

