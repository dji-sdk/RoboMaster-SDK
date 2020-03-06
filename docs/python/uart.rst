===================
UART
===================

.. function:: serial_ctrl.serial_config(baud_rate, data_bit, odd_even, stop_bit)

    :描述: 設定串口的傳輸速率、數據位元、校驗位以及停止位屬性

    :param baud_rate: 設定傳送速率，可選傳送速率為 9600、19200、38400、57600、115200
    :param data_bit: 設定數據位元，可選的數據位元為 cs7、cs8
    :param odd_even_crc: 設定同位，詳情見表格 :data:`odd_even_crc`
    :param stop_bit: 設定停止位，可選的停止位為 1、2

    :return: 無

    :示例: ``serial_ctrl.serial_config(9600, 'cs8', 'none', '1')``

    :示例說明: 設定串口的傳送速率為 9600，數據位元 8 位，不使用同位，停止位為 1 位

.. function:: serial_ctrl.write_line(msg_string)

    :描述: 發送字符串資訊，自動添加換行 ``'\n'``

    :param string msg_string: 需要發送的字符串資訊，發送時字符串後自動添加 ``'\n'``

    :return: 無

    :示例: ``serial_ctrl.write_line('RoboMaster EP')``

    :示例說明: 向串口寫入 ``'RoboMaster EP\n'`` ，最後的換行自動添加，使用者只需要發送 ``'RoboMaster EP'``

.. function:: serial_ctrl.write_string(msg_string)

    :描述: 發送字符串資訊

    :param string msg_string: 需要發送的字符串資訊

    :return: 無

    :示例: ``serial_ctrl.write_string('RoboMaster EP')``

    :示例說明: 向串口寫入 ``'RoboMaster EP'``

.. function:: serial_ctrl.writ_numbers(key, value)

    :描述: 將參數以鍵值對的形式組成字串，並通過串口發送出去

    :param string key: 需要發送的關鍵字
    :param uint32 value: 需要發送的值

    :return: 無

    :示例: ``serial_ctrl.writ_numbers('x', 12)``

    :示例說明: 向串口中寫入字符串 ``'x:12'``

.. function:: serial_ctrl.read_line()

    :描述: 從串口中讀取以 ``'\n'`` 結尾的字符串

    :param void: 無

    :return: 通過串口讀取到的字符串
    :rtype: string

    :示例: ``recv = serial_ctrl.read_line()``

    :示例說明: 從串口讀取一行以 ``'\n'`` 結尾的字符串

.. function:: serial_ctrl.read_string()

    :描述: 從串口中讀取字符串（字符串可以不以 ``'\n'`` 結尾）

    :param void: 無

    :return: 通過串口讀取到的字符串
    :rtype: string

    :示例: ``recv = serial_ctrl.read_line()``

    :示例說明: 從串口讀取一個字符串

.. function:: serial_ctrl.read_until(stop_sig)

    :描述: 從串口中讀取字符串，直到匹配到指定的結束字符 ``'stop_sig'``

    :param stop_sig: 指定的結束字符，參數類型為字符，範圍為[ ``'\n'`` | ``'$'`` | ``'#'`` | ``'.'`` | ``':'`` | ``';'`` ]

    :return: 通過串口讀取到的匹配字符串
    :rtype: string

    :示例: ``serial_ctrl.read_until('#')``

    :示例說明: 從串口中讀取字符串，直到匹配到 ``'#'`` 停止讀取

.. data:: odd_even_crc

        +------------+-------------------+
        |    none    | 不使用同位        |
        +------------+-------------------+
        |    odd     | 使用奇數同位檢查  |
        +------------+-------------------+
        |    even    | 使用偶校驗        |
        +------------+-------------------+