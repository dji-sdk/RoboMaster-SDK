=================
Common
=================

The methods described in this section are applicable to all custom UI controls except Stage.

.. function:: common_object.set_active(status)

    :description: Sets whether to display the current control 

    :param bool status: The activity of the control, where True indicates to display the current control, and False indicates to hide the current control

    :return: None

    :example: ``my_Slider.set_active(Flase)``

    :example description: Set the my_Slider control to hidden

.. function:: common_object.get_active()

    :description: Obtains the display state of the current control 

    :param void: None

    :return: A boolean value, which indicates the display state of the control

    :example: ``status = my_Slider.get_active()``

    :example description: Obtain the display state of the my_Slider control and assign it to the status variable

.. function:: common_object.set_name(name)

    :description: Set the name of the current control

    :param string name: Name of the control

    :return: None

    :example: ``my_Dropdown.set_name('my_dropdown')``

    :example description: Set the name of the my_Dropdown control to "my_dropdown"

.. function:: common_object.get_name()

    :description: Obtains the name of the current control

    :param void: None

    :return: A string, which indicates the name of the control

    :example: ``name = my_Dropdown.get_name()``

    :example description: Obtain the name of the my_Dropdown control and assign it to the name variable

.. function:: common_object.set_position(x, y)

    :description: Sets the coordinates of the control, where the origin is at the center of the screen

    :param int x: The abscissa of the control, whose value is the actual pixel position on the screen. The 0 point is at the horizontal center of the screen, and rightward is the positive direction.
    :param int y: The ordinate of the control, whose value is the actual pixel position on the screen. The 0 point is at the vertical center of the screen, and upward is the positive direction.

    :return: None

    :example: ``my_Text.set_position(-200, 500)``

    :example description: Set the coordinates of the my_Text control to (-200, 500)

.. function:: common_object.get_position()

    :description: Obtains the coordinates of the control

    :param void: None

    :return: [x,y], which represents the position of the control

    :example: ``pos = my_Text.get_position()``

    :example description: Obtain the position of the my_Text control and assign it to the pos variable, which is a list

.. function:: common_object.set_size(w, h)

    :description: Sets the size of the control

    :param int w: Width of the control
    :param int h: Height of the control

    :return: None

    :example: ``my_Button.set_size(300, 200)``

    :example description: Set the width of the my_Button control to 300 and the height to 200

.. function:: common_object.get_size()

    :description: Obtains the size of the control

    :param void: None

    :return: [w,h], which represents the size of the control

    :example: ``size = my_Button.get_size()``

    :example description: Obtain the size of the my_Button control and assign it to the size variable, which is a list

.. function:: common_object.set_rotation(degree)

    :description: Sets the rotation angle of the control

    :param int degree: The rotation angle of the control, whose range is [0, 360]. A positive value indicates clockwise rotation, and a negative value indicates counterclockwise rotation.

    :return: None

    :example: ``my_Button.set_rotation(90)``

    :example description: Set the my_Button control to rotate 90 degrees clockwise

.. function:: common_object.get_rotation()

    :description: Obtains the rotation angle of the control

    :param void: None

    :return: An int value, which indicates the rotation angle of the control, whose range is [0, 360]. A positive value indicates clockwise rotation, and a negative value indicates counterclockwise rotation.

    :example: ``degree = my_Button.get_rotation()``

    :example description: Obtain the rotation angle of the my_Button control and assign it to the degree variable

.. function:: common_object.set_privot(x, y)

    :description: Sets the anchor coordinates of the control, where the input parameter is a normalized parameter. The origin is at the lower-left corner of the control. The anchor point of the control defaults to the center of the control, that is (0.5, 0.5). The position and rotation of the control are controlled by the anchor point.

    :param int x: The x-coordinate of the anchor point, whose range is [0, 1]. Rightward is the positive direction.
    :param int y: The y-coordinate of the anchor point, whose range is [0, 1]. Upward is the positive direction.

    :return: None

    :example: ``my_Button.set_privot(0, 1)``

    :example description: Set the anchor point of the control to the upper-left corner of the control

