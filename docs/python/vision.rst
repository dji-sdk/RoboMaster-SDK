===================
Smart
===================

.. function:: vision_ctrl.marker_detection_color_set(color_enum)

    :Description: Set the visual tag recognition color

    :param color_enum: A tag color type. For details, see table :data:`color_enum`

    :return: None

    :Example: ``vision_ctrl.marker_detection_color_set(rm_define.marker_detection_color_red)``

    :Example description: Set the visual tag recognition color to red

.. data:: color_enum

    +--------------------------------------+-----+
    |rm_define.marker_detection_color_red  |Red  |
    +--------------------------------------+-----+
    |rm_define.marker_detection_color_green|Green|
    +--------------------------------------+-----+
    |rm_define.marker_detection_color_blue |Blue |
    +--------------------------------------+-----+
