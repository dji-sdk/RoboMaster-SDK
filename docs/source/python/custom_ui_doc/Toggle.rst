=================
Toggle
=================

Toggle 控件用於在屏幕上繪製一個開關，通過控制開關的開啟與閉合來執行一些具體的操作。

.. function:: toggle_object.set_text(string, [color_r, color_g, color_b, color_a] , align, size)

    :描述: 設置控件的顯示文字 

    :param string string: 控件上顯示的字符串內容
    :param list [color_r, color_g, color_b, color_a]: 可選參數，需要顯示的字符串的顏色，參數分別為顯示顏色 r 值、b 值、g 值、透明度，取值範圍都為 [0, 255]
    :param enum align: 可選參數，枚舉類型，需要顯示文字的對齊方式，詳細見表格 :data:`align`
    :param int size: 顯示文字的字號大小

    :return: 無

    :示例: ``my_Toggle.set_text(120, 120, 120, 200, text_anchor.upper_left, 12)``

    :示例說明: 設置文字的 rgb 值為（120, 120, 120），透明度為 200，字體對齊方式為頂端左對齊，字號大小為 12 號

.. function:: toggle_object.set_text_color(r, g, b, a)

    :描述: 設置文字的顏色 

    :param int r: 文字顏色的 r 值，範圍為 [0, 255]
    :param int g: 文字顏色的 g 值，範圍為 [0, 255]
    :param int b: 文字顏色的 b 值，範圍為 [0, 255]
    :param int a: 文字顏色的透明度，範圍為 [0, 255]

    :return: 無

    :示例: ``my_Toggle.set_text_color(120, 120, 120, 200)``

    :示例說明: 設置字體的 rgb 值為（120, 120, 120），透明度為 200

.. function:: toggle_object.set_text_align(align)

    :描述: 設置文字的對齊方式 

    :param enum align: 可選參數，枚舉類型，需要顯示文字的對齊方式，詳細見表格 :data:`align`

    :return: 無

    :示例: ``my_Toggle.set_text_align(text_anchor.upper_left)``

    :示例說明: 設置字體的對齊方式為頂端左對齊

.. function:: toggle_object.set_text_size(size)

    :描述: 設置文字的字號大小

    :param int size: 文字的字號值

    :return: 無

    :示例: ``my_Toggle.set_text_size(12)``

    :示例說明: 設置文字的字號為 12 號

.. function:: toggle_object.set_background_color(r, g, b, a)

    :描述: 設置控件的背景色 

    :param int r: 背景顏色的 r 值，範圍為 [0, 255]
    :param int g: 背景顏色的 g 值，範圍為 [0, 255]
    :param int b: 背景顏色的 b 值，範圍為 [0, 255]
    :param int a: 背景顏色的透明度，[0, 255]

    :return: 無

    :示例: ``my_Toggle.set_background_color(200, 200, 200, 230)``

    :示例說明: 設置背景色的 rgb 值為 (200, 200, 200)，透明度為 230

.. function:: toggle_object.set_checkmark_color(r, g, b, a)

    :描述: 設置控件選中圖標的顏色 

    :param int r: 圖標顏色的 r 值，範圍為 [0, 255]
    :param int g: 圖標顏色的 g 值，範圍為 [0, 255]
    :param int b: 圖標顏色的 b 值，範圍為 [0, 255]
    :param int a: 圖標顏色的透明度，範圍為 [0, 255]

    :return: 無

    :示例: ``my_Toggle.set_checkmark_color(200, 200, 200, 230)``

    :示例說明: 設置選中圖標的 rgb 值為 (200, 200, 200)，透明度為 230

.. function:: toggle_object.set_is_on(status)

    :描述: 設置控件的狀態

    :param bool status: 設置控件是否為打開狀態，True 表示打開，False 表示關閉

    :return: 無

    :示例: ``my_Toggle.set_is_on(True)``

    :示例說明: 設置 Toggle 控件為打開狀態