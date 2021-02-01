=================
Common
=================

本部分方法適用於除 Stage 外所有自定義 UI 控件，因此單獨拿出來介紹。

.. function:: common_object.set_active(status)

    :描述: 控制當前控件是否顯示 

    :param bool status: 控件的活動狀態，True 表示顯示當前控件，False 表示隱藏當前控件

    :return: 無

    :示例: ``my_Slider.set_active(Flase)``

    :示例說明: 設置 my_Slider 控件為隱藏狀態

.. function:: common_object.get_active()

    :描述: 獲取當前控件的顯示狀態 

    :param void: 無

    :return: bool, 表示控件的顯示狀態

    :示例: ``status = my_Slider.get_active()``

    :示例說明: 獲取 my_Slider 控件的顯示狀態，賦值給 status 變量

.. function:: common_object.set_name(name)

    :描述: 設置當前控件的名字

    :param string name: 控件的名字

    :return: 無

    :示例: ``my_Dropdown.set_name('my_dropdown')``

    :示例說明: 設置 my_Dropdown 控件的名字為『my_dropdown』

.. function:: common_object.get_name()

    :描述: 獲取當前控件的名字

    :param void: 無

    :return: string，表示控件的名字

    :示例: ``name = my_Dropdown.get_name()``

    :示例說明: 獲取 my_Dropdown 控件的名字，賦值給 name 變量

.. function:: common_object.set_position(x, y)

    :描述: 設置控件的位置坐標，原點在屏幕的中心位置

    :param int x: 控件的橫坐標，取值為屏幕上實際像素的位置，0 點在屏幕水平中心位置，向右為正方向
    :param int y: 控件的縱坐標，取值為屏幕上實際像素的位置，0 點在屏幕垂直中心位置，向上為正方向

    :return: 無

    :示例: ``my_Text.set_position(-200, 500)``

    :示例說明: 設置 my_Text 控件的坐標為 (-200，500)

.. function:: common_object.get_position()

    :描述: 獲取控件的位置坐標

    :param void: 無

    :return: [x,y]，表示控件的位置

    :示例: ``pos = my_Text.get_position()``

    :示例說明: 獲取 my_Text 控件的位置，賦值給變量 pos，pos 為一個列表

.. function:: common_object.set_size(w, h)

    :描述: 設置控件的大小

    :param int w: 控件的寬度
    :param int h: 控件的高度

    :return: 無

    :示例: ``my_Button.set_size(300, 200)``

    :示例說明: 設置 my_Button 控件的寬度為 300，高度為 200

.. function:: common_object.get_size()

    :描述: 獲取控件的大小

    :param void: 無

    :return: [w,h], 表示控件的大小

    :示例: ``size = my_Button.get_size()``

    :示例說明: 獲取 my_Button 控件的大小，賦值給變量 size，size 為一個列表

.. function:: common_object.set_rotation(degree)

    :描述: 設置控件的旋轉角度

    :param int degree: 控件的旋轉角度，範圍為 [0, 360]，正值為順時針旋轉，負值為逆時針旋轉

    :return: 無

    :示例: ``my_Button.set_rotation(90)``

    :示例說明: 設置 my_Button 控件順時針旋轉 90 度

.. function:: common_object.get_rotation()

    :描述: 獲取控件的旋轉角度

    :param void: 無

    :return: int, 表示控件的旋轉角度，範圍為 [0, 360]，正值為順時針旋轉，負值為逆時針旋轉

    :示例: ``degree = my_Button.get_rotation()``

    :示例說明: 獲取 my_Button 控件的旋轉角度，賦值給變量 degree

.. function:: common_object.set_privot(x, y)

    :描述: 設置控件的錨點坐標，輸入參數是歸一化參數，原點位於控件的左下角，控件的錨點默認為控件中心即 (0.5,0.5)，控件的位置和旋轉均以錨點作為控制點

    :param int x: 錨點的 x 坐標，範圍為 [0, 1]，向右為正方向
    :param int y: 錨點的 y 坐標，範圍為 [0, 1]，向上為正方向

    :return: 無

    :示例: ``my_Button.set_privot(0, 1)``

    :示例說明: 設置控件的錨點為控件的左上角

