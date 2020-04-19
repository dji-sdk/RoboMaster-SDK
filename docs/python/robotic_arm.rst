===================
机械臂
===================

.. function:: robotic_arm_ctrl.move(x, y, wait_for_complete=True)

    :描述: 设置机械臂运动的相对位置

    :param int32 x: 设置机械臂水平运动的距离，正数为向前运动，负数为向后运动，精确度为 1 mm
    :param int32 y: 设置机械臂垂直运动的距离，正数为向上运动，负数为向下运动，精确度为 1 mm
    :param bool wait_for_complete: 是否等待执行完成，默认为 True

    :return: 无

    :示例: ``robotic_arm_ctrl.move(40, 50, True)``

    :示例说明: 设置机械臂向前移动 20 mm，向上移动 30 mm，等待执行完成

.. function:: robotic_arm_ctrl.moveto(x, y, wait_for_complete=True)

    :描述: 设置机械臂运动到绝对坐标

    :param int32 x: 设置机械臂水平运动的坐标值，精确度为 1 mm
    :param int32 y: 设置机械臂垂直运动的坐标值，精确度为 1 mm
    :param bool wait_for_complete: 是否等待执行完成，默认为 True

    :return: 无

    :示例: ``robotic_arm_ctrl.moveto(40, 50, True)``

    :示例说明: 设置机械臂移动到（x=40mm，y=50mm）的绝对坐标，等待执行完成

.. function:: robotic_arm_ctrl.get_position()

    :描述: 获取机械臂位置

    :param void: 无

    :return: 机械臂的绝对坐标，精确度为 1 mm
    :rtype: 列表[x, y], x 和 y 为 int32 类型

    :示例: ``[x, y] = robotic_arm_ctrl.get_position()``

    :示例说明: 获取机械臂的绝对坐标

.. function:: robotic_arm_ctrl.recenter()

    :描述: 设置机械臂回中

    :param void: 无

    :return: 无

    :示例: ``robotic_arm_ctrl.recenter()``

    :示例说明: 设置机械臂回中

.. hint:: 模块说明请参考 :doc:`机械臂与机械爪 <../extension_module/robotic_arm_and_gripper>`