=================
Dropdown
=================

Dropdown 控件通常用於在某個對象的多個屬性選項中，選中某個特定值

.. function:: dropdown_object.set_options(*options)

    :描述: 設置下拉框中的內容，輸入為字符串列表，列表中元素個數為下拉框選項個數

    :param string \*args: 下拉框中的選項內容

    :return: 無

    :示例: ``my_Dropdown.set_options('RoboMaser EP', 'People')``

    :示例說明: 下拉框中有兩個選項，分別為 ``RoboMaster EP`` 與 ``People``

.. function:: dropdown_object.set_background_color(r, g, b, a)

    :描述: 設置下拉框中選中的條目的背景色

    :param int r: 背景顏色的 r 值，範圍為[0, 255]
    :param int g: 背景顏色的 g 值，範圍為[0, 255]
    :param int b: 背景顏色的 b 值，範圍為[0, 255]
    :param int a: 背景顏色的透明度，範圍為[0, 255]

    :return: 無

    :示例: ``my_DropDown.set_background_color(200, 200, 200, 230)``

    :示例說明: 設置下拉框中選中的條目的背景色的 rgb 值為(200, 200, 200) ，透明度為 230

.. function:: dropdown_object.set_arrow_color(r, g, b, a)

    :描述: 設置下拉框選箭頭的顏色

    :param int r: 箭頭顏色的 r 值，範圍為[0, 255]
    :param int g: 箭頭顏色的 g 值，範圍為[0, 255]
    :param int b: 箭頭顏色的 b 值，範圍為[0, 255]
    :param int a: 箭頭顏色的透明度，範圍為[0, 255]

    :return: 無

    :示例: ``my_Dropdown.set_arrow_color(120, 120, 120, 200)``

    :示例說明: 設置下拉框選中箭頭顏色的 rgb 值為（120, 120, 120），透明度為 200

.. function:: dropdown_object.set_item_background_color(r, g, b, a)

    :描述: 設置下拉框中未被選擇的條目的背景色

    :param int r: 背景顏色的 r 值，範圍為[0, 255]
    :param int g: 背景顏色的 g 值，範圍為[0, 255]
    :param int b: 背景顏色的 b 值，範圍為[0, 255]
    :param int a: 背景顏色的透明度，範圍為[0, 255]

    :return: 無

    :示例: ``my_DropDown.set_item_background_color(200, 200, 200, 230)``

    :示例說明: 設置下拉框中未被選擇的條目的背景色的 rgb 值為(200, 200, 200) ，透明度為 230

.. function:: dropdown_object.set_item_checkmark_color(r, g, b, a)

    :描述: 設置下拉框中選中圖標的顏色

    :param int r: checkmark顏色的 r 值，範圍為[0, 255]
    :param int g: checkmark顏色的 g 值，範圍為[0, 255]
    :param int b: checkmark顏色的 b 值，範圍為[0, 255]
    :param int a: checkmark 顏色的透明度，範圍為[0, 255]

    :return: 無

    :示例: ``my_DropDown.set_item_checkmark_color(200, 200, 200, 230)``

    :示例說明: 設置下拉框中 checkmark 顏色的 rgb 值為(200, 200, 200) ，透明度為 230 