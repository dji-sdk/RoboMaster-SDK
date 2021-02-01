===================
舵機
===================

.. function:: servo_ctrl.get_angle(servo_id)

    :描述: 獲取舵機旋轉角度

    :param uint8 servo_id: 舵機編號，範圍為[1:4]

    :return: 舵機角度，精確度為 0.1 度
    :rtype: int32

    :示例: ``angle = servo_ctrl.get_angle(1)``

    :示例說明: 獲取編號為 1 的舵機旋轉角度

.. function:: servo_ctrl.set_angle(servo_id, angle, wait_for_complete=True)

    :描述: 設置舵機旋轉角度

    :param uint8 servo_id: 舵機編號，範圍為[1:4]
    :param int32 angle: 旋轉角度，精確度為 0.1 度，正數為順時針旋轉，負數為逆時針旋轉
    :param bool wait_for_complete: 是否等待執行完成，默認為 True

    :return: 無

    :示例: ``servo_ctrl.set_angle(1, 900, True)``

    :示例說明: 設置編號為 1 的舵機順時針旋轉 90°，等待執行完成

.. function:: servo_ctrl.recenter(servo_id, wait_for_complete=True)

    :描述: 設置舵機回中

    :param uint8 servo_id: 舵機編號，範圍為[1:4]
    :param bool wait_for_complete: 是否等待執行完成，默認為 True

    :return: 無

    :示例: ``servo_ctrl.recenter(1, True)``

    :示例說明: 設置編號為 1 的舵機回中，等待執行完成

.. function:: servo_ctrl.set_speed(servo_id, speed)

    :描述: 設置舵機旋轉速度

    :param uint8 servo_id: 舵機編號，範圍為[1:4]
    :param int32 speed: 旋轉速度，精確度為 1 度/秒，正數為順時針旋轉，負數為逆時針旋轉

    :return: 無

    :示例: ``servo_ctrl.set_speed(1, 5)``

    :示例說明: 設置編號為 1 的舵機順時針旋轉，旋轉速度為 5 度/秒

.. hint:: 模塊說明請參考 :doc:`舵機 <../extension_module/servo>`