===================
裝甲板
===================

.. py:function:: def ir_hit_detection_event(msg):

    :描述：當檢測到機器人受到紅外光束攻擊時，運行函數內程式

    :param msg: 函數內部的消息參數

    :return: 無

    :示例:
.. code-block:: python
    :linenos:

    #當檢測到機器人受到紅外光束攻擊時，運行函數內程式

    def ir_hit_detection_event(msg):
        pass

.. function:: armor_ctrl.cond_wait(condition_enum)

    :描述：等待機器人受到紅外光束攻擊時，執行下一條指令

    :param condition_enum: 事件類型，``rm_define.cond_ir_hit_detection`` 表示機器人受到紅外光束攻擊

    :return: 無

    :示例: ``armor_ctrl.cond_wait(rm_define.cond_ir_hit_detection)``

    :示例說明: 等待機器人受到紅外光束攻擊時，執行下一條指令

.. function:: armor_ctrl.check_condition(condition_enum)

    :描述: 判斷機器人是否受到紅外光束攻擊

    :param condition_enum: 事件類型，``rm_define.cond_ir_hit_detection`` 表示機器人受到紅外光束攻擊

    :return: 機器人是否受到紅外光束攻擊，受到攻擊時返回真，否則返回假。
    :rtype: bool

    :示例: ``if armor_ctrl.check_condition(rm_define.cond_ir_hit_detection):``

    :示例說明: 如果機器人受到紅外光束攻擊，執行下一條指令