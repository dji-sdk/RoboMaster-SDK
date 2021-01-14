=================
Text
=================

The Text control is used to display text.

.. function:: text_object.set_text(string, [color_r, color_g, color_b, color_a] , align, size)

    :description: Sets text attributes of the control

    :param string string: The content of the string to be displayed
    :param list [color_r, color_g, color_b, color_a]: Optional parameters, which indicate the color of the string to be displayed. These parameters respectively indicate the r value, b value, g value, and transparency of the displayed color, and their value ranges are all [0, 255].
    :param enum align: An optional enumeration-type parameter, which indicates the alignment mode of the text to be displayed. For details, see the :data:`align` table.
    :param int size: The font size of the displayed text

    :return: None

    :example: ``my_Text.set_text(120, 120, 120, 200, text_anchor.upper_left, 12)``

    :example description: Set the rgb value of text color to (120, 120, 120), the transparency to 200, the text alignment mode to top-left, and the font size to 12

.. function:: text_object.set_text_color(r, g, b, a)

    :description: Sets the text color of the control

    :param int r: The r value of text color, whose range is [0, 255]
    :param int g: The g value of text color, whose range is [0, 255]
    :param int b: The b value of text color, whose range is [0, 255]
    :param int a: The transparency of text color, whose range is [0, 255]

    :return: None

    :example: ``my_Text.set_text_color(120, 120, 120, 200)``

    :example description: Set the rgb value of text to (120, 120, 120) and the transparency to 200

.. function:: text_object.set_text_align(align)

    :description: Set the text alignment mode

    :param enum align: An optional enumeration-type parameter, which indicates the alignment mode of the text to be displayed. For details, see the :data:`align` table.

    :return: None

    :example: ``my_Text.set_text_align(text_anchor.upper_left)``

    :example description: Set the text alignment mode to top-left

.. function:: text_object.set_text_size(size)

    :description: Set the text font size

    :param int size: Font size of text

    :return: None

    :example: ``my_Text.set_text_size(12)``

    :example description: Set the font size of text to 12

.. function:: text_object.set_border_active(active)

    :description: Whether to display text borders

    :param bool active: Whether to display text borders, where True indicates to display borders, and False indicates not to display borders

    :return: None

    :example: ``my_Text.set_border_active(True)``

    :example description: Display text borders

.. function:: text_object.set_background_color(r, g, b, a)

    :description: Sets the background color of the control 

    :param int r: The r value of background color, whose range is [0, 255]
    :param int g: The g value of background color, whose range is [0, 255]
    :param int b: The b value of background color, whose range is [0, 255]
    :param int a: The transparency of background color, whose range is [0, 255]

    :return: None

    :example: ``my_Text.set_background_color(200, 200, 200, 230)``

    :example description: Set the rgb value of background color to (200, 200, 200) and the transparency to 230

.. function:: text_object.set_background_active(active)

    :description: Whether to display the text background

    :param bool active: Whether to display the text background, where True indicates to display the background, and False indicates not to display the background

    :return: None

    :example: ``my_Text.set_background_active(True)``

    :example description: Display the text background

.. function:: text_object.append_text(content)

    :description: Adds text to the Text control

    :param string content: The text that needs to be added to the Text control

    :return: None

    :example: ``my_Text.append_text('RoboMaster EP')``

    :example description: Add the ``RoboMaster EP`` text to the Text control

.. data:: align

        +-------------------------+------------+
        |    text_anchor.upper_left    |    Top-left    |
        +-------------------------+------------+
        |    text_anchor.upper_center    |    Top-center    |
        +-------------------------+------------+
        |    text_anchor.upper_right    |    Top-right    |
        +-------------------------+------------+
        |    text_anchor.middle_left    |    Center-left    |
        +-------------------------+------------+
        |    text_anchor.middle_center    |    Center    |
        +-------------------------+------------+
        |    text_anchor.middle_right    |    Center-right    |
        +-------------------------+------------+
        |    text_anchor.lower_left    |    Bottom-left    |
        +-------------------------+------------+
        |    text_anchor.lower_center    |    Bottom-center    |
        +-------------------------+------------+
        |    text_anchor.lower_right    |    Bottom-right    |
        +-------------------------+------------+