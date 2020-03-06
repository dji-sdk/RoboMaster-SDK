================
Protocol Format
================

*****************
Control command
*****************

IN：**<obj> <command> <params> [<seq>]**

    - Description
        - Control command protocol format. It is generally used to interact with the robot in control
    - Parameters
        - *obj* (str): Control object string
        - *command* (str): Control command string
        - *params* (str): Command parameter string, generally in the form of **<key> <value>**
        - *seq* (str): Command sequence number string, usually in the form of **seq <seq_value>**. An optional parameter

OUT：**<result> [<seq>]**

    - Description
        - The protocol format of the control command response result. It is generally used to confirm the execution result of the control command
        - Unless specifically instructed, all control commands have response results
    - Parameters
        - *result* (exec_result_enum): Execution result string
        - *seq* (str): Execution result sequence number string, usually in the form of **seq <seq_value>**

.. note:: <seq>

    <seq> can be used to identify the uniqueness of the current message. When the control command has the *<seq>* parameter, the response result of the corresponding command contains the corresponding sequence number

*****************
Message push
*****************

OUT: **<obj> push <attr> <value>**

    - Description
        - Message push protocol format. Messages can be received after the message push is enabled via a control command
        - The message push will push messages at a fixed frequency, which depends on the frequency setting while enabling the current message push
    - Parameters
        - *obj* (str): Push object
        - *attr* (str): Push data properties
        - *value* (str): Push data value

*****************
Event reporting
*****************

OUT: **<obj> event <attr> <value>**

    - Description
        - Event reporting protocol format. Reports can be received after an event reporting is switched on through a control command
    - Parameters
        - *obj* (str): The object of the event
        - *attr* (str): Event data properties
        - *value (str)* Event data value

.. note:: Trigger mechanism

    When the *event reporting* function is enabled successfully, an event will be reported if one occurs

*****************
IP broadcasting
*****************

OUT: **robot ip <addr>**

    - Parameters
        - *addr* (str): The IPv4 address of the robot in the current connection mode

.. note:: Broadcast life cycle

    While in *Wi-Fi networking* mode, the robot will continuously broadcast its IPv4 address to corresponding ports. You can connect to the robot through this IP address. When the connection is successful, the broadcast will stop

*****************
Video streaming
*****************

OUT: H.264 encoded real-time video streaming data. Decoding the video streaming data correctly is required in order to display video images in real time.

*****************
Audio streaming
*****************

OUT: Opus encoded real-time audio streaming data. Decoding the audio streaming data correctly is required in order to play the audio in real time.

.. note:: IN/OUT

    In this document, the prefix **IN** or **OUT** has no practical significance in control commands. It is only to identify the direction of data flow of the current command when the robot is the main body:

    IN：Identifies that the current data is sent from an external device to the robot
    
    OUT：Identifies that the current data is sent from the robot to an external device

    In actual practice, please ignore the IN and OUT identifiers. Sending and receiving the actual control commands is enough
