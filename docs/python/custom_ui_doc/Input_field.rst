=================
InputField
=================

The InputField control is used to receive textual information input by users

.. function:: inputfield_object.set_text(string, [color_r, color_g, color_b, color_a] , align, size)

    :Description: Set text properties for input field objects

    :param string string: Strings to be displayed
    :param list [color_r, color_g, color_b, color_a]: Optional parameters. The color of the string to be displayed. The parameters are the display color's r value, b value, g value, and transparency. The value range is [0, 255]
    :param enum align: An optional parameter. Enumeration type. It represents the alignment of the text to be displayed. For details, please see table :data:`align`
    :param int size: The font size of the display text

    :return: None

    :Example: ``my_InputField.set_text(120, 120, 120, 200, text_anchor.upper_left, 12)``

    :Example description: Set the RGB value of the font to (120, 120, 120), the transparency to 200, the text alignment to top left, and the font size to 12

.. function:: input_field_object.set_text_color(r, g, b, [a])

    :Description: Set the color of the text 

    :param int r: The R value of the text color. The value range is [0, 255]
    :param int g: The G value of the text color. The value range is [0, 255]
    :param int b: The B value of the text color. The value range is [0, 255]
    :param int a: An optional parameter. The transparency of the text color. The value range is [0, 255] 

    :return: None

    :Example: ``my_button.set_text_color(120, 120, 120, 200)``

    :Example description: Set the RGB value of the font to (120, 120, 120), and transparency to 200

.. function:: input_field_object.set_text_align(align)

    :Description: Set the text alignment for the control 

    :param enum align: An optional parameter. Enumeration type. It represents the alignment of the text to be displayed. For details, please see table :data:`align`

    :return: None

    :Example: ``my_Input_field.set_text_align(text_anchor.upper_left)``

    :Example description: Set the text alignment to top left

.. function:: input_field_object.set_text_size(size)

    :Description: Set the text font size for the control

    :param int size: The font size value of the text

    :return: None

    :Example: ``my_Input_field.set_text_size(12)``

    :Example description: Set the font size of the text to 12

.. function:: input_field_object.set_background_color(r, g, b, [a])

    :Description: Set the background color for the control 

    :param int r: The R value of the background color. The value range is [0, 255]
    :param int g: The G value of the background color. The value range is [0, 255]
    :param int b: The B value of the background color. The value range is [0, 255]
    :param int a: An optional parameter. The transparency of the background color. The value range is [0, 255]

    :return: None

    :Example: ``my_Input_field.set_background_color(200, 200, 200, 230)``

    :Example description: Set the RGB value of the background color to (200, 200, 200), and the transparency to 230

.. function:: input_field_object.set_hint_text(string, [color_r, color_g, color_b, color_a] , align, size)

    :Description: Set properties for the hint text within the control

    :param string string: Strings to be displayed
    :param list [color_r, color_g, color_b, color_a]: Optional parameters. The color of the string to be displayed. The parameters are the display color's r value, b value, g value, and transparency. The value range is [0, 255]
    :param enum align: An optional parameter. Enumeration type. It represents the alignment of the text to be displayed. For details, please see table  :data:`align`
    :param int size: The font size of the display text

    :return: None

    :Example: ``my_Input_field.set_hint_text(120, 120, 120, 200, text_anchor.upper_left, 12)``

    :Example description: Set the RGB value of the hint text to (120, 120, 120), the transparency to 200, the text alignment to top left, and the font size to 12

.. function:: input_field_object.set_hint_text_color(r, g, b, [a])

    :Description: Set the color of the control's hint text

    :param int r: The R value of the text color. The value range is [0, 255]
    :param int g: The G value of the text color. The value range is [0, 255]
    :param int b: The B value of the text color. The value range is [0, 255]
    :param int a: An optional parameter. The transparency of the text color. The value range is [0, 255] 

    :return: None

    :Example: ``my_Input_field.set_text_color(120, 120, 120, 200)``

    :Example description: Set the RGB value of the hint text to (120, 120, 120), and transparency to 200

.. function:: input_field_object.set_hint_text_align(align)

    :Description: Set the alignment of the hint text 

    :param enum align: An optional parameter. Enumeration type. It represents the alignment of the text to be displayed. For details, please see table  :data:`align`

    :return: None

    :Example: ``my_Input_field.set_text_align(text_anchor.upper_left)``

    :Example description: Set the alignment of the hint text to top left

.. function:: input_field_object.set_hint_text_size(size)

    :Description: Set the font size of the hint text

    :param int size: The font size value of the text

    :return: None

    :Example: ``my_Input_field.set_text_size(12)``

    :Example description: Set the font size of the text within hint objects to 12
