===================
Vision
===================

.. function:: vision_ctrl.marker_detection_color_set(color_enum)

    :description: Sets the color for identifying visual labels

    :param color_enum: For available label colors, refer to the :data:`color_enum` table.

    :return: None

    :example: ``vision_ctrl.marker_detection_color_set(rm_define.marker_detection_color_red)``

    :example description: Set the color for identifying visual labels to red

.. data:: color_enum

    +--------------------------------------+----+
    | rm_define.marker_detection_color_red | Red |
    +--------------------------------------+----+
    | rm_define.marker_detection_color_green | Green |
    +--------------------------------------+----+
    | rm_define.marker_detection_color_blue | Blue |
    +--------------------------------------+----+