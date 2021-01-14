=================
Toggle
=================

The Toggle control is used to draw a switch on the screen and perform certain operations by turning the switch on and off.

.. function:: toggle_object.set_text(string, [color_r, color_g, color_b, color_a] , align, size)

    :description: Set the display text of the control 

    :param string string: The content of the string displayed on the control
    :param list [color_r, color_g, color_b, color_a]: Optional parameters, which indicate the color of the string to be displayed. These parameters respectively indicate the r value, b value, g value, and transparency of the displayed color, and their value ranges are all [0, 255].
    :param enum align: An optional enumeration-type parameter, which indicates the alignment mode of the text to be displayed. For details, see the :data:`align` table.
    :param int size: The font size of the displayed text

    :return: None

    :example: ``my_Toggle.set_text(120, 120, 120, 200, text_anchor.upper_left, 12)``

    :example description: Set the rgb value of text to (120, 120, 120), the transparency to 200, the text alignment mode to top-left, and the font size to 12

.. function:: toggle_object.set_text_color(r, g, b, a)

    :description: Sets the color of text 

    :param int r: The r value of text color, whose range is [0, 255]
    :param int g: The g value of text color, whose range is [0, 255]
    :param int b: The b value of text color, whose range is [0, 255]
    :param int a: The transparency of text color, whose range is [0, 255]

    :return: None

    :example: ``my_Toggle.set_text_color(120, 120, 120, 200)``

    :example description: Set the rgb value of the font to (120, 120, 120) and the transparency to 200

.. function:: toggle_object.set_text_align(align)

    :description: Set the text alignment mode 

    :param enum align: An optional enumeration-type parameter, which indicates the alignment mode of the text to be displayed. For details, see the :data:`align` table.

    :return: None

    :example: ``my_Toggle.set_text_align(text_anchor.upper_left)``

    :example description: Set the font alignment mode to top-left

.. function:: toggle_object.set_text_size(size)

    :description: Set the text font size

    :param int size: Font size of text

    :return: None

    :example: ``my_Toggle.set_text_size(12)``

    :example description: Set the font size of text to 12

.. function:: toggle_object.set_background_color(r, g, b, a)

    :description: Sets the background color of the control 

    :param int r: The r value of background color, whose range is [0, 255]
    :param int g: The g value of background color, whose range is [0, 255]
    :param int b: The b value of background color, whose range is [0, 255]
    :param int a: The transparency of background color, whose range is [0, 255]

    :return: None

    :example: ``my_Toggle.set_background_color(200, 200, 200, 230)``

    :example description: Set the rgb value of background color to (200, 200, 200) and the transparency to 230

.. function:: toggle_object.set_checkmark_color(r, g, b, a)

    :description: Set the color of the selection icon in the control 

    :param int r: The r value of icon color, whose range is [0, 255]
    :param int g: The g value of icon color, whose range is [0, 255]
    :param int b: The b value of icon color, whose range is [0, 255]
    :param int a: The transparency of icon color, whose range is [0, 255]

    :return: None

    :example: ``my_Toggle.set_checkmark_color(200, 200, 200, 230)``

    :example description: Set the rgb value of the selection icon to (200, 200, 200) and the transparency to 230

.. function:: toggle_object.set_is_on(status)

    :description: Set the state of the control

    :param bool status: Set whether the control is enabled, where True indicates yes, and False indicates no

    :return: None

    :example: ``my_Toggle.set_is_on(True)``

    :example description: Set the Toggle control to enabled