.. function:: common_object.get_privot()

    :描述: 獲取控件的錨點坐標

    :param void: 無

    :return: [x,y]，表示控件的錨點坐標

    :示例: ``privot = my_Button.get_privot()``

    :示例說明: 獲取控件的錨點坐標，賦值給變量 privot，privot 為一個列表

.. function:: common_object.set_order(order)

    :描述: 設置控件的顯示優先級，當多個控件重疊時，優先級高的控件在上層，數字越大優先級越高

    :param int order: 控件的指定優先級，控件重疊時優先級高的優先顯示

    :return: 無

    :示例: ``my_Button.set_order(8)``

    :示例說明: 將控件的顯示優先級設置為 8，當控件重疊時，低於此優先級的控件將被覆蓋

.. function:: common_object.get_order()

    :描述: 獲取控件的顯示優先級

    :param void: 無

    :return: int，表示控件的顯示優先級

    :示例: ``order = my_Button.get_order()``

    :示例說明: 獲取 my_Button 控件的顯示優先級，賦值給變量 order

.. function:: common_object.callback_register(event, callback)

    :描述: 註冊控件事件觸發的回調函數，當控件檢測到相應的事件後，執行註冊的回調函數

    :param string event: 指定回調函數的觸發事件

        各控件可註冊的事件如下：

        * Button 控件：
            - ``on_click`` 一次按下鬆開按鈕的過程, 在鬆開按鈕的時候觸發該事件
            - ``on_press_down`` 按下按鈕的時候觸發該事件
            - ``on_press_up`` 鬆開按鈕的時候觸發該事件

        * Toggle 控件：
            - ``on_value_changed`` 值發生改變的時候觸發該事件，回調函數中的 args 參數為 bool，表示該 Toggle 控件值發生改變後的值

        * Dropdown 控件：
            - ``on_value_changed`` 值發生改變的時候觸發該事件，回調函數中的 args 參數為 int，表示該 Dropdown 控件值發生改變後的選中索引

        * Text 控件：
            - 無觸發事件 

        * InputField 控件：
            - ``on_value_changed`` 值發生改變的時候觸發該事件，回調函數中的 args 參數為 string，表示該 InputField 控件值發生改變後的值

    :param function callback: 需要註冊的回調函數，回調函數的統一簽名為： ``def callback(widget,*args,**kw):`` ，其中 widget 為觸發事件的控件引用，args，kw為參數.

    :return: 無

    :示例 1: 

.. code-block:: python
    :linenos:

    # 當 my_Button 控件被點擊後，打印信息到控制台上，機器人會開槍射擊一次

    def button_callback(widget,*args,**kw):
        print('the button is clicked and the button's name is '+ widget.get_name())
        gun_ctrl.fire_once()
    my_Button.callback_register('on_click',button_callback)
..

    :示例 2: 

.. code-block:: python
    :linenos:

    # 當 my_Toggle 控件被點擊後，值會發生改變，打印信息到控制台上，機器人會播放聲音

    def toggle_callback(widget,*args,**kw):
        print("the toggle's value is changed and the toggle's name is "+ widget.get_name())
        print("the toggle's value now is "+ str(args))
        media_ctrl.play_sound(rm_define.media_sound_recognize_success)
    my_Toggle.callback_register('on_value_changed',toggle_callback)
..

 :示例 3: 

.. code-block:: python
    :linenos:

    # 當點擊 my_Dropdown 控件改變其選中的值，值會發生改變，打印信息到控制台上，機器人會播放聲音

    def dropdown_callback(widget,*args,**kw):
        print("the dropdown's value is changed and the dropdown's name is "+ widget.get_name())
        print("the dropdown's value now is "+ str(args))
        media_ctrl.play_sound(rm_define.media_sound_solmization_1A)
    my_Dropdown.callback_register('on_value_changed',dropdown_callback)
..

    :示例 4: 

.. code-block:: python
    :linenos:

    # 當點擊 my_InputField 控件改變其選中的值，值會發生改變，打印信息到控制台上

    def input_field_callback(widget,*args,**kw):
        print("the input_field's value is changed and the input_field's name is "+ widget.get_name())
        print("the input_field's value now is "+ str(args))
    my_InputField.callback_register('on_value_changed',input_field_callback)

