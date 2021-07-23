===================
舵机
===================

.. function:: servo_ctrl.get_angle(servo_id)

    :描述: 获取舵机旋转角度

    :param uint8 servo_id: 舵机编号，范围为[1:3]

    :return: 舵机角度，精确度为 0.1 度
    :rtype: int32

    :示例: ``angle = servo_ctrl.get_angle(1)``

    :示例说明: 获取编号为 1 的舵机旋转角度

.. function:: servo_ctrl.set_angle(servo_id, angle, wait_for_complete=True)

    :描述: 设置舵机旋转角度

    :param uint8 servo_id: 舵机编号，范围为[1:3]
    :param int32 angle: 旋转角度，精确度为 0.1 度，正数为顺时针旋转，负数为逆时针旋转
    :param bool wait_for_complete: 是否等待执行完成，默认为 True

    :return: 无

    :示例: ``servo_ctrl.set_angle(1, 900, True)``

    :示例说明: 设置编号为 1 的舵机顺时针旋转 90°，等待执行完成

.. function:: servo_ctrl.recenter(servo_id, wait_for_complete=True)

    :描述: 设置舵机回中

    :param uint8 servo_id: 舵机编号，范围为[1:3]
    :param bool wait_for_complete: 是否等待执行完成，默认为 True

    :return: 无

    :示例: ``servo_ctrl.recenter(1, True)``

    :示例说明: 设置编号为 1 的舵机回中，等待执行完成

.. function:: servo_ctrl.set_speed(servo_id, speed)

    :描述: 设置舵机旋转速度

    :param uint8 servo_id: 舵机编号，范围为[1:3]
    :param int32 speed: 旋转速度，精确度为 1 度/秒，正数为顺时针旋转，负数为逆时针旋转

    :return: 无

    :示例: ``servo_ctrl.set_speed(1, 5)``

    :示例说明: 设置编号为 1 的舵机顺时针旋转，旋转速度为 5 度/秒

.. hint:: 模块说明请参考 :doc:`舵机 <../extension_module/servo>`
