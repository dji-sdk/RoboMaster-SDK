=================
Button
=================

The Button control is used to initiate or confirm an action in response to a click from the user.

.. function:: button_object.set_text(content, [color_r, color_g, color_b, color_a], align, size)

    :Description: Set text properties for button objects

    :param string content: The string displayed on a button
    :param list [color_r, color_g, color_b, [color_a]]: Optional parameters. The color of the string to be displayed. The parameters are the display color's r value, b value, g value, and transparency. The value range is [0, 255]
    :param enum align: An optional parameter. Enumeration type. It represents the alignment of the text to be displayed. For details, please see table :data:`align`
    :param int size: The font size of the display text

    :return: None

    :Example: ``my_Button.set_text(120, 120, 120, 255, text_anchor.upper_left, 12)``

    :Example description: Set the RGB value of the text color to (120, 120, 120), the transparency to 255, the text alignment to top left, and the font size to 12

.. function:: button_object.set_text_color(r, g, b, [a])

    :Description: Set the color of the text 

    :param int r: The R value of the text color. The value range is [0, 255]
    :param int g: The G value of the text color. The value range is [0, 255]
    :param int b: The B value of the text color. The value range is [0, 255]
    :param int a: An optional parameter. Transparency. The value range is [0, 255] 

    :return: None

    :Example: ``my_button.set_text_color(120, 120, 120, 200)``

    :Example description: Set the RGB value of the text color to (120, 120, 120), and transparency to 200

.. function:: button_object.set_text_align(align)

    :Description: Set the text alignment 

    :param enum align: An optional parameter. Enumeration type. It represents the alignment of the text to be displayed. For details, please see table :data:`align`

    :return: None

    :Example: ``my_button.set_text_align(text_anchor.upper_left)``

    :Example description: Set the text alignment to top left

.. function:: button_object.set_text_size(size)

    :Description: Set the text's font size

    :param int size: The font size value of the text

    :return: None

    :Example: ``my_button.set_text_size(12)``

    :Example description: Set the font size of the text to 12

.. function:: button_object.set_background_color(r, g, b, [a])

    :Description: Set the background color of the button 

    :param int r: The R value of the font color. The value range is [0, 255]
    :param int g: The G value of the font color. The value range is [0, 255]
    :param int b: The B value of the font color. The value range is [0, 255]
    :param int a: An optional parameter. The transparency of the font color. The value range is [0, 255]

    :return: None

    :Example: ``my_button.set_background_color(200, 200, 200, 230)``

    :Example description: Set the RGB value of the background color to (200, 200, 200), and the transparency to 230
