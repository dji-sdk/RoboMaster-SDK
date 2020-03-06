===================
Sensor
===================

.. function:: ir_distance_sensor_ctrl.enable_measure(port_id)

    :Description: Turn on the TOF ranging function

    :param int port_id: TOF module number. The range is [1:4]

    :return: None

    :Example: ``ir_distance_sensor_ctrl.enable_measure(1)``

    :Example description: Turn on the ranging function of TOF 1

.. function:: ir_distance_sensor_ctrl.disable_measure(port_id)

    :Description: Turn off the TOF ranging function

    :param int port_id: TOF module number. The range is [1:4]

    :return: None

    :Example: ``ir_distance_sensor_ctrl.disable_measure(1)``

    :Example description: Turn off the ranging function of TOF 1

.. function:: ir_distance_sensor_ctrl.get_distance_info(port_id)

    :Description: Obtain the ranging information from a TOF

    :param int port_id: TOF module number. The range is [1:4]

    :return: Distance of obstacle in front of the TOF, with an accuracy of 1 cm
    :rtype: uint16

    :Example: ``ir_distance_sensor_ctrl.get_distance_info(1)``

    :Example description: Obtain the ranging information from TOF 1

.. function:: def ir_distance_[port_id]_[compare_type]_[dist]_event(msg):

    :Description: When it is detected that the distance of the obstacle in front of the TOF module satisfies the condition, the program in the function is run

    :param int port_id: TOF module number. The range is [1:4]
    :param compare_type: Comparison type. It can be eq, ge, gt, le, and lt (i.e. equal to, greater than or equal to, greater than, less than or equal to, or less than)
    :param dist: The distance used for comparison, with an accuracy of 1 cm, a range of 5-500 cm, and an error rate of 5%

    :return: None

    :Example:
.. code-block:: python
    :linenos:

    #When the distance of the obstacle in front of TOF 1 is detected as less than 10 cm, the program in the function is run

    def ir_distance_1_lt_10_event(msg):
        pass

.. function:: ir_distance_sensor_ctrl.cond_wait('ir_distance_[port_id]_[compare_type]_[dist]')

    :Description: When the distance of the obstacle in front of the TOF module satisfies the condition, the next command is executed

    :param 'ir_distance_[port_id]_[compare_type]_[dist]': A string used for distance comparison. It contains the module number, comparison type, and distance
    :param int port_id: TOF module number. The range is [1:4]
    :param compare_type: Comparison type. It can be eq, ge, gt, le, and lt (i.e. equal to, greater than or equal to, greater than, less than or equal to, or less than)
    :param dist: The distance used for comparison, with an accuracy of 1 cm, a range of 5-500 cm, and an error rate of 5%

    :return: None

    :Example: ``ir_distance_sensor_ctrl.cond_wait('ir_distance_1_gt_50')``

    :Example description: When the distance of the obstacle in front of TOF 1 is greater than 50 cm, the next command is executed

.. function:: ir_distance_sensor_ctrl.check_condition('ir_distance_[port_id]_[compare_type]_[dist]')

    :Description: Judge whether the distance of the obstacle in front of the TOF module satisfies the condition

    :param 'ir_distance_[port_id]_[compare_type]_[dist]': A string used for distance comparison. It contains the module number, comparison type, and distance
    :param int port_id: TOF module number. The range is [1:4]
    :param compare_type: Comparison type. It can be eq, ge, gt, le, and lt (i.e. equal to, greater than or equal to, greater than, less than or equal to, or less than)
    :param dist: The distance used for comparison, with an accuracy of 1 cm, a range of 5-500 cm, and an error rate of 5%

    :return: Whether it satisfies the condition or not. When it does, it returns true; otherwise, it returns false.
    :rtype: bool

    :Example:
.. code-block:: python
    :linenos:

    # When the distance of the obstacle in front of TOF 1 is detected as less than 10 cm, the program in the function is run

    if ir_distance_sensor_ctrl.check_condition('ir_distance_1_gt_50'):
        pass
