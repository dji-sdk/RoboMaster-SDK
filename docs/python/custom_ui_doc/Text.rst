=================
Text
=================

The Text control is used to display texts

.. function:: text_object.set_text(string, [color_r, color_g, color_b, color_a] , align, size)

    :Description: Set the text properties of the control

    :param string string: String content to be displayed
    :param list [color_r, color_g, color_b, color_a]: An optional parameter. The color of the string to be displayed. The parameters are the display color's r value, b value, g value, and transparency. The value range is [0, 255]
    :param enum align: An optional parameter. Enumeration type. The alignment of the text to be displayed. For details, see table :data:`align`
    :param int size: The font size of the display text

    :return: N/A

    :Example: ``my_Text.set_text(120, 120, 120, 200, text_anchor.upper_left, 12)``

    :Example description: Set the RGB value of the text color to (120, 120, 120), the transparency to 200, the text alignment to top left, and the font size to 12

.. function:: text_object.set_text_color(r, g, b, [a])

    :Description: Set the text color of the control

    :param int r: The R value of the text color. The value range is [0, 255]
    :param int g: The G value of the text color. The value range is [0, 255]
    :param int b: The B value of the text color. The value range is [0, 255]
    :param int a: An optional parameter. The transparency of the text color. The value range is [0, 255] 

    :return: N/A

    :Example: ``my_Text.set_text_color(120, 120, 120, 200)``

    :Example description: Set the RGB value of the text to (120, 120, 120), and transparency to 200

.. function:: text_object.set_text_align(align)

    :Description: Set the text alignment

    :param enum align: An optional parameter. Enumeration type. The alignment of the text to be displayed. For details, see table :data:`align`

    :return: None

    :Example: ``my_Text.set_text_align(text_anchor.upper_left)``

    :Example description: Set the text alignment to top left

.. function:: text_object.set_text_size(size)

    :Description: Set the text's font size

    :param int size: The font size value of the text

    :return: None

    :Example: ``my_Text.set_text_size(12)``

    :Example description: Set the font size of the text to 12

.. function:: text_object.set_border_active(active)

    :Description: Display the text border or not

    :param bool active: Whether the text border is displayed. True means to display the border, and False means not to display the border

    :return: N/A

    :Example: ``my_Text.set_border_active(True)``

    :Example description: Display the text border

.. function:: text_object.set_background_color(r, g, b, [a])

    :Description: Set the background color for the control 

    :param int r: The R value of the background color. The value range is [0, 255]
    :param int g: The G value of the background color. The value range is [0, 255]
    :param int b: The B value of the background color. The value range is [0, 255]
    :param int a: An optional parameter. The transparency of the background color. The value range is [0, 255]

    :return: N/A

    :Example: ``my_Text.set_background_color(200, 200, 200, 230)``

    :Example description: Set the RGB value of the background color to (200, 200, 200), and the transparency to 230

.. function:: text_object.append_text(content)

    :Description: Add text to the Text control

    :param string content: The text to be added to Text

    :return: N/A

    :Example: ``my_Text.append_text('RoboMaster EP')``

    :Example description: The text to be added to Text: ``RoboMaster EP``

.. data:: align

        +--------------------------+---------------------+
        |text_anchor.upper_left    |Top left aligned     |
        +--------------------------+---------------------+
        |text_anchor.upper_center  |Top center aligned   |
        +--------------------------+---------------------+
        |text_anchor.upper_right   |Top right aligned    |
        +--------------------------+---------------------+
        |text_anchor.middle_left   |Middle left aligned  |
        +--------------------------+---------------------+
        |text_anchor.middle_center |Middle center aligned|
        +--------------------------+---------------------+
        |text_anchor.middle_right  |Middle right aligned |
        +--------------------------+---------------------+
        |text_anchor.lower_left    |Bottom left aligned  |
        +--------------------------+---------------------+
        |text_anchor.lower_center  |Bottom center aligned|
        +--------------------------+---------------------+
        |text_anchor.lower_right   |Bottom right aligned |
        +--------------------------+---------------------+

