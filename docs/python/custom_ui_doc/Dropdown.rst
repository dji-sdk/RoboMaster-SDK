=================
Dropdown
=================

The Dropdown control is usually used to select a specific value from multiple property options of an object

.. function:: dropdown_object.set_option(*options)

    :Description: Set the content of the drop-down box. The input content is a string list, and the number of elements in the list is the number of options in the drop-down box

    :param string \*args: Options in the drop-down box

    :return: None

    :Example: ``my_Dropdown.set_option('RoboMaser EP', 'People')``

    :Example description: There are two options in the drop-down box: ``RoboMaster EP`` and ``People``

.. function:: dropdown_object.set_text_color(r, g, b, [a])

    :Description: Set the color of the text

    :param int r: The R value of the text color. The value range is [0, 255]
    :param int g: The G value of the text color. The value range is [0, 255]
    :param int b: The B value of the text color. The value range is [0, 255]
    :param int a: An optional parameter. The transparency of the text color. The value range is [0, 255] 

    :return: None

    :Example: ``my_Dropdown.set_text_color(120, 120, 120, 200)``

    :Example description: Set the RGB value of the text to (120, 120, 120), and transparency to 200

.. function:: dropdown_object.set_background_color(r, g, b, [a])

    :Description: Set the background color of the selected item in the drop-down box

    :param int r: The R value of the background color. The value range is [0, 255]
    :param int g: The G value of the background color. The value range is [0, 255]
    :param int b: The B value of the background color. The value range is [0, 255]
    :param int a: An optional parameter. The transparency of the background color. The value range is [0, 255] 

    :return: None

    :Example: ``my_DropDown.set_background_color(200, 200, 200, 230)``

    :Example description: Set the RGB value for the background color of the selected item in the drop-down box to (200, 200, 200), and transparency to 230

.. function:: dropdown_object.set_arrow_color(r, g, b, [a])

    :Description: Set the arrow color of the drop-down box

    :param int r: The R value of the arrow color. The value range is [0, 255]
    :param int g: The G value of the arrow color. The value range is [0, 255]
    :param int b: The B value of the arrow color. The value range is [0, 255]
    :param int a: An optional parameter. The transparency of the arrow color. The value range is [0, 255] 

    :return: None

    :Example: ``my_Dropdown.set_arrow_color(120, 120, 120, 200)``

    :Example description: Set the RGB value for the color of the selected arrow in the drop-down box to (120, 120, 120), and transparency to 200

.. function:: dropdown_object.set_item_color(r, g, b, [a])

    :Description: Set the font color of the unselected items in the drop-down box

    :param int r: The R value of the font color. The value range is [0, 255]
    :param int g: The G value of the font color. The value range is [0, 255]
    :param int b: The B value of the font color. The value range is [0, 255]
    :param int a: An optional parameter. The transparency of the font color. The value range is [0, 255] 

    :return: None

    :Example: ``my_Dropdown.set_item_color(120, 120, 120, 200)``

    :Example description: The RGB value for the font color of unselected items in the drop-down box is (120, 120, 120), and the transparency is 200

.. function:: dropdown_object.set_item_background_color(r, g, b, [a])

    :Description: Set the background color of unselected items in the drop-down box

    :param int r: The R value of the background color. The value range is [0, 255]
    :param int g: The G value of the background color. The value range is [0, 255]
    :param int b: The B value of the background color. The value range is [0, 255]
    :param int a: An optional parameter. The transparency of the background color. The value range is [0, 255] 

    :return: None

    :Example: ``my_DropDown.set_item_background_color(200, 200, 200, 230)``

    :Example description: Set the RGB value for the background color of unselected items in the drop-down box to (200, 200, 200), and transparency to 230

.. function:: dropdown_object.set_item_checkmark_color(r, g, b, [a])

    :Description: Set the color for the selected icon in the drop-down box

    :param int r: checkmarkThe R value of the check mark color. The value range is [0, 255]
    :param int g: checkmarkThe G value of the check mark color. The value range is [0, 255]
    :param int b: checkmarkThe B value of the check mark color. The value range is [0, 255]
    :param int a: An optional parameter. The transparency of the check mark color. The value range is [0, 255] 

    :return: None

    :Example: ``my_DropDown.set_item_checkmark_color(200, 200, 200, 230)``

    :Example description: Set the RGB value for the color of the check mark in the drop-down box to (200, 200, 200), and transparency to 230
