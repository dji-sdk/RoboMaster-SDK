===============================
Multi-device Communication
===============================

.. function:: multi_comm_ctrl.set_group(send_group, recv_group_list)

    :description: Sets the group number of the device to ``send_group``, and the device can receive messages from the group numbers registered in ``recv_group_list``. If the ``recv_group_list'' parameter is not used, messages from group 0 will be received by default.

    :param int send_group: The sending group number of the current device. The default group number is 0.
    :param list/tuple recv_group_list: The current list of groups that receive messages, whose type can be list or tuple

    :return: None

    :example: ``multi_comm_ctrl.set_group(1, (1,2,3))``

    :example description: Set the current sending group number to 1 and receive messages from groups 1, 2, and 3. If the receiving group includes the sending group, you will receive the messages you send.

.. function:: multi_comm_ctrl.send_msg(msg, group)

    :description: Send a message via multi-device communication. Sending groups for this message can be set separately.

    :param int msg: The message that needs to be sent
    :param int group: An optional parameter, which specifies the current message sending group number. If you do not specify this parameter, the previously set group number will be used by default.

    :return: None

    :example: ``multi_comm_ctrl.send_msg('RoboMaster EP', 3)``

    :example description: Send the ``'RoboMaster EP'`` message to group 3

.. function:: multi_comm_ctrl.recv_msg(timeout)

    :description: Receive messages (valid when `recv_callback` is not registered). You can set a timeout period.

    :param int timeout: The waiting time, which indicates the waiting time of the receiving function, whose accuracy is 1 second. The default value of this parameter is 72 seconds.

    :return: ``<msg_group>, <msg>``, which is the group number of the message sender and the content of the message

    :example: ``group, recv_msg = multi_comm_ctrl.recv_msg(30)``

    :example description: Receive the message with a waiting time of 30 seconds, where "group" is the group number of the message sender, and "msg" is the content of the received message

.. function:: multi_comm_ctrl.register_recv_callback(callback)

    :description: Registers the callback function for receiving messages. When a message is received, the callback function is run automatically.

    :param function callback: The callback function to be registered. The prototype of the callback function is ``def callback(msg)``, where the type of the ``msg`` parameter is the ``(msg_group, msg)`` tuple.

    :return: None

    :example:
.. code-block:: python
    :linenos:

    #Define a function and register it as a callback function for receiving messages

    def recv_callback(msg):
        pass

    multi_comm_ctrl.register_recv_callback(recv_callback)

.. hint:: For a description of the module, refer to :doc:`Multi-device Communication<./multi_comm_info>`.