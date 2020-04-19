===================
多机通信
===================

.. function:: multi_comm_ctrl.set_group(send_group, recv_group_list)

    :描述: 设置机器的组号为 ``send_group`` ，机器可以接收来自 ``recv_group_list`` 中注册的组号的消息。如果不使用 ``recv_group_list`` 参数，默认接收组号 0 的消息

    :param int send_group: 当前机器的发送组号，默认组号为 0
    :param list/tuple recv_group_list: 当前接收消息的组别列表，类型可以为列表或元组

    :return: 无

    :示例: ``multi_comm_ctrl.set_group(1, (1,2,3))``

    :示例说明: 设置当前发送组号为 1， 接收组号 1,2,3 的消息，若接收组别包含发送组别，则会接收到自己发送的消息

.. function:: multi_comm_ctrl.send_msg(msg, group)

    :描述: 通过多机通信发送消息，可以单独设置该消息的发送组号

    :param int msg: 需要发送的消息
    :param int group: 可选参数，指定当前消息发送组号，不指定则默认使用之前设置的组号

    :return: 无

    :示例: ``multi_comm_ctrl.send_msg('RoboMaster EP', 3)``

    :示例说明: 向组号 3 发送消息 ``'RoboMaster EP'``

.. function:: multi_comm_ctrl.recv_msg(timeout)

    :描述: 接收消息（当没有注册`recv_callback`时生效），可设置超时时间

    :param int timeout: 等待时间，接收函数等待的时间，精确度为 1 秒，默认为 72 秒

    :return: ``<msg_group>, <msg>`` 消息发送方的组号和消息内容

    :示例: ``group, recv_msg = multi_comm_ctrl.recv_msg(30)``

    :示例说明: 接收消息，等待时间为 30 秒，group 为信息发送方的组号，msg 为收到的消息内容

.. function:: multi_comm_ctrl.register_recv_callback(callback)

    :描述: 注册接收消息的回调函数，当接收到信息后，自动执行回调函数

    :param function callback: 需要注册的回调函数, 回调函数原型为 ``def callback(msg)``，其中 ``msg`` 参数类型为元组 ``(msg_group, msg)``

    :return: 无

    :示例:
.. code-block:: python
    :linenos:

    #定义一个函数，并将其注册为接收消息的回调函数

    def recv_callback(msg):
        pass

    multi_comm_ctrl.register_recv_callback(recv_callback)

.. hint:: 模块说明请参考 :doc:`多机通信 <./multi_comm_info>`