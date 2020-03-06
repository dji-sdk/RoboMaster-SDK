===================
轉接模組
===================

.. function:: sensor_adapter_ctrl.get_sensor_adapter_adc(board_id, port_num)

    :描述: 獲取感測器轉接模組相應埠類比引腳的 ADC 值

    :param int board_id: 感測器轉接模組編號，範圍為[1:6]
    :param uint8 port_num: 感測器轉接模組上的埠號，範圍為[1:2]
    :param bool wait_for_complete: 是否等待執行完成，預設為 True

    :return: 感測器轉接模組相應埠類比引腳的 ADC 值，範圍為[0:1023]
    :rtype: uint16

    :示例: ``ret = sensor_adapter_ctrl.get_sensor_adapter_adc(1, 2)``

    :示例說明: 獲取 1 號感測器轉接模組 2 號埠模擬引腳的 ADC 值

.. function:: sensor_adapter_ctrl.get_sensor_adapter_pulse_period(board_id, port_num)

    :描述: 獲取感測器轉接模組相應埠引腳的脈衝持續時間

    :param int board_id: 感測器轉接模組編號，範圍為[1:6]
    :param uint8 port_num: 感測器轉接模組上的埠號，範圍為[1:2]

    :return: 感測器轉接模組相應埠引腳的脈衝持續時間，精確度為 1 ms
    :rtype: uint32

    :示例: ``ret = sensor_adapter_ctrl.get_sensor_pulse_period(1, 2)``

    :示例說明: 獲取 1 號感測器轉接模組 2 號埠引腳脈衝持續時間

.. function:: def sensor_adapter[board_id]_port[port_id]_[judge_type]_event(msg):

    :描述: 當檢測到感測器轉接模組相應埠引腳跳變為高電平/低電平/雙向，運行函數內程式

    :param int board_id: 感測器轉接模組編號，範圍為[1:6]
    :param uint8 port_num: 感測器轉接模組上的埠號，範圍為[1:2]
    :param judge_type: 觸發條件，可以為 high, low, trigger，分別表示高電平，低電平還是雙向跳變

    :return: 無

    :示例:
.. code-block:: python
    :linenos:

    #當檢測到 1 號感測器轉接模組 2 號埠引腳跳變為高電平時，運行函數內程式

    def sensor_adapter1_port2_high_event(msg):
        pass

.. function:: sensor_adapter_ctrl.cond_wait(rm_define.cond_sensor_adapter[board_id]_port[port_id]_[judge_type]_event)

    :描述: 等待感測器轉接模組相應埠引腳脈衝為（高/低/跳變）時，執行下一條指令

    :param int board_id: 感測器轉接模組編號，範圍為[1:6]
    :param uint8 port_num: 感測器轉接模組上的埠號，範圍為[1:2]
    :param judge_type: 觸發條件，可以為 high, low, trigger，分別表示高電平，低電平還是雙向跳變

    :return: 無

    :示例: ``sensor_adapter_ctrl.cond_wait(rm_define.cond_sensor_adapter1_port2_high_event)``

    :示例說明: 等待 1 號感測器轉接模組 2 號埠引腳為高電平時，執行下一條指令

.. function:: sensor_adapter_ctrl.check_condition(rm_define.cond_sensor_adapter[board_id]_port[port_id]_[judge_type]_event)

    :描述: 判斷感測器轉接模組相應埠引腳脈衝是否為（高/低/跳變）

    :param int board_id: 感測器轉接模組編號，範圍為[1:6]
    :param uint8 port_num: 感測器轉接模組上的埠號，範圍為[1:2]
    :param judge_type: 觸發條件，可以為 high, low, trigger，分別表示高電平，低電平還是雙向跳變

    :return: 是否滿足條件，滿足條件時返回真，否則返回假。
    :rtype: bool

    :示例:
.. code-block:: python
    :linenos:

    #如果 1 號感測器轉接模組 2 號埠引腳正在跳變時，執行下一條指令

    if sensor_adapter_ctrl.check_condition(rm_define.cond_sensor_adapter1_port2_trigger_event):
        pass