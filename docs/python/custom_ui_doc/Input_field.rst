=================
InputField
=================

InputField 控制項用於接收使用者輸入的文本資訊

.. function:: inputfield_object.set_text(string, [color_r, color_g, color_b, color_a] , align, size)

    :描述: 設定輸入框物件中的文字屬性

    :param string string: 需要顯示的字符串內容
    :param list [color_r, color_g, color_b, color_a]: 可選參數，需要顯示的字符串的顏色，參數分別為顯示顏色 r 值、b 值，g 值，透明度，取值範圍都為 [0, 255]
    :param enum align: 可選參數，枚舉類型，需要顯示文字的對齊方式，詳細見表格 :data:`align`
    :param int size: 顯示文字的字型大小

    :return: 無

    :示例: ``my_InputField.set_text(120, 120, 120, 200, text_anchor.upper_left, 12)``

    :示例說明: 設定字體的 rgb 值為（120, 120, 120），透明度為 200 ，字體對齊方式為頂端左對齊，字型大小為 12 號

.. function:: input_field_object.set_text_color(r, g, b, a)

    :描述: 設定文字的顏色 

    :param int r: 文字顏色的 r 值，範圍為[0, 255]
    :param int g: 文字顏色的 g 值，範圍為[0, 255]
    :param int b: 文字顏色的 b 值，範圍為[0, 255]
    :param int a: 文字顏色的透明度， 範圍為[0, 255]

    :return: 無

    :示例: ``my_button.set_text_color(120, 120, 120, 200)``

    :示例說明: 設定字體的 rgb 值為（120, 120, 120），透明度為 200

.. function:: input_field_object.set_text_align(align)

    :描述: 設定控制項中文字的對齊方式 

    :param enum align: 可選參數，枚舉類型，需要顯示文字的對齊方式，詳細見表格 :data:`align`

    :return: 無

    :示例: ``my_Input_field.set_text_align(text_anchor.upper_left)``

    :示例說明: 設定文字的對齊方式為頂端左對齊

.. function:: input_field_object.set_text_size(size)

    :描述: 設定控制項中文字的字型大小

    :param int size: 文字的字型大小值

    :return: 無

    :示例: ``my_Input_field.set_text_size(12)``

    :示例說明: 設定文字的字型大小為 12 號

.. function:: input_field_object.set_background_color(r, g, b, a)

    :描述: 設定控制項的背景色 

    :param int r: 背景顏色的 r 值，範圍為[0, 255]
    :param int g: 背景顏色的 g 值，範圍為[0, 255]
    :param int b: 背景顏色的 b 值，範圍為[0, 255]
    :param int a: 背景顏色的透明度，[0, 255]

    :return: 無

    :示例: ``my_Input_field.set_background_color(200, 200, 200, 230)``

    :示例說明: 設定背景色的 rgb 值為(200, 200, 200) ，透明度為 230

.. function:: input_field_object.set_hint_text(string, [color_r, color_g, color_b, color_a] , align, size)

    :描述: 設定控制項中的提示文字的屬性

    :param string string: 需要顯示的字符串內容
    :param list [color_r, color_g, color_b, color_a]: 可選參數，需要顯示的字串的顏色，參數分別為顯示顏色 r 值、b 值，g 值，透明度，取值範圍都為[0, 255]
    :param enum align: 可選參數，枚舉類型，需要顯示文字的對齊方式，詳細見表格 :data:`align`
    :param int size: 顯示文字的字型大小

    :return: 無

    :示例: ``my_Input_field.set_hint_text(120, 120, 120, 200, text_anchor.upper_left, 12)``

    :示例說明: 設定提示文字的 rgb 值為（120, 120, 120），透明度為 200 ，字體對齊方式為頂端左對齊，字型大小為 12 號

.. function:: input_field_object.set_hint_text_color(r, g, b, a)

    :描述: 設定控制項提示文字的顏色

    :param int r: 文字顏色的 r 值，範圍為[0, 255]
    :param int g: 文字顏色的 g 值，範圍為[0, 255]
    :param int b: 文字顏色的 b 值，範圍為[0, 255]
    :param int a: 文字顏色的透明度， 範圍為[0, 255]

    :return: 無

    :示例: ``my_Input_field.set_text_color(120, 120, 120, 200)``

    :示例說明: 設定提示文字的 rgb 值為（120, 120, 120），透明度為 200

.. function:: input_field_object.set_hint_text_align(align)

    :描述: 設定提示文字的對齊方式 

    :param enum align: 可選參數，枚舉類型，需要顯示文字的對齊方式，詳細見表格 :data:`align`

    :return: 無

    :示例: ``my_Input_field.set_text_align(text_anchor.upper_left)``

    :示例說明: 設定提示文字的對齊方式為頂端左對齊

.. function:: input_field_object.set_hint_text_size(size)

    :描述: 設定提示文字的字型大小

    :param int size: 文字的字型大小值

    :return: 無

    :示例: ``my_Input_field.set_text_size(12)``

    :示例說明: 設定 hint 物件中文字的字型大小為 12 號