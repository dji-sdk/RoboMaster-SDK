=================
Toggle
=================

The Toggle control is used to draw a switch on the screen. It can perform some specific operations by controlling the opening and closing of the switch.

.. function:: toggle_object.set_text(string, [color_r, color_g, color_b, color_a] , align, size)

    :Description: Set the display text of the control 

    :param string string: String content to be displayed on the control
    :param list [color_r, color_g, color_b, color_a]: An optional parameter. The color of the string to be displayed. The parameters are the display color's r value, b value, g value, and transparency. The value range is [0, 255]
    :param enum align: An optional parameter. Enumeration type. The alignment of the text to be displayed. For details, see table :data:`align`
    :param int size: The font size of the display text

    :return: N/A

    :Example: ``my_Toggle.set_text(120, 120, 120, 200, text_anchor.upper_left, 12)``

    :Example description: Set the RGB value of the text to (120, 120, 120), the transparency to 200, the text alignment to top left, and the font size to 12

.. function:: toggle_object.set_text_color(r, g, b, [a])

    :Description: Set the color of the text 

    :param int r: The R value of the text color. The value range is [0, 255]
    :param int g: The G value of the text color. The value range is [0, 255]
    :param int b: The B value of the text color. The value range is [0, 255]
    :param int a: An optional parameter. The transparency of the text color. The value range is [0, 255] 

    :return: None

    :Example: ``my_Toggle.set_text_color(120, 120, 120, 200)``

    :Example description: Set the RGB value of the font to (120, 120, 120), and transparency to 200

.. function:: toggle_object.set_text_align(align)

    :Description: Set the text alignment 

    :param enum align: An optional parameter. Enumeration type. The alignment of the text to be displayed. For details, see table :data:`align`

    :return: None

    :Example: ``my_Toggle.set_text_align(text_anchor.upper_left)``

    :Example description: Set the text alignment to top left

.. function:: toggle_object.set_text_size(size)

    :Description: Set the text's font size

    :param int size: The font size value of the text

    :return: None

    :Example: ``my_Toggle.set_text_size(12)``

    :Example description: Set the font size of the text to 12

.. function:: toggle_object.set_background_color(r, g, b, [a])

    :Description: Set the background color for the control 

    :param int r: The R value of the background color. The value range is [0, 255]
    :param int g: The G value of the background color. The value range is [0, 255]
    :param int b: The B value of the background color. The value range is [0, 255]
    :param int a: An optional parameter. The transparency of the background color. The value range is [0, 255]

    :return: N/A

    :Example: ``my_Toggle.set_background_color(200, 200, 200, 230)``

    :Example description: Set the RGB value of the background color to (200, 200, 200), and the transparency to 230

.. function:: toggle_object.set_checkmark_color(r, g, b, [a])

    :Description: Set the color for the selected icons of the control 

    :param int r: The R value of the icon color. The value range is [0, 255]
    :param int g: The G value of the icon color. The value range is [0, 255]
    :param int b: The B value of the icon color. The value range is [0, 255]
    :param int a: The transparency of the icon color. The value range is [0, 255]

    :return: N/A

    :Example: ``my_Toggle.set_checkmark_color(200, 200, 200, 230)``

    :Example description: Set the RGB value of the selected icon to (200, 200, 200), and the transparency to 230

.. function:: toggle_object.set_is_on(status)

    :Description: Set the state of the control

    :param bool status: Set whether the control is open. True means open, and False means closed

    :return: N/A

    :Example: ``my_Toggle.set_is_on(True)``

    :Example description: Set the Toggle control to open
