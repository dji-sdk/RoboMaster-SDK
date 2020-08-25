=================
Dropdown
=================

Dropdown 控件通常用于在某个对象的多个属性选项中，选中某个特定值

.. function:: dropdown_object.set_options(*options)

    :描述: 设置下拉框中的内容，输入为字符串列表，列表中元素个数为下拉框选项个数

    :param string \*args: 下拉框中的选项内容

    :return: 无

    :示例: ``my_Dropdown.set_options('RoboMaser EP', 'People')``

    :示例说明: 下拉框中有两个选项，分别为 ``RoboMaster EP`` 与 ``People``

.. function:: dropdown_object.set_background_color(r, g, b, a)

    :描述: 设置下拉框中选中的条目的背景色

    :param int r: 背景颜色的 r 值，范围为[0, 255]
    :param int g: 背景颜色的 g 值，范围为[0, 255]
    :param int b: 背景颜色的 b 值，范围为[0, 255]
    :param int a: 背景颜色的透明度，范围为[0, 255]

    :return: 无

    :示例: ``my_DropDown.set_background_color(200, 200, 200, 230)``

    :示例说明: 设置下拉框中选中的条目的背景色的 rgb 值为(200, 200, 200) ，透明度为 230

.. function:: dropdown_object.set_arrow_color(r, g, b, a)

    :描述: 设置下拉框选箭头的颜色

    :param int r: 箭头颜色的 r 值，范围为[0, 255]
    :param int g: 箭头颜色的 g 值，范围为[0, 255]
    :param int b: 箭头颜色的 b 值，范围为[0, 255]
    :param int a: 箭头颜色的透明度，范围为[0, 255]

    :return: 无

    :示例: ``my_Dropdown.set_arrow_color(120, 120, 120, 200)``

    :示例说明: 设置下拉框选中箭头颜色的 rgb 值为（120, 120, 120），透明度为 200

.. function:: dropdown_object.set_item_background_color(r, g, b, a)

    :描述: 设置下拉框中未被选择的条目的背景色

    :param int r: 背景颜色的 r 值，范围为[0, 255]
    :param int g: 背景颜色的 g 值，范围为[0, 255]
    :param int b: 背景颜色的 b 值，范围为[0, 255]
    :param int a: 背景颜色的透明度，范围为[0, 255]

    :return: 无

    :示例: ``my_DropDown.set_item_background_color(200, 200, 200, 230)``

    :示例说明: 设置下拉框中未被选择的条目的背景色的 rgb 值为(200, 200, 200) ，透明度为 230

.. function:: dropdown_object.set_item_checkmark_color(r, g, b, a)

    :描述: 设置下拉框中选中图标的颜色

    :param int r: checkmark颜色的 r 值，范围为[0, 255]
    :param int g: checkmark颜色的 g 值，范围为[0, 255]
    :param int b: checkmark颜色的 b 值，范围为[0, 255]
    :param int a: checkmark 颜色的透明度，范围为[0, 255]

    :return: 无

    :示例: ``my_DropDown.set_item_checkmark_color(200, 200, 200, 230)``

    :示例说明: 设置下拉框中 checkmark 颜色的 rgb 值为(200, 200, 200) ，透明度为 230 