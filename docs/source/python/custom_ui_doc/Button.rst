=================
Button
=================

Button 控件用於響應來自用戶的點擊來啟動或確認操作。

.. function:: button_object.set_text(content, [color_r, color_g, color_b, color_a], align, size)

    :描述: 設置按鈕對象的文字屬性

    :param string content: 按鈕上顯示的字符串內容
    :param list [color_r, color_g, color_b, color_a]: 可選參數，需要顯示的字符串的顏色，參數分別為顯示顏色 r 值、b 值，g 值，透明度，取值範圍都為 [0, 255]
    :param enum align: 可選參數，枚舉類型，需要顯示文字的對齊方式，詳細見表格 :data:`align`
    :param int size: 顯示文字的字號大小

    :return: 無

    :示例: ``my_Button.set_text(120, 120, 120, 255, text_anchor.upper_left, 12)``

    :示例說明: 設置文字顏色的 rgb 值為（120, 120, 120），透明度為 255，文字對齊方式為頂端左對齊，字號大小為 12 號

.. function:: button_object.set_text_color(r, g, b, a)

    :描述: 設置文字的顏色 

    :param int r: 文字顏色的 r 值，範圍為 [0, 255]
    :param int g: 文字顏色的 g 值，範圍為 [0, 255]
    :param int b: 文字顏色的 b 值，範圍為 [0, 255]
    :param int a: 文字顏色的透明度，範圍為 [0, 255]

    :return: 無

    :示例: ``my_button.set_text_color(120, 120, 120, 200)``

    :示例說明: 設置文字顏色的 rgb 值為（120, 120, 120），透明度為 200

.. function:: button_object.set_text_align(align)

    :描述: 設置文字的對齊方式 

    :param enum align: 可選參數，枚舉類型，需要顯示文字的對齊方式，詳見表格 :data:`align`

    :return: 無

    :示例: ``my_button.set_text_align(text_anchor.upper_left)``

    :示例說明: 設置文字的對齊方式為頂端左對齊

.. function:: button_object.set_text_size(size)

    :描述: 設置文字的字號大小

    :param int size: 文字的字號值

    :return: 無

    :示例: ``my_button.set_text_size(12)``

    :示例說明: 設置文字的字號為 12 號

.. function:: button_object.set_background_color(r, g, b, a)

    :描述: 設置按鈕的背景色 

    :param int r: 字體顏色的 r 值，範圍為 [0, 255]
    :param int g: 字體顏色的 g 值，範圍為 [0, 255]
    :param int b: 字體顏色的 b 值，範圍為 [0, 255]
    :param int a: 字體顏色的透明度，範圍為 [0, 255]

    :return: 無

    :示例: ``my_button.set_background_color(200, 200, 200, 230)``

    :示例說明: 設置背景色的 rgb 值為 (200, 200, 200)，透明度為 230