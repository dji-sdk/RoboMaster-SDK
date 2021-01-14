=================
Button
=================

The Button control is used to start or confirm an operation in response to a click from users.

.. function:: button_object.set_text(content, [color_r, color_g, color_b, color_a], align, size)

    :description: Set the text attribute of the button object

    :param string content: The content of the string displayed on the button
    :param list [color_r, color_g, color_b, color_a]: Optional parameters, which indicate the color of the string to be displayed. These parameters respectively indicate the r value, b value, g value, and transparency of the displayed color, and their value ranges are all [0, 255].
    :param enum align: An optional enumeration-type parameter, which indicates the alignment mode of the text to be displayed. For details, see the :data:`align` table.
    :param int size: The font size of the displayed text

    :return: None

    :example: ``my_Button.set_text(120, 120, 120, 255, text_anchor.upper_left, 12)``

    :example description: Set the rgb value of text color to (120, 120, 120), the transparency to 255, the text alignment mode to top-left, and the font size to 12

.. function:: button_object.set_text_color(r, g, b, a)

    :description: Set the color of the text 

    :param int r: The r value of text color, whose range is [0, 255]
    :param int g: The g value of text color, whose range is [0, 255]
    :param int b: The b value of text color, whose range is [0, 255]
    :param int a: The transparency of text color, whose range is [0, 255]

    :return: None

    :example: ``my_button.set_text_color(120, 120, 120, 200)``

    :example description: Set the rgb value of text color to (120, 120, 120) and the transparency to 200

.. function:: button_object.set_text_align(align)

    :description: Set the text alignment mode 

    :param enum align: An optional enumeration-type parameter, which indicates the alignment mode of the text to be displayed. For details, see the :data:`align` table.

    :return: None

    :example: ``my_button.set_text_align(text_anchor.upper_left)``

    :example description: Set the text alignment mode to top-left

.. function:: button_object.set_text_size(size)

    :description: Set the text font size

    :param int size: Text font size

    :return: None

    :example: ``my_button.set_text_size(12)``

    :example description: Set the text font size to 12

.. function:: button_object.set_background_color(r, g, b, a)

    :description: Set the background color of the button 

    :param int r: The r value of font color, whose range is [0, 255]
    :param int g: The g value of font color, whose range is [0, 255]
    :param int b: The b value of font color, whose range is [0, 255]
    :param int a: The transparency of font color, whose range is [0, 255]

    :return: None

    :example: ``my_button.set_background_color(200, 200, 200, 230)``

    :example description: Set the rgb value of background color to (200, 200, 200) and the transparency to 230