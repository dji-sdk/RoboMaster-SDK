=================
Text
=================

Text 控件用于显示文本

.. function:: text_object.set_text(string, [color_r, color_g, color_b, color_a] , align, size)

    :描述: 设置控件的文字属性

    :param string string: 需要显示的字符串内容
    :param list [color_r, color_g, color_b, color_a]: 可选参数，需要显示的字符串的颜色，参数分别为显示颜色 r 值、b 值、g 值，透明度，取值范围都为 [0, 255]
    :param enum align: 可选参数，枚举类型，需要显示文字的对齐方式，详细见表格 :data:`align`
    :param int size: 显示文字的字号大小

    :return: 无

    :示例: ``my_Text.set_text(120, 120, 120, 200, text_anchor.upper_left, 12)``

    :示例说明: 设置文字颜色的 rgb 值为（120, 120, 120），透明度为 200，字体对齐方式为顶端左对齐，字号大小为 12 号

.. function:: text_object.set_text_color(r, g, b, a)

    :描述: 设置控件的文字颜色

    :param int r: 文字颜色的 r 值，范围为 [0, 255]
    :param int g: 文字颜色的 g 值，范围为 [0, 255]
    :param int b: 文字颜色的 b 值，范围为 [0, 255]
    :param int a: 文字颜色的透明度，范围为 [0, 255]

    :return: 无

    :示例: ``my_Text.set_text_color(120, 120, 120, 200)``

    :示例说明: 设置文字的 rgb 值为（120, 120, 120），透明度为 200

.. function:: text_object.set_text_align(align)

    :描述: 设置文字的对齐方式

    :param enum align: 可选参数，枚举类型，需要显示文字的对齐方式，详细见表格 :data:`align`

    :return: 无

    :示例: ``my_Text.set_text_align(text_anchor.upper_left)``

    :示例说明: 设置文字的对齐方式为顶端左对齐

.. function:: text_object.set_text_size(size)

    :描述: 设置文字的字号大小

    :param int size: 文字的字号值

    :return: 无

    :示例: ``my_Text.set_text_size(12)``

    :示例说明: 设置文字的字号为 12 号

.. function:: text_object.set_border_active(active)

    :描述: 是否显示文字边框

    :param bool active: 是否显示文字边框，True 表示显示边框，False 表示不显示边框

    :return: 无

    :示例: ``my_Text.set_border_active(True)``

    :示例说明: 显示文字边框

.. function:: text_object.set_background_color(r, g, b, a)

    :描述: 设置控件的背景色 

    :param int r: 背景颜色的 r 值，范围为 [0, 255]
    :param int g: 背景颜色的 g 值，范围为 [0, 255]
    :param int b: 背景颜色的 b 值，范围为 [0, 255]
    :param int a: 背景颜色的透明度，范围为 [0, 255]

    :return: 无

    :示例: ``my_Text.set_background_color(200, 200, 200, 230)``

    :示例说明: 设置背景色的 rgb 值为 (200, 200, 200)，透明度为 230

.. function:: text_object.set_background_active(active)

    :描述: 是否显示文字背景

    :param bool active: 是否显示背景，True 表示显示背景，False 表示不显示背景

    :return: 无

    :示例: ``my_Text.set_background_active(True)``

    :示例说明: 显示文字背景

.. function:: text_object.append_text(content)

    :描述: 向 Text 控件中增加文本

    :param string content: 需要向 Text 中增加的文本

    :return: 无

    :示例: ``my_Text.append_text('RoboMaster EP')``

    :示例说明: 向 Text 中增加的文字 ``RoboMaster EP``

.. data:: align

        +-------------------------+------------+
        |text_anchor.upper_left   |顶端左对齐  |
        +-------------------------+------------+
        |text_anchor.upper_center |顶端居中对齐|
        +-------------------------+------------+
        |text_anchor.upper_right  |顶端右对齐  |
        +-------------------------+------------+
        |text_anchor.middle_left  |中间左对齐  |
        +-------------------------+------------+
        |text_anchor.middle_center|中间居中对齐|
        +-------------------------+------------+
        |text_anchor.middle_right |中间右对齐  |
        +-------------------------+------------+
        |text_anchor.lower_left   |底端左对齐  |
        +-------------------------+------------+
        |text_anchor.lower_center |底端居中对齐|
        +-------------------------+------------+
        |text_anchor.lower_right  |底端右对齐  |
        +-------------------------+------------+