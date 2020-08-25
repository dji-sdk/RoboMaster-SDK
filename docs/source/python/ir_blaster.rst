===================
发射器
===================

.. function:: ir_blaster_ctrl.set_fire_count(count)

    :描述: 设置红外光束的发射频率，即每秒射出的红外光束次数

    :param int color_enum: 发射频率，即每秒射出的红外光束次数，范围为[1:8]

    :return: 无

    :示例: ``ir_blaster_ctrl.set_fire_count(4)``

    :示例说明: 设置红外光束的发射频率为 4

.. function:: ir_blaster_ctrl.fire_once()

    :描述: 控制发射器只发射一次红外光束

    :param void: 无

    :return: 无

    :示例: ``ir_blaster_ctrl.fire_once()``

    :示例说明: 控制发射器只发射一次红外光束

.. function:: ir_blaster_ctrl.fire_continuous()

    :描述: 控制发射器持续发射红外光束

    :param void: 无

    :return: 无

    :示例: ``ir_blaster_ctrl.fire_continuous()``

    :示例说明: 控制发射器持续发射红外光束

.. function:: ir_blaster_ctrl.stop()

    :描述: 停止发射红外光束

    :param void: 无

    :return: 无

    :示例: ``ir_blaster_ctrl.stop()``

    :示例说明: 停止发射红外光束