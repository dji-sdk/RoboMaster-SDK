===================
機械爪
===================

.. function:: gripper_ctrl.open()

    :描述: 控制機械爪打開

    :param void: 無

    :return: 無

    :示例: ``gripper_ctrl.open()``

    :示例說明: 控制機械爪打開

.. function:: gripper_ctrl.close()

    :描述: 控制機械爪關閉

    :param void: 無

    :return: 無

    :示例: ``gripper_ctrl.close()``

    :示例說明: 控制機械爪關閉

.. function:: gripper_ctrl.stop()

    :描述: 控制機械爪停止運動

    :param void: 無

    :return: 無

    :示例: ``gripper_ctrl.stop()``

    :示例說明: 控制機械爪停止運動

.. function:: gripper_ctrl.update_power_level(level)

    :描述: 設置機械爪力度檔位

    :param int level: 機械爪的力度檔位，範圍為[1:4]檔，默認為 1

    :return: 無

    :示例: ``gripper_ctrl.update_power_level(1)``

    :示例說明: 設置機械爪力度檔位為 1

.. function:: gripper_ctrl.is_closed()

    :描述: 獲取機械爪夾緊狀態

    :param void: 無

    :return: 機械爪夾緊狀態，若機械爪夾緊則返回 true，否則返回 false
    :rtype: bool

    :示例: ``ret = gripper_ctrl.is_closed()``

    :示例說明: 獲取機械爪夾緊狀態

.. function:: gripper_ctrl.is_open()

    :描述: 獲取機械爪張開狀態

    :param void: 無

    :return: 機械爪張開狀態，若機械爪完全張開則返回 true，否則返回 false
    :rtype: bool

    :示例: ``ret = gripper_ctrl.is_open()``

    :示例說明: 獲取機械爪張開狀態

.. hint:: 模塊說明請參考 :doc:`機械臂與機械爪 <../extension_module/robotic_arm_and_gripper>`