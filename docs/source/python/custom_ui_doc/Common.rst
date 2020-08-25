=================
Common
=================

本部分方法适用于除 Stage 外所有自定义 UI 控件，因此单独拿出来介绍。

.. function:: common_object.set_active(status)

    :描述: 控制当前控件是否显示 

    :param bool status: 控件的活动状态，True 表示显示当前控件，False 表示隐藏当前控件

    :return: 无

    :示例: ``my_Slider.set_active(Flase)``

    :示例说明: 设置 my_Slider 控件为隐藏状态

.. function:: common_object.get_active()

    :描述: 获取当前控件的显示状态 

    :param void: 无

    :return: bool, 表示控件的显示状态

    :示例: ``status = my_Slider.get_active()``

    :示例说明: 获取 my_Slider 控件的显示状态，赋值给 status 变量

.. function:: common_object.set_name(name)

    :描述: 设置当前控件的名字

    :param string name: 控件的名字

    :return: 无

    :示例: ``my_Dropdown.set_name('my_dropdown')``

    :示例说明: 设置 my_Dropdown 控件的名字为『my_dropdown』

.. function:: common_object.get_name()

    :描述: 获取当前控件的名字

    :param void: 无

    :return: string，表示控件的名字

    :示例: ``name = my_Dropdown.get_name()``

    :示例说明: 获取 my_Dropdown 控件的名字，赋值给 name 变量

.. function:: common_object.set_position(x, y)

    :描述: 设置控件的位置坐标，原点在屏幕的中心位置

    :param int x: 控件的横坐标，取值为屏幕上实际像素的位置，0 点在屏幕水平中心位置，向右为正方向
    :param int y: 控件的纵坐标，取值为屏幕上实际像素的位置，0 点在屏幕垂直中心位置，向上为正方向

    :return: 无

    :示例: ``my_Text.set_position(-200, 500)``

    :示例说明: 设置 my_Text 控件的坐标为 (-200，500)

.. function:: common_object.get_position()

    :描述: 获取控件的位置坐标

    :param void: 无

    :return: [x,y]，表示控件的位置

    :示例: ``pos = my_Text.get_position()``

    :示例说明: 获取 my_Text 控件的位置，赋值给变量 pos，pos 为一个列表

.. function:: common_object.set_size(w, h)

    :描述: 设置控件的大小

    :param int w: 控件的宽度
    :param int h: 控件的高度

    :return: 无

    :示例: ``my_Button.set_size(300, 200)``

    :示例说明: 设置 my_Button 控件的宽度为 300，高度为 200

.. function:: common_object.get_size()

    :描述: 获取控件的大小

    :param void: 无

    :return: [w,h], 表示控件的大小

    :示例: ``size = my_Button.get_size()``

    :示例说明: 获取 my_Button 控件的大小，赋值给变量 size，size 为一个列表

.. function:: common_object.set_rotation(degree)

    :描述: 设置控件的旋转角度

    :param int degree: 控件的旋转角度，范围为 [0, 360]，正值为顺时针旋转，负值为逆时针旋转

    :return: 无

    :示例: ``my_Button.set_rotation(90)``

    :示例说明: 设置 my_Button 控件顺时针旋转 90 度

.. function:: common_object.get_rotation()

    :描述: 获取控件的旋转角度

    :param void: 无

    :return: int, 表示控件的旋转角度，范围为 [0, 360]，正值为顺时针旋转，负值为逆时针旋转

    :示例: ``degree = my_Button.get_rotation()``

    :示例说明: 获取 my_Button 控件的旋转角度，赋值给变量 degree

.. function:: common_object.set_privot(x, y)

    :描述: 设置控件的锚点坐标，输入参数是归一化参数，原点位于控件的左下角，控件的锚点默认为控件中心即 (0.5,0.5)，控件的位置和旋转均以锚点作为控制点

    :param int x: 锚点的 x 坐标，范围为 [0, 1]，向右为正方向
    :param int y: 锚点的 y 坐标，范围为 [0, 1]，向上为正方向

    :return: 无

    :示例: ``my_Button.set_privot(0, 1)``

    :示例说明: 设置控件的锚点为控件的左上角

