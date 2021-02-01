===================
機械臂
===================

.. function:: robotic_arm_ctrl.move(x, y, wait_for_complete=True)

    :描述: 設置機械臂運動的相對位置

    :param int32 x: 設置機械臂水平運動的距離，正數為向前運動，負數為向後運動，精確度為 1 mm
    :param int32 y: 設置機械臂垂直運動的距離，正數為向上運動，負數為向下運動，精確度為 1 mm
    :param bool wait_for_complete: 是否等待執行完成，默認為 True

    :return: 無

    :示例: ``robotic_arm_ctrl.move(40, 50, True)``

    :示例說明: 設置機械臂向前移動 20 mm，向上移動 30 mm，等待執行完成

.. function:: robotic_arm_ctrl.moveto(x, y, wait_for_complete=True)

    :描述: 設置機械臂運動到絕對坐標

    :param int32 x: 設置機械臂水平運動的坐標值，精確度為 1 mm
    :param int32 y: 設置機械臂垂直運動的坐標值，精確度為 1 mm
    :param bool wait_for_complete: 是否等待執行完成，默認為 True

    :return: 無

    :示例: ``robotic_arm_ctrl.moveto(40, 50, True)``

    :示例說明: 設置機械臂移動到（x=40mm，y=50mm）的絕對坐標，等待執行完成

.. function:: robotic_arm_ctrl.get_position()

    :描述: 獲取機械臂位置

    :param void: 無

    :return: 機械臂的絕對坐標，精確度為 1 mm
    :rtype: 列表[x, y], x 和 y 為 int32 類型

    :示例: ``[x, y] = robotic_arm_ctrl.get_position()``

    :示例說明: 獲取機械臂的絕對坐標

.. function:: robotic_arm_ctrl.recenter()

    :描述: 設置機械臂回中

    :param void: 無

    :return: 無

    :示例: ``robotic_arm_ctrl.recenter()``

    :示例說明: 設置機械臂回中

.. hint:: 模塊說明請參考 :doc:`機械臂與機械爪 <../extension_module/robotic_arm_and_gripper>`