===================
装甲板
===================

.. py:function:: def ir_hit_detection_event(msg):

    :描述: 当检测到机器人受到红外光束攻击时，运行函数内程序

    :param msg: 函数内部的消息参数

    :return: 无

    :示例:
.. code-block:: python
    :linenos:

    #当检测到机器人受到红外光束攻击时，运行函数内程序

    def ir_hit_detection_event(msg):
        pass

.. function:: armor_ctrl.cond_wait(condition_enum)

    :描述: 等待机器人受到红外光束攻击时，执行下一条指令

    :param condition_enum: 事件类型，``rm_define.cond_ir_hit_detection`` 表示机器人受到红外光束攻击

    :return: 无

    :示例: ``armor_ctrl.cond_wait(rm_define.cond_ir_hit_detection)``

    :示例说明: 等待机器人受到红外光束攻击时，执行下一条指令

.. function:: armor_ctrl.check_condition(condition_enum)

    :描述: 判断机器人是否受到红外光束攻击

    :param condition_enum: 事件类型，``rm_define.cond_ir_hit_detection`` 表示机器人受到红外光束攻击

    :return: 机器人是否受到红外光束攻击，受到攻击时返回真，否则返回假。
    :rtype: bool

    :示例: ``if armor_ctrl.check_condition(rm_define.cond_ir_hit_detection):``

    :示例说明: 如果机器人受到红外光束攻击时，执行下一条指令