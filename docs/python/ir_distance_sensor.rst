===================
红外深度传感器
===================

.. function:: ir_distance_sensor_ctrl.enable_measure(port_id)

    :描述: 开启红外深度传感器测距功能

    :param int port_id: 红外深度传感器模块编号，范围为[1:4]

    :return: 无

    :示例: ``ir_distance_sensor_ctrl.enable_measure(1)``

    :示例说明: 开启 1 号红外深度传感器测距功能

.. function:: ir_distance_sensor_ctrl.disable_measure(port_id)

    :描述: 关闭红外深度传感器测距功能

    :param int port_id: 红外深度传感器模块编号，范围为[1:4]

    :return: 无

    :示例: ``ir_distance_sensor_ctrl.disable_measure(1)``

    :示例说明: 关闭 1 号红外深度传感器测距功能

.. function:: ir_distance_sensor_ctrl.get_distance_info(port_id)

    :描述: 获取红外深度传感器测距信息

    :param int port_id: 红外深度传感器模块编号，范围为[1:4]

    :return: 红外深度传感器前方障碍物的距离，精确度为 1 cm
    :rtype: uint16

    :示例: ``ir_distance_sensor_ctrl.get_distance_info(1)``

    :示例说明: 获取 1 号红外深度传感器测距信息

.. function:: def ir_distance_[port_id]_[compare_type]_[dist]_event(msg):

    :描述: 当检测到红外深度传感器模块前方障碍物距离满足条件时，运行函数内程序

    :param int port_id: 红外深度传感器模块编号，范围为[1:4]
    :param compare_type: 比较类型，可以为 eq, ge, gt, le, lt, 分别表示等于，大于等于，大于，小于等于，小于
    :param dist: 用于比较的距离，精确度为 1 cm，范围为 5~500 cm，误差率为 5%

    :return: 无

    :示例:
.. code-block:: python
    :linenos:

    #当检测到 1 号红外深度传感器前方障碍物距离小于 10 cm 时，运行函数内程序

    def ir_distance_1_lt_10_event(msg):
        pass

.. function:: ir_distance_sensor_ctrl.cond_wait('ir_distance_[port_id]_[compare_type]_[dist]')

    :描述: 等待红外深度传感器模块前方障碍物距离满足条件时，执行下一条指令

    :param 'ir_distance_[port_id]_[compare_type]_[dist]': 用于距离比较的字符串，含模块编号，比较类型和距离
    :param int port_id: 红外深度传感器模块编号，范围为[1:4]
    :param compare_type: 比较类型，可以为 eq, ge, gt, le, lt, 分别表示等于，大于等于，大于，小于等于，小于
    :param dist: 用于比较的距离，精确度为 1 cm，范围为 5~500 cm，误差率为 5%

    :return: 无

    :示例: ``ir_distance_sensor_ctrl.cond_wait('ir_distance_1_gt_50')``

    :示例说明: 等待 1 号红外深度传感器模块前方障碍物距离大于 50 cm 时，执行下一条指令

.. function:: ir_distance_sensor_ctrl.check_condition('ir_distance_[port_id]_[compare_type]_[dist]')

    :描述: 判断红外深度传感器模块前方障碍物距离是否满足条件

    :param 'ir_distance_[port_id]_[compare_type]_[dist]': 用于距离比较的字符串，含模块编号，比较类型和距离
    :param int port_id: 红外深度传感器模块编号，范围为[1:4]
    :param compare_type: 比较类型，可以为 eq, ge, gt, le, lt, 分别表示等于，大于等于，大于，小于等于，小于
    :param dist: 用于比较的距离，精确度为 1 cm，范围为 5~500 cm，误差率为 5%

    :return: 是否满足条件，满足条件时返回真，否则返回假。
    :rtype: bool

    :示例:
.. code-block:: python
    :linenos:

    #当检测到 1 号红外深度传感器前方障碍物距离小于 10 cm 时，运行函数内程序

    if ir_distance_sensor_ctrl.check_condition('ir_distance_1_gt_50'):
        pass

.. hint:: 模块说明请参考 :doc:`红外深度传感器 <../extension_module/ir_distance_sensor>`