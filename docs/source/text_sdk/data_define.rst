====================
Data Description
====================

.. data:: switch_enum

    - ``on``: On
    - ``off``: Off


.. data:: mode_enum

    - ``chassis_lead`` : Gimbal follows chassis mode
    - ``gimbal_lead`` : Chassis follows gimbal mode
    - ``free`` : Free mode

.. data:: chassis_push_attr_enum

    - ``position`` : The chassis position
    - ``attitude`` : The chassis posture
    - ``status`` : The chassis status

.. data:: gimbal_push_attr_enum

    - ``attitude``: The gimbal posture

.. data:: armor_event_attr_enum

    - ``hit`` : The armor hit detected

.. data:: sound_event_attr_enum

    - ``applause`` : Applause

.. data:: led_comp_enum

    - ``all`` : All LED lights
    - ``top_all`` : All LED lights on the gimbal
    - ``top_right`` : Right LED light on the gimbal
    - ``top_left`` : Left LED light on the gimbal

    - ``bottom_all`` : All LED lights on the chassis
    - ``bottom_front`` : Front LED light on the chassis
    - ``bottom_back`` : All rear LED lights
    - ``bottom_left`` : All left LED lights
    - ``bottom_right`` : All right LED lights

.. data:: led_effect_enum

    - ``solid`` : Solid on
    - ``off`` : Off
    - ``pulse`` : Breathing
    - ``blink`` : Flashing
    - ``scrolling`` : Marquee

.. data:: line_color_enum

    - ``red`` : Red
    - ``blue`` : Blue
    - ``green`` : Green

.. data:: marker_color_enum

    - ``red`` : Red
    - ``blue`` : Blue

.. data:: ai_push_attr_enum

    - ``person`` : Pedestrian
    - ``gesture`` : Gesture
    - ``line``: Line
    - ``marker`` : Visual label
    - ``robot`` : Robot

.. data:: ai_pose_id_enum

    - ``4`` : The forward V gesture
    - ``5`` : The reverse V gesture
    - ``6`` : The shooting gesture

.. data:: ai_marker_id_enum

    - ``1`` : Stop
    - ``4`` : Turn left
    - ``5`` : Turn right
    - ``6`` : Move forward
    - ``8`` : Red heart
    - ``10 - 19`` : A number between 0 and 9
    - ``20 - 45`` : A letter between A and Z

.. data:: camera_ev_enum

    - ``default`` : Default
    - ``small`` : Small
    - ``medium`` : Medium
    - ``large`` : Large
