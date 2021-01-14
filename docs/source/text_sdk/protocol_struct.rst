================
Protocol Format
================

*****************
Control commands
*****************

IN：**<obj> <command> <params> [<seq>]**;

    - Description
        - The format of the control command protocol, which is generally used to interact with the robot for control purposes.
        - The ending character is ``;``.
    - Parameters
        - *obj* (str): The control object string
        - *command* (str): The control command string
        - *params* (str): The command parameter string, which is generally in the format of **<key> <value>**
        - *seq* (str): The command sequence number string, which is generally in the format of **seq <seq_value>**. This parameter is optional.

OUT：**<result> [<seq>];**

    - Description
        - The format of the control command response protocol, which is generally used to confirm the execution results of control commands.
        - Unless otherwise stated, all control commands have responses.
        - The ending character is ``;``.
    - Parameters
        - *result* (exec_result_enum): The execution result string
        - *seq* (str): The execution result sequence number string, which is generally in the format of **seq <seq_value>**

.. note:: <seq>

    The <seq> parameter is used to identify the uniqueness of the current message. When the control command contains the *<seq>* parameter, the response result of the command contains the corresponding sequence number.

*****************
Message push
*****************

OUT: **<obj> push <attr> <value>;**

    - Description
        - The format of the message push protocol. You can receive messages after enabling message push through a control command.
        - Message push runs at a fixed frequency, which is set when the message push is enabled.
        - The ending character is ``;``.
    - Parameters
        - *obj* (str): The push object
        - *attr* (str): The push data attribute
        - *value* (str): The push data value

*****************
Event reporting
*****************

OUT: **<obj> event <attr> <value>;**

    - Description
        - The format of the event reporting protocol. You can receive reporting after enabling an event reporting switch through a control command.
        - The ending character is ``;``.
    - Parameters
        - *obj* (str): The object of the event
        - *attr* (str): The event data attribute
        - *value (str)*: The event data value

.. note:: The trigger mechanism

    After the corresponding *event reporting* function is enabled, event reporting will be triggered when an event occurs.

*****************
IP broadcasting
*****************

OUT: **robot ip <addr>;**

    - Parameters
        - *addr* (str): The IPv4 address of the robot in the current connection method

.. note:: The broadcasting lifecycle

    In *Wi-Fi networking* mode, the robot continuously broadcasts its own IPv4 address through the corresponding port, and you can connect to the robot through this IP address. When a connection is established, the broadcast stops.

*****************
The video stream
*****************

OUT: H.264-encoded real-time video stream data with a resolution of 1280×720 and a refresh rate of 30 fps. The video stream data must be correctly decoded to display the video picture in real time.

*****************
The audio stream
*****************

OUT: Opus-encoded real-time audio stream data with a sampling rate of 48,000 bps, a frame size of 960 bit, and a single channel. The audio stream data must be correctly decoded to play audio in real time.

.. tip:: Decoder

    For the sample code for decoding video and audio streams on the receiving end, refer to `Stream Decoder <https://github.com/dji-sdk/RoboMaster-SDK/tree/master/sample_code/RoboMasterEP/stream/>`_.


.. note:: IN/OUT

    In this document, the **IN** or **OUT** prefix in the control commands has no practical meaning. Instead, it only identifies the data flow direction of the current command from the perspective of the robot.

    IN: indicates that the current data is sent from an external device to the robot.
    
    OUT: indicates that the current data is sent from the robot to an external device.

    During actual use, ignore this identifier and simply send and receive actual control commands.