===================
传感器转接模块
===================

.. function:: sensor_adapter_ctrl.get_sensor_adapter_adc(board_id, port_num)

    :描述: 获取传感器转接模块相应端口模拟引脚的 ADC 值

    :param int board_id: 传感器转接模块编号，范围为[1:6]
    :param uint8 port_num: 传感器转接模块上的端口号，范围为[1:2]
    :param bool wait_for_complete: 是否等待执行完成，默认为 True

    :return: 传感器转接模块相应端口模拟引脚的 ADC 值，范围为[0:1023]
    :rtype: uint16

    :示例: ``ret = sensor_adapter_ctrl.get_sensor_adapter_adc(1, 2)``

    :示例说明: 获取 1 号传感器转接模块 2 号端口模拟引脚的 ADC 值

.. function:: sensor_adapter_ctrl.get_sensor_adapter_pulse_period(board_id, port_num)

    :描述: 获取传感器转接模块相应端口引脚的脉冲持续时间

    :param int board_id: 传感器转接模块编号，范围为[1:6]
    :param uint8 port_num: 传感器转接模块上的端口号，范围为[1:2]

    :return: 传感器转接模块相应端口引脚的脉冲持续时间，精确度为 1 ms
    :rtype: uint32

    :示例: ``ret = sensor_adapter_ctrl.get_sensor_pulse_period(1, 2)``

    :示例说明: 获取 1 号传感器转接模块 2 号端口引脚脉冲持续时间

.. function:: def sensor_adapter[board_id]_port[port_id]_[judge_type]_event(msg):

    :描述: 当检测到传感器转接模块相应端口引脚跳变为高电平/低电平/双向，运行函数内程序

    :param int board_id: 传感器转接模块编号，范围为[1:6]
    :param uint8 port_num: 传感器转接模块上的端口号，范围为[1:2]
    :param judge_type: 触发条件，可以为 high, low, trigger，分别表示高电平，低电平还是双向跳变

    :return: 无

    :示例:
.. code-block:: python
    :linenos:

    #当检测到 1 号传感器转接模块 2 号端口引脚跳变为高电平时，运行函数内程序

    def sensor_adapter1_port2_high_event(msg):
        pass

.. function:: sensor_adapter_ctrl.cond_wait(rm_define.cond_sensor_adapter[board_id]_port[port_id]_[judge_type]_event)

    :描述: 等待传感器转接模块相应端口引脚脉冲为（高/低/跳变）时，执行下一条指令

    :param int board_id: 传感器转接模块编号，范围为[1:6]
    :param uint8 port_num: 传感器转接模块上的端口号，范围为[1:2]
    :param judge_type: 触发条件，可以为 high, low, trigger，分别表示高电平，低电平还是双向跳变

    :return: 无

    :示例: ``sensor_adapter_ctrl.cond_wait(rm_define.cond_sensor_adapter1_port2_high_event)``

    :示例说明: 等待 1 号传感器转接模块 2 号端口引脚为高电平时，执行下一条指令

.. function:: sensor_adapter_ctrl.check_condition(rm_define.cond_sensor_adapter[board_id]_port[port_id]_[judge_type]_event)

    :描述: 判断传感器转接模块相应端口引脚脉冲是否为（高/低/跳变）

    :param int board_id: 传感器转接模块编号，范围为[1:6]
    :param uint8 port_num: 传感器转接模块上的端口号，范围为[1:2]
    :param judge_type: 触发条件，可以为 high, low, trigger，分别表示高电平，低电平还是双向跳变

    :return: 是否满足条件，满足条件时返回真，否则返回假。
    :rtype: bool

    :示例:
.. code-block:: python
    :linenos:

    #如果 1 号传感器转接模块 2 号端口引脚正在跳变时，执行下一条指令

    if sensor_adapter_ctrl.check_condition(rm_define.cond_sensor_adapter1_port2_trigger_event):
        pass

.. hint:: 模块说明请参考 :doc:`传感器转接模块 <../extension_module/sensor_adapter>`