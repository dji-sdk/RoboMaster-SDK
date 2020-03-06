=================
Common
=================

The methods in this section are applicable to all custom UI controls except Stage, so a separate introduction is made here.

.. function:: common_object.set_active(status)

    :Description: Control whether the current control is displayed 

    :param bool status: The active state of the control. True means the current control is displayed, and False means the current control is hidden

    :return: None

    :Example: ``my_Slider.set_active(False)``

    :Example description: Set the my_Slider control to the hidden state

.. function:: common_object.get_active()

    :Description: Obtain the display status of the current control 

    :param void: None

    :return: Bool type. It represents the display status of the control

    :Example: ``status = my_Slider.get_active()``

    :Example description: Obtain the display status of the my_Slider control and assign it to the status variable

.. function:: common_object.set_name(name)

    :Description: Set the current control's name

    :param string name: The name of the control

    :return: None

    :Example: ``my_Dropdown.set_name('my_dropdown')``

    :Example description: Set the my_Dropdown control name to "my_dropdown"

.. function:: common_object.get_name()

    :Description: Obtain the current control's name

    :param void: 无

    :return: String type. It represents the control's name

    :Example: ``name = my_Dropdown.get_name()``

    :Example description: Obtain the my_Dropdown control's name and assign it to the name variable

.. function:: common_object.set_position(x, y)

    :Description: Set the position coordinates of the control, with the origin at the center of the screen

    :param int x: The horizontal coordinate of the control. The value is the position of the actual pixel on the screen. Point 0 is in the horizontal center of the screen, and the right part is the positive direction
    :param int y: The vertical coordinate of the control. The value is the position of the actual pixel on the screen. Point 0 is in the vertical center of the screen, and the upward part is the positive direction

    :return: None

    :Example: ``my_Text.set_position(-200, 500)``

    :Example description: Set the coordinates of the my_Text control to (-200, 500)

.. function:: common_object.get_position()

    :Description: Obtain the position coordinates of the control

    :param void: None

    :return: [x,y]. It represents the position of the control

   :Example: ``pos = my_Text.get_position()``

    :Example description: Obtain the position of the my_Text control and assign it to the pos variable, which is a list

.. function:: common_object.set_size(w, h)

    :Description: Set the size of the control

    :param int w: The width of the control
    :param int h: The height of the control

    :return: None

    :Example: ``my_Button.set_size(300, 200)``

    :Example description: Set the width of the my_Button control to 300 and the height to 200

.. function:: common_object.get_size()

    :Description: Obtain the size of the control

    :param void: None

    :return: [w,h]. It represents the control size

    :Example: ``size = my_Button.get_size()``

    :Example description: Obtain the my_Button control's size, and assign it to the size variable, which is a list

.. function:: common_object.set_rotation(degree)

    :Description: Set the rotation angle of the control

    :param int degree: The rotation angle of the control. The range is [0, 360]. A positive value indicates clockwise rotation, and a negative value indicates counterclockwise rotation

    :return: None

    :Example: ``my_Button.set_rotation(90)``

    :Example description: Set the my_Button control to rotate 90 degrees clockwise

.. function:: common_object.get_rotation()

    :Description: Obtain the rotation angle of the control

    :param void: None

    :return: An integer. Indicates the rotation angle of the control. The range is [0, 360]. A positive value indicates clockwise rotation, and a negative value indicates counterclockwise rotation

    :Example: ``degree = my_Button.get_rotation()``

    :Example description: Obtain the rotation angle of the my_Button control and assign it to the degree variable

.. function:: common_object.set_privot(x, y)

    :Description: Set the anchor coordinates of the control. The input parameter is normalized. The origin is located in the lower left corner of the control. The anchor of the control is defaulted to the control center, that is, (0.5,0.5). The anchor is used as the control point for the position and rotation of the control

    :param int x: The x coordinate of the anchor point. The range is [0, 1], and the right part is the positive direction
    :param int y: The y coordinate of the anchor point. The range is [0, 1], and the upward part is the positive direction

    :return: None

    :Example: ``my_Button.set_pivot(0, 1)``

    :Example description: Set the anchor point of the control to the top left corner of the control