.. function:: common_object.get_privot()

    :description: Obtains the anchor coordinates of the control

    :param void: None

    :return: [x,y], which represents the anchor coordinates of the control

    :example: ``privot = my_Button.get_privot()``

    :example description: Obtain the anchor coordinates of the control and assign them to the privot variable, which is a list

.. function:: common_object.set_order(order)

    :description: Sets the display priority of the control. If multiple controls overlap with each other, the control with higher priority is in the upper layer. The greater the display priority value, the higher the priority.

    :param int order: The specified priority of the control. If multiple controls overlap with each other, the control with higher priority is displayed first.

    :return: None

    :example: ``my_Button.set_order(8)``

    :example description: Set the display priority of the control to 8. When multiple controls overlap, the controls with priority values lower than this priority value are covered.

.. function:: common_object.get_order()

    :description: Obtains the display priority value of the control

    :param void: None

    :return: An int value, which indicates the display priority value of the control

    :example: ``order = my_Button.get_order()``

    :example description: Obtain the display priority value of the my_Button control and assign it to the order variable

.. function:: common_object.callback_register(event, callback)

    :description: The callback function triggered by the registered control event. When the control detects this event, the registered callback function is executed.

    :param string event: Specify the trigger event of the callback function

        The events that can be registered for each control are described as follows:

        * The Button control:
            - ``on_click``: Trigger this event when the button is released in the process of pressing and releasing the button once
            - ``on_press_down``: Trigger this event when the button is pressed
            - ``on_press_up``: Trigger this event when the button is released

        * The Toggle control:
            - Trigger this event when the value of ``on_value_changed`` changes. The args parameter in the callback function is a boolean value, which is the updated value of the Toggle control.

        * The Dropdown control:
            - Trigger this event when the value of ``on_value_changed`` changes. The args parameter in the callback function is an int value, which is the selected index entry after the value of the Toggle control changes.

        * The Text control:
            - No trigger events are available. 

        * The InputField control:
            - Trigger this event when the value of ``on_value_changed`` changes. The args parameter in the callback function is a string, which is the updated value of the InputField control.

    :param function callback: The callback function that needs to be registered. The unified signature of callback functions is ``def callback(widget,*args,**kw):``, where widget is the reference to the control that triggered the event, and args and kw are parameters.

    :return: None

    :example 1: 

.. code-block:: python
    :linenos:

    # When the my_Button control is clicked, the information will be output to the console, and the robot will shoot once.

    def button_callback(widget,*args,**kw):
        print('the button is clicked and the button's name is '+ widget.get_name())
        gun_ctrl.fire_once()
    my_Button.callback_register('on_click',button_callback)
..

    :example 2: 

.. code-block:: python
    :linenos:

    # When the my_Toggle control is clicked, the value of the control changes, the information is output to the console, and the robot will play a sound.

    def toggle_callback(widget,*args,**kw):
        print("the toggle's value is changed and the toggle's name is "+ widget.get_name())
        print("the toggle's value now is "+ str(args))
        media_ctrl.play_sound(rm_define.media_sound_recognize_success)
    my_Toggle.callback_register('on_value_changed',toggle_callback)
..

 :example 3: 

.. code-block:: python
    :linenos:

    # When you click the my_Dropdown control to change its selected value, the value changes, the information is output to the console, and the robot will play a sound.

    def dropdown_callback(widget,*args,**kw):
        print("the dropdown's value is changed and the dropdown's name is "+ widget.get_name())
        print("the dropdown's value now is "+ str(args))
        media_ctrl.play_sound(rm_define.media_sound_solmization_1A)
    my_Dropdown.callback_register('on_value_changed',dropdown_callback)
..

    :example 4: 

.. code-block:: python
    :linenos:

    # When you click the my_InputField control to change its selected value, the value changes, and the information is output to the console.

    def input_field_callback(widget,*args,**kw):
        print("the input_field's value is changed and the input_field's name is "+ widget.get_name())
        print("the input_field's value now is "+ str(args))
    my_InputField.callback_register('on_value_changed',input_field_callback)

