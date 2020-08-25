=================
Toggle
=================

Toggle 控件用于在屏幕上绘制一个开关，通过控制开关的开启与闭合来执行一些具体的操作。

.. function:: toggle_object.set_text(string, [color_r, color_g, color_b, color_a] , align, size)

    :描述: 设置控件的显示文字 

    :param string string: 控件上显示的字符串内容
    :param list [color_r, color_g, color_b, color_a]: 可选参数，需要显示的字符串的颜色，参数分别为显示颜色 r 值、b 值、g 值、透明度，取值范围都为 [0, 255]
    :param enum align: 可选参数，枚举类型，需要显示文字的对齐方式，详细见表格 :data:`align`
    :param int size: 显示文字的字号大小

    :return: 无

    :示例: ``my_Toggle.set_text(120, 120, 120, 200, text_anchor.upper_left, 12)``

    :示例说明: 设置文字的 rgb 值为（120, 120, 120），透明度为 200，字体对齐方式为顶端左对齐，字号大小为 12 号

.. function:: toggle_object.set_text_color(r, g, b, a)

    :描述: 设置文字的颜色 

    :param int r: 文字颜色的 r 值，范围为 [0, 255]
    :param int g: 文字颜色的 g 值，范围为 [0, 255]
    :param int b: 文字颜色的 b 值，范围为 [0, 255]
    :param int a: 文字颜色的透明度，范围为 [0, 255]

    :return: 无

    :示例: ``my_Toggle.set_text_color(120, 120, 120, 200)``

    :示例说明: 设置字体的 rgb 值为（120, 120, 120），透明度为 200

.. function:: toggle_object.set_text_align(align)

    :描述: 设置文字的对齐方式 

    :param enum align: 可选参数，枚举类型，需要显示文字的对齐方式，详细见表格 :data:`align`

    :return: 无

    :示例: ``my_Toggle.set_text_align(text_anchor.upper_left)``

    :示例说明: 设置字体的对齐方式为顶端左对齐

.. function:: toggle_object.set_text_size(size)

    :描述: 设置文字的字号大小

    :param int size: 文字的字号值

    :return: 无

    :示例: ``my_Toggle.set_text_size(12)``

    :示例说明: 设置文字的字号为 12 号

.. function:: toggle_object.set_background_color(r, g, b, a)

    :描述: 设置控件的背景色 

    :param int r: 背景颜色的 r 值，范围为 [0, 255]
    :param int g: 背景颜色的 g 值，范围为 [0, 255]
    :param int b: 背景颜色的 b 值，范围为 [0, 255]
    :param int a: 背景颜色的透明度，[0, 255]

    :return: 无

    :示例: ``my_Toggle.set_background_color(200, 200, 200, 230)``

    :示例说明: 设置背景色的 rgb 值为 (200, 200, 200)，透明度为 230

.. function:: toggle_object.set_checkmark_color(r, g, b, a)

    :描述: 设置控件选中图标的颜色 

    :param int r: 图标颜色的 r 值，范围为 [0, 255]
    :param int g: 图标颜色的 g 值，范围为 [0, 255]
    :param int b: 图标颜色的 b 值，范围为 [0, 255]
    :param int a: 图标颜色的透明度，范围为 [0, 255]

    :return: 无

    :示例: ``my_Toggle.set_checkmark_color(200, 200, 200, 230)``

    :示例说明: 设置选中图标的 rgb 值为 (200, 200, 200)，透明度为 230

.. function:: toggle_object.set_is_on(status)

    :描述: 设置控件的状态

    :param bool status: 设置控件是否为打开状态，True 表示打开，False 表示关闭

    :return: 无

    :示例: ``my_Toggle.set_is_on(True)``

    :示例说明: 设置 Toggle 控件为打开状态