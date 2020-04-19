===================
UART
===================

.. function:: serial_ctrl.serial_config(baud_rate, data_bit, odd_even, stop_bit)

    :描述: 设置串口的波特率、数据位、校验位以及停止位属性

    :param baud_rate: 设置波特率，可选波特率为 9600、19200、38400、57600、115200
    :param data_bit: 设置数据位，可选的数据位为 cs7、cs8
    :param odd_even_crc: 设置奇偶校验，详细见表格 :data:`odd_even_crc`
    :param stop_bit: 设置停止位，可选的停止位为 1、2

    :return: 无

    :示例: ``serial_ctrl.serial_config(9600, 'cs8', 'none', 1)``

    :示例说明: 设置串口的波特率为 9600，数据位 8 位，不使用奇偶校验，停止位为 1 位

.. function:: serial_ctrl.write_line(msg_string)

    :描述: 发送字符串信息，自动添加换行 ``'\n'``

    :param string msg_string: 需要发送的字符串信息，发送时字符串后自动添加 ``'\n'``

    :return: 无

    :示例: ``serial_ctrl.write_line('RoboMaster EP')``

    :示例说明: 向串口写入 ``'RoboMaster EP\n'`` ，最后的换行自动添加，用户只需要发送 ``'RoboMaster EP'``

.. function:: serial_ctrl.write_string(msg_string)

    :描述: 发送字符串信息

    :param string msg_string: 需要发送的字符串信息

    :return: 无

    :示例: ``serial_ctrl.write_string('RoboMaster EP')``

    :示例说明: 向串口写入 ``'RoboMaster EP'``

.. function:: serial_ctrl.write_number(value)

    :描述: 将数字参数转换成字符串，并通过串口发送出去

    :param int value: 需要发送的值

    :return: 无

    :示例: ``serial_ctrl.write_number(12)``

    :示例说明: 向串口中写入字符串 ``'12'``

.. function:: serial_ctrl.write_numbers(value1, value2, value3...)

    :描述: 将数字列表转换成字符串，并通过串口发送出去

    :param int value1: 需要发送数字列表的值
    :param int value2: 需要发送数字列表的值
    :param int value3: 需要发送数字列表的值

    :return: 无

    :示例: ``serial_ctrl.write_numbers(12,13,14)``

    :示例说明: 向串口中写入字符串 ``'12,13,14'``

.. function:: serial_ctrl.write_value(key, value)

    :描述: 将参数以键值对的形式组成字符串，并通过串口发送出去

    :param string key: 需要发送的关键字
    :param int value: 需要发送的值

    :return: 无

    :示例: ``serial_ctrl.write_value('x', 12)``

    :示例说明: 向串口中写入字符串 ``'x:12'``

.. function:: serial_ctrl.read_line([timeout])

    :描述: 从串口中读取以 ``'\n'`` 结尾的字符串

    :param float timeout: 可选，超时时间，单位为秒，默认为永久阻塞

    :return: 通过串口读取到的字符串
    :rtype: string

    :示例: ``recv = serial_ctrl.read_line()``

    :示例说明: 从串口读取一行以 ``'\n'`` 结尾的字符串

.. function:: serial_ctrl.read_string([timeout])

    :描述: 从串口中读取字符串（字符串可以不以 ``'\n'`` 结尾）

    :param float timeout: 可选，超时时间，单位为秒，默认为永久阻塞

    :return: 通过串口读取到的字符串
    :rtype: string

    :示例: ``recv = serial_ctrl.read_string()``

    :示例说明: 从串口读取一个字符串

.. function:: serial_ctrl.read_until(stop_sig, [timeout])

    :描述: 从串口中读取字符串，直到匹配到指定的结束字符 ``'stop_sig'``

    :param stop_sig: 指定的结束字符，参数类型为字符，范围为[ ``'\n'`` | ``'$'`` | ``'#'`` | ``'.'`` | ``':'`` | ``';'`` ]
    :param float timeout: 可选，超时时间，单位为秒，默认为永久阻塞

    :return: 通过串口读取到的匹配字符串
    :rtype: string

    :示例: ``serial_ctrl.read_until('#')``

    :示例说明: 从串口中读取字符串，直到匹配到 ``'#'`` 停止读取

.. data:: odd_even_crc

        +------------+---------------+
        |    none    | 不使用奇偶校验|
        +------------+---------------+
        |    odd     | 使用奇校验    |
        +------------+---------------+
        |    even    | 使用偶校验    |
        +------------+---------------+

.. hint:: 模块说明请参考 :doc:`UART <../extension_module/uart>`