.. function:: common_object.get_privot()

    :Description: Obtain the anchor coordinates of the control

    :param void: None

    :return: [x,y]. Indicates the anchor coordinates of the control

    :Example: ``pivot = my_Button.get_pivot()``

    :Example description: Obtain the anchor coordinate of the control, and assign it to the pivot variable, which is a list

.. function:: common_object.set_order(order)

    :Description: Set the display priority of the control. When multiple controls overlap, the control with a higher priority is at the top. The higher the number, the higher the priority

    :param int order: The specified priority of the control. When several controls overlap, the control with a higher priority is displayed first

    :return: None

    :Example: ``my_Button.set_order(8)``

    :Example description: Set the display priority of the control to 8. When several controls overlap, the controls below this priority will be overwritten

.. function:: common_object.get_order()

    :Description: Obtain the display priority of the control

    :param void: None

    :return: An integer. Indicates the display priority of the control

    :Example: ``order = my_Button.get_order()``

    :Example description: Obtain the display priority of the my_Button control and assign it to the order variable

.. function:: common_object.callback_register(event, callback)

    :Description: The callback function triggered by the control registration event. When the control detects the corresponding event, the registered callback function is executed

    :param string event: Specifies the trigger event for the callback function

 The events that can be registered for each control are as follows:

    * Button control:
        - ``on_click``: In a button press and release process, the event is triggered when the button is released
        - ``on_press_down``: This event is triggered when the button is pressed
        - ``on_press_up``: This event is triggered when the button is released

    * Toggle control:
        - ``on_value_changed``: This event is triggered when the value is changed. The args parameter in the callback function is a bool type, indicating the changed toggle control value

    * Dropdown control:
        - ``on_value_changed``: This event is triggered when the value is changed. The args parameter in the callback function is an integer, indicating the selected index after the Dropdown control value is changed

    * Text control:
        - No trigger event 

    * InputField control:
        - ``on_value_changed``: This event is triggered when the value is changed. The args parameter in the callback function is a string type, indicating the changed InputField control value

    :param function callback: The callback function to be registered. The unified signature of the callback function is: ``def callback(widget,*args,**kw):``, where widget is the control reference of the trigger event, and args is a parameter; TODO: Supplementary parameter description

    :return: None

    :Example 1: 

.. code-block:: python
    :linenos:

    # After the my_Button control is clicked, information is printed to the console, and the robot shoots once

    def button_callback(widget,*args,**kw):
        print('the button is clicked and the button's name is '+ widget.get_name())
        gun_ctrl.fire_once()
    my_Button.callback_register('on_click',button_callback)
..

    :Example 2: 

.. code-block:: python
    :linenos:

    # After the my_Toggle control is clicked, the value changes, information is printed to the console, and the robot plays the sound

    def toggle_callback(widget,*args,**kw):
        print('the toggle's value is changed and the toggle's name is '+ widget.get_name())
        print('the toggle's value now is '+ str(args))
        media_ctrl.play_sound(rm_define.media_sound_recognize_success)
    my_Toggle.callback_register('on_value_changed',toggle_callback)
..

 :Example 3: 

.. code-block:: python
    :linenos:

    # When you click the my_Dropdown control to change its selected value, the value changes, information is printed to the console, and the robot plays the sound

    def dropdown_callback(widget,*args,**kw):
        print('the dropdown's value is changed and the dropdown's name is '+ widget.get_name())
        print('the dropdown's value now is '+ str(args))
        media_ctrl.play_sound(rm_define.media_sound_solmization_1A)
    my_Dropdown.callback_register('on_value_changed',dropdown_callback)
..

    :Example 4: 

.. code-block:: python
    :linenos:

    # When you click my_InputField control to change its selected value, the value changes and information is printed to the console

    def input_field_callback(widget,*args,**kw):
        print('the input_field's value is changed and the input_field's name is '+ widget.get_name())
        print('the input_field's value now is '+ str(args))
    my_InputField.callback_register('on_value_changed',input_field_callback)
