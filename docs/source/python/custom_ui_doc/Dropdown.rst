=================
Dropdown
=================

The Dropdown control is often used to select a specific value among the multiple attribute options of an object.

.. function:: dropdown_object.set_options(*options)

    :description: Sets the content of the dropdown box, which is a list of strings. The number of items in the list is the number of dropdown box options.

    :param string \*args: Options in the dropdown box

    :return: None

    :example: ``my_Dropdown.set_options('RoboMaser EP', 'People')``

    :example description: There are two options in the dropdown box, ``RoboMaster EP`` and ``People``

.. function:: dropdown_object.set_background_color(r, g, b, a)

    :description: Sets the background color of the selected item in the dropdown box

    :param int r: The r value of background color, whose range is [0, 255]
    :param int g: The g value of the background color, whose range is [0, 255]
    :param int b: The b value of the background color, whose range is [0, 255]
    :param int a: The transparency of the background color, whose range is [0, 255]

    :return: None

    :example: ``my_DropDown.set_background_color(200, 200, 200, 230)``

    :example description: Set the rgb value of the background color of selected items in the dropdown box to (200, 200, 200) and the transparency to 230

.. function:: dropdown_object.set_arrow_color(r, g, b, a)

    :description: Sets the color of the selection arrow in the dropdown box

    :param int r: The r value of arrow color, whose range is [0, 255]
    :param int g: The g value of arrow color, whose range is [0, 255]
    :param int b: The b value of arrow color, whose range is [0, 255]
    :param int a: The transparency of arrow color, whose range is [0, 255]

    :return: None

    :example: ``my_Dropdown.set_arrow_color(120, 120, 120, 200)``

    :example description: Set the rgb value of the color of the selection arrow in the dropdown box to (120, 120, 120) and the transparency to 200

.. function:: dropdown_object.set_item_background_color(r, g, b, a)

    :description: Sets the background color of unselected items in the dropdown box

    :param int r: The r value of background color, whose range is [0, 255]
    :param int g: The g value of the background color, whose range is [0, 255]
    :param int b: The b value of the background color, whose range is [0, 255]
    :param int a: The transparency of the background color, whose range is [0, 255]

    :return: None

    :example: ``my_DropDown.set_item_background_color(200, 200, 200, 230)``

    :example description: Set the rgb value of the background color of unselected items in the dropdown box to (200, 200, 200) and the transparency to 230

.. function:: dropdown_object.set_item_checkmark_color(r, g, b, a)

    :description: Sets the color of the selection icon in the dropdown box

    :param int r: The r value of checkmark color, whose range is [0, 255]
    :param int g: The g value of checkmark color, whose range is [0, 255]
    :param int b: The b value of checkmark color, whose range is [0, 255]
    :param int a: The transparency of checkmark color, whose range is [0, 255]

    :return: None

    :example: ``my_DropDown.set_item_checkmark_color(200, 200, 200, 230)``

    :example description: Set the rgb value of the checkmark color in the dropdown box to (200, 200, 200) and the transparency to 230 