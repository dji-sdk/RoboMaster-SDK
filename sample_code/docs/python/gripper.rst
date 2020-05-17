===================
机械爪
===================

.. function:: gripper_ctrl.open()

    :描述: 控制机械爪打开

    :param void: 无

    :return: 无

    :示例: ``gripper_ctrl.open()``

    :示例说明: 控制机械爪打开

.. function:: gripper_ctrl.close()

    :描述: 控制机械爪关闭

    :param void: 无

    :return: 无

    :示例: ``gripper_ctrl.close()``

    :示例说明: 控制机械爪关闭

.. function:: gripper_ctrl.stop()

    :描述: 控制机械爪停止运动

    :param void: 无

    :return: 无

    :示例: ``gripper_ctrl.stop()``

    :示例说明: 控制机械爪停止运动

.. function:: gripper_ctrl.update_power_level(level)

    :描述: 设置机械爪力度档位

    :param int level: 机械爪的力度档位，范围为[1:4]档，默认为 1

    :return: 无

    :示例: ``gripper_ctrl.update_power_level(1)``

    :示例说明: 设置机械爪力度档位为 1

.. function:: gripper_ctrl.is_closed()

    :描述: 获取机械爪夹紧状态

    :param void: 无

    :return: 机械爪夹紧状态，若机械爪夹紧则返回 true，否则返回 false
    :rtype: bool

    :示例: ``ret = gripper_ctrl.is_closed()``

    :示例说明: 获取机械爪夹紧状态

.. function:: gripper_ctrl.is_open()

    :描述: 获取机械爪张开状态

    :param void: 无

    :return: 机械爪张开状态，若机械爪完全张开则返回 true，否则返回 false
    :rtype: bool

    :示例: ``ret = gripper_ctrl.is_open()``

    :示例说明: 获取机械爪张开状态

.. hint:: 模块说明请参考 :doc:`机械臂与机械爪 <../extension_module/robotic_arm_and_gripper>`