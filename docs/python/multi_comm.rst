===================
多機通訊
===================

.. function:: multi_comm_ctrl.set_group(send_group, recv_group_list)

    :描述: 設定機器的組號為 ``send_group`` ，機器可以接收來自 ``recv_group_list`` 中註冊組號的消息。如果不使用 ``recv_group_list`` 參數，預設接收組號 0 的消息

    :param int send_group: 當前機器的發送組號，預設組號為 0
    :param list/tuple recv_group_list: 當前接收消息的組別清單，類型可以為列表或元組

    :return: 無

    :示例: ``multi_comm_ctrl.set_group(1, (1,2,3))``

    :示例說明: 設定當前發送組號為 1， 接收組號 1,2,3 的消息，若接收組別包含發送組別，則會接收到自己發送的消息

.. function:: multi_comm_ctrl.send_msg(msg, group)

    :描述: 通過多機通訊發送消息，可以單獨設定該消息的發送組號

    :param int msg: 需要發送的消息
    :param int group: 可選參數，指定當前消息發送組號，不指定則預設使用之前設定的組號

    :return: 無

    :示例: ``multi_comm_ctrl.send('RoboMaster EP', 3)``

    :示例說明: 向組號 3 發送消息 ``'RoboMaster EP'``

.. function:: multi_comm_ctrl.recv_msg(timeout)

    :描述: 接收消息（當沒有註冊`recv_callback`時生效），可設定超時時間

    :param int timeout: 等待時間，接收函數等待的時間，精確度為 1 秒，預設為 72 秒

    :return: ``<msg_group>, <msg>`` 消息發送方的組號和消息內容

    :示例: ``group, recv_msg = multi_comm_ctrl.recv_msg(30)``

    :示例說明: 接收消息，等待時間為 30 秒，group 為消息發送方的組號，msg 為收到的消息內容

.. function:: multi_comm_ctrl.register_recv_callback(callback)

    :描述: 註冊接收消息的回呼函數，當接收到消息後，自動執行回呼函數

    :param function callback: 需要註冊的回呼函數, 回呼函數原型為 ``def callback(msg)``，其中 ``msg`` 參數類型為元組 ``(msg_group, msg)``

    :return: 無

    :示例:
.. code-block:: python
    :linenos:

    #定義一個函數，並將其註冊為接收消息的回呼函數

    def recv_callback(msg):
        pass

    multi_comm_ctrl.register_recv_callback(recv_callback)