===================
智能
===================

.. function:: vision_ctrl.marker_detection_color_set(color_enum)

    :描述: 設置視覺標籤識別顏色

    :param color_enum: 標籤顏色類型，詳細見表格 :data:`color_enum`

    :return: 無

    :示例: ``vision_ctrl.marker_detection_color_set(rm_define.marker_detection_color_red)``

    :示例說明: 設置視覺標籤識別顏色為紅色

.. data:: color_enum

    +--------------------------------------+----+
    |rm_define.marker_detection_color_red  |紅色|
    +--------------------------------------+----+
    |rm_define.marker_detection_color_green|綠色|
    +--------------------------------------+----+
    |rm_define.marker_detection_color_blue |藍色|
    +--------------------------------------+----+