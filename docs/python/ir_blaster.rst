===================
發射器
===================

.. function:: ir_blaster_ctrl.set_fire_count(count)

    :描述: 設定紅外光束的發射頻率，即每秒射出的紅外光束次數

    :param int color_enum: 發射頻率，即每秒射出的紅外光束次數，範圍為[1:8]

    :return: 無

    :示例: ``ir_blaster_ctrl.set_fire_count(4)``

    :示例說明: 設定紅外光束的發射頻率為 4

.. function:: ir_blaster_ctrl.fire_once()

    :描述: 控制發射器只發射一次紅外光束

    :param void: 無

    :return: 無

    :示例: ``ir_blaster_ctrl.fire_once()``

    :示例說明: 控制發射器只發射一次紅外光束

.. function:: ir_blaster_ctrl.fire_continuous()

    :描述: 控制發射器持續發射紅外光束

    :param void: 無

    :return: 無

    :示例: ``ir_blaster_ctrl.fire_continuous()``

    :示例說明: 控制發射器持續發射紅外光束

.. function:: ir_blaster_ctrl.stop()

    :描述: 停止發射紅外光束

    :param void: 無

    :return: 無

    :示例: ``ir_blaster_ctrl.stop()``

    :示例說明: 停止發射紅外光束