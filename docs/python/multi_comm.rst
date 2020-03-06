============================
Multi-Machine Communication
============================

.. function:: multi_comm_ctrl.set_group(send_group, recv_group_list)

    :Description: Set the group number of the machine to ``send_group``. The machine can receive messages from the group numbers registered in ``recv_group_list``. If the parameter ``recv_group_list`` is not used, messages from group number 0 are received by default

    :param int send_group: The sending group number of the current machine. The default group number is 0
    :param list/tuple recv_group_list: The list of groups currently receiving messages. The type can be list or tuple

    :return: None

    :Example: ``multi_comm_ctrl.set_group(1, (1,2,3))``

    :Example description: Set the current sending group number to 1 and the receiving group numbers as 1, 2, and 3. If the receiving group includes the sending group, it will receive messages sent by itself

.. function:: multi_comm_ctrl.send_msg(msg, group)

    :Description: By sending a message through multi-machine communication, you can individually set the group to which the message is sent

    :param int msg: Message to be sent
    :param int group: An optional parameter. It specifies the group to which the current message is sent. If not specified, the previously set group number will be used by default

    :return: None

    :Example: ``multi_comm_ctrl.send('RoboMaster EP', 3)``

    :Example description: Send the message ``'RoboMaster EP'`` to group number 3

.. function:: multi_comm_ctrl.recv_msg(timeout)

    :Description: Set a timeout when receiving messages (effective when `recv_callback` is not registered)

    :param int timeout: Waiting time, i.e. the time that the receiving function has waited, with an accuracy of 1 second. The default setting is 72 seconds

    :return: ``<msg_group>, <msg>`` The group number of the message sender and the message content

    :Example: ``group, recv_msg = multi_comm_ctrl.recv_msg(30)``

    :Example description: When receiving messages, the waiting time is 30 seconds; group is the group number of the sender, and msg is the content of the received message

.. function:: multi_comm_ctrl.register_recv_callback(callback)

    :Description: Register the callback function used to receive messages. When the message is received, the callback function is executed automatically

    :param function callback: The callback function to be registered. The prototype of the callback function is ``def callback(msg)``, where the ``msg`` parameter type is the tuple ``(msg_group, msg)``

    :return: None

    :Example:
.. code-block:: python
    :linenos:

    #Define a function and register it as the callback function used to receive messages

    def recv_callback(msg):
        pass

    multi_comm_ctrl.register_recv_callback(recv_callback)
