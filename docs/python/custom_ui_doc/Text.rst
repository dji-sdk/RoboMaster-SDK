=================
Text
=================

Text 控制項用於顯示文本

.. function:: text_object.set_text(string, [color_r, color_g, color_b, color_a] , align, size)

    :描述: 設定控制項的文字屬性

    :param string string: 需要顯示的字串內容
    :param list [color_r, color_g, color_b, color_a]: 可選參數，需要顯示的字串的顏色，參數分別為顯示顏色 r 值、b 值、g 值，透明度，取值範圍都為 [0, 255]
    :param enum align: 可選參數，枚舉類型，需要顯示文字的對齊方式，詳情見表格 :data:`align`
    :param int size: 顯示文字的字型大小

    :return: 無

    :示例: ``my_Text.set_text(120, 120, 120, 200, text_anchor.upper_left, 12)``

    :示例說明: 設定文字顏色的 rgb 值為（120, 120, 120），透明度為 200，字體對齊方式為頂端左對齊，字型大小為 12 號

.. function:: text_object.set_text_color(r, g, b, a)

    :描述: 設定控制項的文字顏色

    :param int r: 文字顏色的 r 值，範圍為 [0, 255]
    :param int g: 文字顏色的 g 值，範圍為 [0, 255]
    :param int b: 文字顏色的 b 值，範圍為 [0, 255]
    :param int a: 文字顏色的透明度，範圍為 [0, 255] 

    :return: 無

    :示例: ``my_Text.set_text_color(120, 120, 120, 200)``

    :示例說明: 設定文字的 rgb 值為（120, 120, 120），透明度為 200

.. function:: text_object.set_text_align(align)

    :描述: 設定文字的對齊方式

    :param enum align: 可選參數，枚舉類型，需要顯示文字的對齊方式，詳細見表格 :data:`align`

    :return: 無

    :示例: ``my_Text.set_text_align(text_anchor.upper_left)``

    :示例說明: 設定文字的對齊方式為頂端左對齊

.. function:: text_object.set_text_size(size)

    :描述: 設定文字的字型大小

    :param int size: 文字的字型大小值

    :return: 無

    :示例: ``my_Text.set_text_size(12)``

    :示例說明: 設定文字的字型大小為 12 號

.. function:: text_object.set_border_active(active)

    :描述: 是否顯示文字邊框

    :param bool active: 是否顯示文字邊框，True 表示顯示邊框，False 表示不顯示邊框

    :return: 無

    :示例: ``my_Text.set_border_active(True)``

    :示例說明: 顯示文字邊框

.. function:: text_object.set_background_color(r, g, b, a)

    :描述: 設定控制項的背景色 

    :param int r: 背景顏色的 r 值，範圍為 [0, 255]
    :param int g: 背景顏色的 g 值，範圍為 [0, 255]
    :param int b: 背景顏色的 b 值，範圍為 [0, 255]
    :param int a: 背景顏色的透明度，範圍為 [0, 255]

    :return: 無

    :示例: ``my_Text.set_background_color(200, 200, 200, 230)``

    :示例說明: 設定背景色的 rgb 值為 (200, 200, 200)，透明度為 230

.. function:: text_object.set_background_active(active)

    :描述: 是否顯示文字背景

    :param bool active: 是否顯示背景，True 表示显示顯示景，False 表示不顯示背景

    :return: 无

    :示例: ``my_Text.set_background_active(True)``

    :示例說明: 顯示文字背景

.. function:: text_object.append_text(content)

    :描述: 向 Text 控制項中增加文本

    :param string content: 需要向 Text 中增加的文本

    :return: 無

    :示例: ``my_Text.append_text('RoboMaster EP')``

    :示例說明: 向 Text 中增加的文字 ``RoboMaster EP``

.. data:: align

        +-------------------------+------------+
        |text_anchor.upper_left   |頂端左對齊  |
        +-------------------------+------------+
        |text_anchor.upper_center |頂端居中對齊|
        +-------------------------+------------+
        |text_anchor.upper_right  |頂端右對齊  |
        +-------------------------+------------+
        |text_anchor.middle_left  |中間左對齊  |
        +-------------------------+------------+
        |text_anchor.middle_center|中間居中對齊|
        +-------------------------+------------+
        |text_anchor.middle_right |中間右對其  |
        +-------------------------+------------+
        |text_anchor.lower_left   |底端左對齊  |
        +-------------------------+------------+
        |text_anchor.lower_center |底端居中對齊|
        +-------------------------+------------+
        |text_anchor.lower_right  |底端右對齊  |
        +-------------------------+------------+