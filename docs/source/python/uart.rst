===================
UART
===================

.. function:: serial_ctrl.serial_config(baud_rate, data_bit, odd_even, stop_bit)

    :description: Sets the baud rate, data bit, parity bit, and stop bit attributes of the serial port

    :param baud_rate: Set the baud rate, which can be 9600, 19200, 38400, 57600, or 115200
    :param data_bit: Set the data bit, which can be cs7 or cs8
    :param odd_even_crc: Set parity check. For details, refer to the :data:`odd_even_crc` table.
    :param stop_bit: Set the stop bit, which can be 1 or 2

    :return: None

    :example: ``serial_ctrl.serial_config(9600, 'cs8', 'none', 1)``

    :example description: Set the baud rate to 9600, 8 data bits, no parity check, and 1 stop bit for the serial port

.. function:: serial_ctrl.write_line(msg_string)

    :description: Send string information and automatically add line breaks (``'\\n'``)

    :param string msg_string: The string information that needs to be sent. Automatically append line breaks (``'\\n'``) after the string when sending it.

    :return: None

    :example: ``serial_ctrl.write_line('RoboMaster EP')``

    :example description: Write ``'RoboMaster EP\\n'`` to the serial port and add line breaks automatically. You only need to send ``'RoboMaster EP'`` in this case.

.. function:: serial_ctrl.write_string(msg_string)

    :description: Send string information

    :param string msg_string: String information that needs to be sent

    :return: None

    :example: ``serial_ctrl.write_string('RoboMaster EP')``

    :example description: Write ``'RoboMaster EP'`` to the serial port

.. function:: serial_ctrl.write_number(value)

    :description: Convert the numeric parameter to a string and send the string through the serial port

    :param int value: The value that needs to be sent

    :return: None

    :example: ``serial_ctrl.write_number(12)``

    :example description: Write the ``'12'`` string to the serial port

.. function:: serial_ctrl.write_numbers(value1, value2, value3...)

    :description: Convert the list of numbers to a string and send the string through the serial port

    :param int value1: Value 1 in the list that needs to be sent
    :param int value2: Value 2 in the list that needs to be sent
    :param int value3: Value 3 in the list that needs to be sent

    :return: None

    :example: ``serial_ctrl.write_numbers(12,13,14)``

    :example description: Write the ``'12,13,14'`` string to the serial port

.. function:: serial_ctrl.write_value(key, value)

    :description: Converts the parameter to a string of key-value pairs and sends the string through the serial port

    :param string key: The key to be sent
    :param int value: The value to be sent

    :return: None

    :example: ``serial_ctrl.write_value('x', 12)``

    :example description: Write the ``'x:12'`` string to the serial port

.. function:: serial_ctrl.read_line([timeout])

    :description: Read the string ending with ``'\\n'`` from the serial port

    :param float timeout: An optional parameter, which indicates the timeout period in seconds. The default value of this parameter is permanent blocking.

    :return: The string read from the serial port
    :rtype: string

    :example: ``recv = serial_ctrl.read_line()``

    :example description: Read a string ending with ``'\\n'`` from the serial port

.. function:: serial_ctrl.read_string([timeout])

    :description: Read the string from the serial port (the string may or may not end with ``'\\n'``)

    :param float timeout: An optional parameter, which indicates the timeout period in seconds. The default value of this parameter is permanent blocking.

    :return: The string read from the serial port
    :rtype: string

    :example: ``recv = serial_ctrl.read_string()``

    :example description: Read a string from the serial port

.. function:: serial_ctrl.read_until(stop_sig, [timeout])

    :description: Reads a string from the serial port until the string matches the specified ``'stop_sig'`` ending character

    :param stop_sig: The specified ending character, whose type is char and range is [ ``'\n'`` | ``'$'`` | ``'#'`` | ``'.'`` | ``':'`` | ``';'`` ]
    :param float timeout: An optional parameter, which indicates the timeout period in seconds. The default value of this parameter is permanent blocking.

    :return: The matched string read from the serial port
    :rtype: string

    :example: ``serial_ctrl.read_until('#')``

    :example description: Read a string from the serial port until the ending character of the string matches ``'#'``

.. data:: odd_even_crc

        +------------+---------------+
        |    none    |    Do not perform parity check    |
        +------------+---------------+
        |    odd    |    Perform parity check (odd)   |
        +------------+---------------+
        |    even    |    Perform parity check (even)    |
        +------------+---------------+

.. hint:: For the description of the module, refer to :doc:`UART<../extension_module/uart>`.