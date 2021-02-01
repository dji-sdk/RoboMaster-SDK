===================
紅外深度傳感器
===================

.. function:: ir_distance_sensor_ctrl.enable_measure(port_id)

    :描述: 開啟紅外深度傳感器測距功能

    :param int port_id: 紅外深度傳感器模塊編號，範圍為[1:4]

    :return: 無

    :示例: ``ir_distance_sensor_ctrl.enable_measure(1)``

    :示例說明: 開啟 1 號紅外深度傳感器測距功能

.. function:: ir_distance_sensor_ctrl.disable_measure(port_id)

    :描述: 關閉紅外深度傳感器測距功能

    :param int port_id: 紅外深度傳感器模塊編號，範圍為[1:4]

    :return: 無

    :示例: ``ir_distance_sensor_ctrl.disable_measure(1)``

    :示例說明: 關閉 1 號紅外深度傳感器測距功能

.. function:: ir_distance_sensor_ctrl.get_distance_info(port_id)

    :描述: 獲取紅外深度傳感器測距信息

    :param int port_id: 紅外深度傳感器模塊編號，範圍為[1:4]

    :return: 紅外深度傳感器前方障礙物的距離，精確度為 1 cm
    :rtype: uint16

    :示例: ``ir_distance_sensor_ctrl.get_distance_info(1)``

    :示例說明: 獲取 1 號紅外深度傳感器測距信息

.. function:: def ir_distance_[port_id]_[compare_type]_[dist]_event(msg):

    :描述: 當檢測到紅外深度傳感器模塊前方障礙物距離滿足條件時，運行函數內程序

    :param int port_id: 紅外深度傳感器模塊編號，範圍為[1:4]
    :param compare_type: 比較類型，可以為 eq, ge, gt, le, lt, 分別表示等於，大於等於，大於，小於等於，小於
    :param dist: 用於比較的距離，精確度為 1 cm，範圍為 5~500 cm，誤差率為 5%

    :return: 無

    :示例:
.. code-block:: python
    :linenos:

    #當檢測到 1 號紅外深度傳感器前方障礙物距離小於 10 cm 時，運行函數內程序

    def ir_distance_1_lt_10_event(msg):
        pass

.. function:: ir_distance_sensor_ctrl.cond_wait('ir_distance_[port_id]_[compare_type]_[dist]')

    :描述: 等待紅外深度傳感器模塊前方障礙物距離滿足條件時，執行下一條指令

    :param 'ir_distance_[port_id]_[compare_type]_[dist]': 用於距離比較的字符串，含模塊編號，比較類型和距離
    :param int port_id: 紅外深度傳感器模塊編號，範圍為[1:4]
    :param compare_type: 比較類型，可以為 eq, ge, gt, le, lt, 分別表示等於，大於等於，大於，小於等於，小於
    :param dist: 用於比較的距離，精確度為 1 cm，範圍為 5~500 cm，誤差率為 5%

    :return: 無

    :示例: ``ir_distance_sensor_ctrl.cond_wait('ir_distance_1_gt_50')``

    :示例說明: 等待 1 號紅外深度傳感器模塊前方障礙物距離大於 50 cm 時，執行下一條指令

.. function:: ir_distance_sensor_ctrl.check_condition('ir_distance_[port_id]_[compare_type]_[dist]')

    :描述: 判斷紅外深度傳感器模塊前方障礙物距離是否滿足條件

    :param 'ir_distance_[port_id]_[compare_type]_[dist]': 用於距離比較的字符串，含模塊編號，比較類型和距離
    :param int port_id: 紅外深度傳感器模塊編號，範圍為[1:4]
    :param compare_type: 比較類型，可以為 eq, ge, gt, le, lt, 分別表示等於，大於等於，大於，小於等於，小於
    :param dist: 用於比較的距離，精確度為 1 cm，範圍為 5~500 cm，誤差率為 5%

    :return: 是否滿足條件，滿足條件時返回真，否則返回假。
    :rtype: bool

    :示例:
.. code-block:: python
    :linenos:

    #當檢測到 1 號紅外深度傳感器前方障礙物距離小於 10 cm 時，運行函數內程序

    if ir_distance_sensor_ctrl.check_condition('ir_distance_1_gt_50'):
        pass

.. hint:: 模塊說明請參考 :doc:`紅外深度傳感器 <../extension_module/ir_distance_sensor>`