.. function:: common_object.get_privot()

    :描述: 获取控件的锚点坐标

    :param void: 无

    :return: [x,y]，表示控件的锚点坐标

    :示例: ``privot = my_Button.get_privot()``

    :示例说明: 获取控件的锚点坐标，赋值给变量 privot，privot 为一个列表

.. function:: common_object.set_order(order)

    :描述: 设置控件的显示优先级，当多个控件重叠时，优先级高的控件在上层，数字越大优先级越高

    :param int order: 控件的指定优先级，控件重叠时优先级高的优先显示

    :return: 无

    :示例: ``my_Button.set_order(8)``

    :示例说明: 将控件的显示优先级设置为 8，当控件重叠时，低于此优先级的控件将被覆盖

.. function:: common_object.get_order()

    :描述: 获取控件的显示优先级

    :param void: 无

    :return: int，表示控件的显示优先级

    :示例: ``order = my_Button.get_order()``

    :示例说明: 获取 my_Button 控件的显示优先级，赋值给变量 order

.. function:: common_object.callback_register(event, callback)

    :描述: 注册控件事件触发的回调函数，当控件检测到相应的事件后，执行注册的回调函数

    :param string event: 指定回调函数的触发事件

        各控件可注册的事件如下：

        * Button 控件：
            - ``on_click`` 一次按下松开按钮的过程, 在松开按钮的时候触发该事件
            - ``on_press_down`` 按下按钮的时候触发该事件
            - ``on_press_up`` 松开按钮的时候触发该事件

        * Toggle 控件：
            - ``on_value_changed`` 值发生改变的时候触发该事件，回调函数中的 args 参数为 bool，表示该 Toggle 控件值发生改变后的值

        * Dropdown 控件：
            - ``on_value_changed`` 值发生改变的时候触发该事件，回调函数中的 args 参数为 int，表示该 Dropdown 控件值发生改变后的选中索引

        * Text 控件：
            - 无触发事件 

        * InputField 控件：
            - ``on_value_changed`` 值发生改变的时候触发该事件，回调函数中的 args 参数为 string，表示该 InputField 控件值发生改变后的值

    :param function callback: 需要注册的回调函数，回调函数的统一签名为： ``def callback(widget,*args,**kw):`` ，其中 widget 为触发事件的控件引用，args，kw为参数.

    :return: 无

    :示例 1: 

.. code-block:: python
    :linenos:

    # 当 my_Button 控件被点击后，打印信息到控制台上，机器人会开枪射击一次

    def button_callback(widget,*args,**kw):
        print('the button is clicked and the button's name is '+ widget.get_name())
        gun_ctrl.fire_once()
    my_Button.callback_register('on_click',button_callback)
..

    :示例 2: 

.. code-block:: python
    :linenos:

    # 当 my_Toggle 控件被点击后，值会发生改变，打印信息到控制台上，机器人会播放声音

    def toggle_callback(widget,*args,**kw):
        print("the toggle's value is changed and the toggle's name is "+ widget.get_name())
        print("the toggle's value now is "+ str(args))
        media_ctrl.play_sound(rm_define.media_sound_recognize_success)
    my_Toggle.callback_register('on_value_changed',toggle_callback)
..

 :示例 3: 

.. code-block:: python
    :linenos:

    # 当点击 my_Dropdown 控件改变其选中的值，值会发生改变，打印信息到控制台上，机器人会播放声音

    def dropdown_callback(widget,*args,**kw):
        print("the dropdown's value is changed and the dropdown's name is "+ widget.get_name())
        print("the dropdown's value now is "+ str(args))
        media_ctrl.play_sound(rm_define.media_sound_solmization_1A)
    my_Dropdown.callback_register('on_value_changed',dropdown_callback)
..

    :示例 4: 

.. code-block:: python
    :linenos:

    # 当点击 my_InputField 控件改变其选中的值，值会发生改变，打印信息到控制台上

    def input_field_callback(widget,*args,**kw):
        print("the input_field's value is changed and the input_field's name is "+ widget.get_name())
        print("the input_field's value now is "+ str(args))
    my_InputField.callback_register('on_value_changed',input_field_callback)

