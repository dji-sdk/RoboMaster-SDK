=============================
Infrared Distance Sensor
=============================

.. function:: ir_distance_sensor_ctrl.enable_measure(port_id)

    :description: Enables the ranging function of the infrared distance sensor

    :param int port_id: The module number of the infrared distance sensor, whose range is [1:4]

    :return: None

    :example: ``ir_distance_sensor_ctrl.enable_measure(1)``

    :example description: Enable the ranging function of infrared distance sensor 1

.. function:: ir_distance_sensor_ctrl.disable_measure(port_id)

    :description: Disables the ranging function of the infrared distance sensor

    :param int port_id: The module number of the infrared distance sensor, whose range is [1:4]

    :return: None

    :example: ``ir_distance_sensor_ctrl.disable_measure(1)``

    :example description: Disable the ranging function of infrared distance sensor 1

.. function:: ir_distance_sensor_ctrl.get_distance_info(port_id)

    :description: Obtains the ranging information of the infrared distance sensor

    :param int port_id: The module number of the infrared distance sensor, whose range is [1:4]

    :return: The distance to the obstacle in front of the infrared distance sensor, with an accuracy of 1 cm
    :rtype: uint16

    :example: ``ir_distance_sensor_ctrl.get_distance_info(1)``

    :example description: Obtain the ranging information of infrared distance sensor 1

.. function:: def ir_distance_[port_id]_[compare_type]_[dist]_event(msg):

    :description: When the distance to the obstacle in front of the infrared distance sensor is judged to satisfy the relevant conditions, run the program in the function

    :param int port_id: The module number of the infrared distance sensor, whose range is [1:4]
    :param compare_type: The comparison type, which can be eq (equal), ge (greater than or equal to), gt (greater than), le (less than or equal to), or lt (less than).
    :param dist: The distance used for comparison, with an accuracy of 1 cm, range of 5-500 cm, and error rate of 5%

    :return: None

    :example:
.. code-block:: python
    :linenos:

    #When the distance to the obstacle in front of the infrared distance sensor is judged to satisfy the relevant conditions, run the program in the function

    def ir_distance_1_lt_10_event(msg):
        pass

.. function:: ir_distance_sensor_ctrl.cond_wait('ir_distance_[port_id]_[compare_type]_[dist]')

    :description: When the distance to the obstacle in front of the waiting infrared distance sensor is judged to satisfy the relevant conditions, execute the next instruction

    :param 'ir_distance_[port_id]_[compare_type]_[dist]': The string used for distance comparison, which includes the module number, comparison type, and distance
    :param int port_id: The module number of the infrared distance sensor, whose range is [1:4]
    :param compare_type: The comparison type, which can be eq (equal), ge (greater than or equal to), gt (greater than), le (less than or equal to), or lt (less than).
    :param dist: The distance used for comparison, with an accuracy of 1 cm, range of 5-500 cm, and error rate of 5%

    :return: None

    :example: ``ir_distance_sensor_ctrl.cond_wait('ir_distance_1_gt_50')``

    :example description: If the distance to the obstacle in front of infrared distance sensor 1 is greater than 50 cm, execute the next instruction

.. function:: ir_distance_sensor_ctrl.check_condition('ir_distance_[port_id]_[compare_type]_[dist]')

    :description: Determines whether the distance to the obstacle in front of the infrared distance sensor meets the relevant conditions

    :param 'ir_distance_[port_id]_[compare_type]_[dist]': The string used for distance comparison, which includes the module number, comparison type, and distance
    :param int port_id: The module number of the infrared distance sensor, whose range is [1:4]
    :param compare_type: The comparison type, which can be eq (equal), ge (greater than or equal to), gt (greater than), le (less than or equal to), or lt (less than).
    :param dist: The distance used for comparison, with an accuracy of 1 cm, range of 5-500 cm, and error rate of 5%

    :return: Whether the relevant conditions are satisfied. If yes, true is returned. If no, false is returned.
    :rtype: bool

    :example:
.. code-block:: python
    :linenos:

    #When the distance to the obstacle in front of the infrared distance sensor is judged to satisfy the relevant conditions, run the program in the function

    if ir_distance_sensor_ctrl.check_condition('ir_distance_1_gt_50'):
        pass

.. hint:: For the description of the module, refer to :doc:`Infrared Distance Sensor<../extension_module/ir_distance_sensor>`.