===================
UART
===================

.. function:: serial_ctrl.serial_config(baud_rate, data_bit, odd_even, stop_bit)

    :Description: Set the serial port's baud rate, data bit, parity bit, and stop bit properties

    :param baud_rate: Set the baud rate. The optional baud rates are 9600, 19200, 38400, 57600, and 115200
    :param data_bit: Set the data bit. The optional data bits are cs7 and cs8
    :param odd_even_crc: Set the parity. For details, see table :data:`odd_even_crc`
    :param stop_bit: Set the stop bit. The optional stop bits are 1 and 2

    :return: None

    :Example: ``serial_ctrl.serial_config(9600, 'cs8', 'none', '1')``

    :Example description: Set the baud rate of the serial port to 9600, the data bit to 8, do not use parity, and set the stop bit to 1

.. function:: serial_ctrl.write_line(msg_string)

    :Description: Transmit string information by adding line feed ``'\n'`` automatically

    :param string msg_string: The string information to be transmitted. ``'\n'`` is added automatically to the end of the string while being transmitted

    :return: None

    :Example: ``serial_ctrl.write_line('RoboMaster EP')``

    :Example description: Write ``'RoboMaster EP\n'`` to the serial port. The last line feed will be added automatically. The user only needs to send ``'RoboMaster EP'``

.. function:: serial_ctrl.write_string(msg_string)

    :Description: Transmit string information

    :param string msg_string: String information to be transmitted

    :return: None

    :Example: ``serial_ctrl.write_string('RoboMaster EP')``

    :Example description: Write ``'RoboMaster EP'`` to the serial port

.. function:: serial_ctrl.writ_numbers(key, value)

    :Description: Form the parameters into strings in the form of key value pairs and transmit them through the serial port

    :param string key: Keywords to be transmitted
    :param uint32 value: Value to be transmitted

    :return: None

    :Example: ``serial_ctrl.writ_numbers('x', 12)``

    :Example description: Write the string ``'x:12'`` to the serial port

.. function:: serial_ctrl.read_line()

    :Description: Read strings ending with ``'\n'`` from the serial port

    :param void: None

    :return: The string read through the serial port
    :rtype: string

    :Example: ``recv = serial_ctrl.read_line()``

    :Example description: Read a line of strings ending with ``'\n'`` from the serial port

.. function:: serial_ctrl.read_string()

    :Description: Read strings from the serial port (It is OK if the strings do not end with ``'\n'``)

    :param void: None

    :return: The string read through the serial port
    :rtype: string

    :Example: ``recv = serial_ctrl.read_line()``

    :Example description: Read a string from the serial port

.. function:: serial_ctrl.read_until(stop_sig)

    :Description: Read strings from the serial port until the specified end character ``'stop_sig'`` is matched

    :param stop_sig: The specified end character. The parameter type is character. The range is [ ``'\n'`` | ``'$'`` | ``'#'`` | ``'.'`` | ``':'`` | ``';'`` ]

    :return: The matched string read through the serial port
    :rtype: string

    :Example: ``serial_ctrl.read_until('#')``

    :Example description: Read strings from the serial port until ``'#'`` is matched, and then stop reading

.. data:: odd_even_crc

        +------------+----------------------------+
        |    none    | Do not use the parity check|
        +------------+----------------------------+
        |    odd     | Use the odd check          |
        +------------+----------------------------+
        |    even    | Use the even check         |
        +------------+----------------------------+
