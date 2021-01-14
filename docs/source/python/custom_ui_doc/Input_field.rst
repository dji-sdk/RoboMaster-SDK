=================
InputField
=================

The InputField control is used to receive text information input by users.

.. function:: inputfield_object.set_text(string, [color_r, color_g, color_b, color_a] , align, size)

    :description: Sets the text attributes in the input box object

    :param string string: The content of the string to be displayed
    :param list [color_r, color_g, color_b, color_a]: Optional parameters, which indicate the color of the string to be displayed. These parameters respectively indicate the r value, b value, g value, and transparency of the displayed color, and their value ranges are all [0, 255].
    :param enum align: An optional enumeration-type parameter, which indicates the alignment mode of the text to be displayed. For details, see the :data:`align` table.
    :param int size: The font size of the displayed text

    :return: None

    :example: ``my_InputField.set_text('Hello RoboMaster',120, 120, 120, 200, text_anchor.upper_left, 12)``

    :example description: Set the RGB value of the font to (120, 120, 120), the transparency to 200, the font alignment mode to top-left, and the font size to 12

.. function:: input_field_object.set_text_color(r, g, b, a)

    :description: Sets the color of text 

    :param int r: The r value of text color, whose range is [0, 255]
    :param int g: The g value of text color, whose range is [0, 255]
    :param int b: The b value of text color, whose range is [0, 255]
    :param int a: The transparency of text color, whose range is [0, 255]

    :return: None

    :example: ``my_button.set_text_color(120, 120, 120, 200)``

    :example description: Set the RGB value of the font to (120, 120, 120) and the transparency to 200

.. function:: input_field_object.set_text_align(align)

    :description: Sets the alignment mode of text in the control 

    :param enum align: An optional enumeration-type parameter, which indicates the alignment mode of the text to be displayed. For details, see the :data:`align` table.

    :return: None

    :example: ``my_Input_field.set_text_align(text_anchor.upper_left)``

    :example description: Set the text alignment mode to top-left

.. function:: input_field_object.set_text_size(size)

    :description: Sets the font size of text in the control

    :param int size: Font size of text

    :return: None

    :example: ``my_Input_field.set_text_size(12)``

    :example description: Set the font size of text to 12

.. function:: input_field_object.set_background_color(r, g, b, a)

    :description: Sets the background color of the control 

    :param int r: The r value of background color, whose range is [0, 255]
    :param int g: The g value of background color, whose range is [0, 255]
    :param int b: The b value of background color, whose range is [0, 255]
    :param int a: The transparency of background color, whose range is [0, 255]

    :return: None

    :example: ``my_Input_field.set_background_color(200, 200, 200, 230)``

    :example description: Set the RGB value of the background color to (200, 200, 200) and the transparency to 230

.. function:: input_field_object.set_hint_text(string, [color_r, color_g, color_b, color_a] , align, size)

    :description: Sets the attributes of prompt text in the control

    :param string string: The content of the string to be displayed
    :param list [color_r, color_g, color_b, color_a]: Optional parameters, which indicate the color of the string to be displayed. These parameters respectively indicate the r value, b value, g value, and transparency of the displayed color, and their value ranges are all [0, 255].
    :param enum align: An optional enumeration-type parameter, which indicates the alignment mode of the text to be displayed. For details, see the :data:`align` table.
    :param int size: The font size of the displayed text

    :return: None

    :example: ``my_Input_field.set_hint_text(120, 120, 120, 200, text_anchor.upper_left, 12)``

    :example description: Set the RGB value of the prompt text to (120, 120, 120), the transparency to 200, the font alignment mode to top-left, and the font size to 12

.. function:: input_field_object.set_hint_text_color(r, g, b, a)

    :description: Sets the color of control prompt text

    :param int r: The r value of text color, whose range is [0, 255]
    :param int g: The g value of text color, whose range is [0, 255]
    :param int b: The b value of text color, whose range is [0, 255]
    :param int a: The transparency of text color, whose range is [0, 255]

    :return: None

    :example: ``my_Input_field.set_text_color(120, 120, 120, 200)``

    :example description: Set the RGB value of the prompt text to (120, 120, 120) and the transparency to 200

.. function:: input_field_object.set_hint_text_align(align)

    :description: Sets the alignment mode of prompt text 

    :param enum align: An optional enumeration-type parameter, which indicates the alignment mode of the text to be displayed. For details, see the :data:`align` table.

    :return: None

    :example: ``my_Input_field.set_text_align(text_anchor.upper_left)``

    :example description: Set the alignment mode of prompt text to top left

.. function:: input_field_object.set_hint_text_size(size)

    :description: Sets the font size of prompt text

    :param int size: Font size of text

    :return: None

    :example: ``my_Input_field.set_text_size(12)``

    :example description: Set the font size of the text in the hint object to 12