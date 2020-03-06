===================
智能
===================

.. function:: vision_ctrl.marker_detection_color_set(color_enum)

    :描述: 设置视觉标签识别颜色

    :param color_enum: 标签颜色类型，详细见表格 :data:`color_enum`

    :return: 无

    :示例: ``vision_ctrl.marker_detection_color_set(rm_define.marker_detection_color_red)``

    :示例说明: 设置视觉标签识别颜色为红色

.. data:: color_enum

    +--------------------------------------+----+
    |rm_define.marker_detection_color_red  |红色|
    +--------------------------------------+----+
    |rm_define.marker_detection_color_green|绿色|
    +--------------------------------------+----+
    |rm_define.marker_detection_color_blue |蓝色|
    +--------------------------------------+----+