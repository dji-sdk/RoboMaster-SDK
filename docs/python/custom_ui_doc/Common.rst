=================
Common
=================

本部分方法適用於除 Stage 外所有自訂 UI 控制項，因此單獨介紹。

.. function:: common_object.set_active(status)

    :描述: 控制當前控制項是否顯示 

    :param bool status: 控制項的活動狀態，True 表示顯示當前控制項，False 表示隱藏當前控制項

    :return: 無

    :示例: ``my_Slider.set_active(Flase)``

    :示例說明: 設定 my_Slider 控制項為隱藏狀態

.. function:: common_object.get_active()

    :描述: 獲取當前控制項的顯示狀態 

    :param void: 無

    :return: bool, 表示控制項的顯示狀態

    :示例: ``status = my_Slider.get_active()``

    :示例說明: 獲取 my_Slider 控制項的顯示狀態，賦值給 status 變數

.. function:: common_object.set_name(name)

    :描述: 設定當前控制項的名字

    :param string name: 控制項的名字

    :return: 無

    :示例: ``my_Dropdown.set_name('my_dropdown')``

    :示例說明: 設定 my_Dropdown 控制項的名字為『my_dropdown』

.. function:: common_object.get_name()

    :描述: 獲取當前控制項的名字

    :param void: 無

    :return: string，表示控制項的名字

    :示例: ``name = my_Dropdown.get_name()``

    :示例說明: 獲取 my_Dropdown 控制項的名字，賦值給 name 變數

.. function:: common_object.set_position(x, y)

    :描述: 設定控制項的位置座標，原點在螢幕的中心位置

    :param int x: 控制項的橫坐標，取值為螢幕上實際像素的位置，0 點在螢幕水平中心位置，向右為正方向
    :param int y: 控制項的縱坐標，取值為螢幕上實際像素的位置，0 點在螢幕垂直中心位置，向上為正方向

    :return: 無

    :示例: ``my_Text.set_position(-200, 500)``

    :示例說明: 設定 my_Text 控制項的座標為（-200，500）

.. function:: common_object.get_position()

    :描述: 獲取控制項的位置座標

    :param void: 無

    :return: [x,y]，表示控制項的位置

    :示例: ``pos = my_Text.get_position()``

    :示例說明: 獲取 my_Text 控制項的位置，賦值給變數 pos，pos 為一個列表

.. function:: common_object.set_size(w, h)

    :描述: 設定控制項的大小

    :param int w: 控制項的寬度
    :param int h: 控制項的高度

    :return: 無

    :示例: ``my_Button.set_size(300, 200)``

    :示例說明: 設定 my_Button 控制項的寬度為 300，高度為 200

.. function:: common_object.get_size()

    :描述: 獲取控制項的大小

    :param void: 無

    :return: [w,h], 表示控制項的大小

    :示例: ``size = my_Button.get_size()``

    :示例說明: 獲取 my_Button 控制項的大小，賦值給變數 size，size 為一個列表

.. function:: common_object.set_rotation(degree)

    :描述: 設定控制項的旋轉角度

    :param int degree: 控制項的旋轉角度，範圍為 [0, 360]，正值為順時針旋轉，負值為逆時針旋轉

    :return: 無

    :示例: ``my_Button.set_rotation(90)``

    :示例說明: 設定 my_Button 控制項順時針旋轉 90 度

.. function:: common_object.get_rotation()

    :描述: 獲取控制項的旋轉角度

    :param void: 無

    :return: int, 表示控制項的旋轉角度，範圍為 [0, 360]，正值為順時針旋轉，負值為逆時針旋轉

    :示例: ``degree = my_Button.get_rotation()``

    :示例說明: 獲取 my_Button 控制項的旋轉角度，賦值給變數 degree

.. function:: common_object.set_privot(x, y)

    :描述: 設定控制項的錨點座標，輸入參數是歸一化參數，原點位於控制項的左下角，控制項的錨點預設為控制項中心即（0.5, 0.5），控制項的位置和旋轉均以錨點作為控制點

    :param int x: 錨點的 x 座標，範圍為 [0, 1]，向右為正方向
    :param int y: 錨點的 y 座標，範圍為 [0, 1]，向上為正方向

    :return: 無

    :示例: ``my_Button.set_privot(0, 1)``

    :示例說明: 設定控制項的錨點為控制項的左上角

.. function:: common_object.get_privot()

    :描述: 獲取控制項的錨點座標

    :param void: 無

    :return: [x,y]，表示控制項的錨點座標

    :示例: ``privot = my_Button.get_privot()``

    :示例說明: 獲取控制項的錨點座標，賦值給變數 privot，privot 為一個列表

.. function:: common_object.set_order(order)

    :描述: 設定控制項的顯示優先順序，當多個控制項重疊時，優先順序高的控制項在上層，數字越大優先順序越高

    :param int order: 控制項的指定優先順序，控制項重疊時優先順序高的優先顯示

    :return: 無

    :示例: ``my_Button.set_order(8)``

    :示例說明: 將控制項的顯示優先順序設定為 8，當控制項重疊時，低於此優先順序的控制項將被覆蓋

.. function:: common_object.get_order()

    :描述: 獲取控制項的顯示優先順序

    :param void: 無

    :return: int，表示控制項的顯示優先順序

    :示例: ``order = my_Button.get_order()``

    :示例說明: 獲取 my_Button 控制項的顯示優先順序，賦值給變數 order

.. function:: common_object.callback_register(event, callback)

    :描述: 註冊控制項事件觸發的回呼函數，當控制項檢測到相應的事件後，執行註冊的回呼函數

    :param string event: 指定回呼函數的觸發事件

各控制項可註冊的事件如下: 

    * Button 控制項：
        - ``on_click`` 一次按下鬆開按鈕的過程，在鬆開按鈕時觸發該事件
        - ``on_press_down`` 按下按鈕時觸發該事件
        - ``on_press_up`` 鬆開按鈕時觸發該事件

    * Toggle 控制項：
        - ``on_value_changed`` 值發生改變時觸發該事件，回呼函數中的 args 參數為bool，表示該 Toggle 控制項值發生改變後的值
    * Dropdown 控制項：
        - ``on_value_changed`` 值發生改變時觸發該事件，回呼函數中的 args 參數為int，表示該 Dropdown 控制項值發生改變後的選中索引

    * Text 控制項：
        - 無觸發事件

    * InputField 控制項：
        - ``on_value_changed`` 值發生改變的時候觸發該事件，回呼函數中的 args 參數為 string，表示該 InputField 控制項值發生改變後的值

    :param function callback: 需要註冊的回呼函數，回呼函數的統一簽名為: ``def callback(widget,*args,**kw):``，其中 widget 為觸發事件的控制項引用，args 為擴充參數

    :return: 無

    :示例 1: 

.. code-block:: python
    :linenos:

    # 當 my_Button 控制項被點擊後，將資訊列印到控制台上，機器人會開槍射擊一次

    def button_callback(widget,*args,**kw):
        print("the button is clicked and the button's name is "+ widget.get_name())
        gun_ctrl.fire_once()
    my_Button.callback_register('on_click',button_callback)
..

    :示例 2: 

.. code-block:: python
    :linenos:

    # 當 my_Toggle 控制項被點擊後，值會發生改變，將資訊列印到控制台上，機器人會播放聲音

    def toggle_callback(widget,*args,**kw):
        print("the toggle's value is changed and the toggle's name is "+ widget.get_name())
        print("the toggle's value now is "+ str(args))
        media_ctrl.play_sound(rm_define.media_sound_recognize_success)
    my_Toggle.callback_register('on_value_changed',toggle_callback)
..

 :示例 3: 

.. code-block:: python
    :linenos:

    # 當點擊 my_Dropdown 控制項改變其選中的值，值會發生改變，將資訊列印到控制台上，機器人會播放聲音

    def dropdown_callback(widget,*args,**kw):
        print("the dropdown's value is changed and the dropdown's name is "+ widget.get_name())
        print("the dropdown's value now is "+ str(args))
        media_ctrl.play_sound(rm_define.media_sound_solmization_1A)
    my_Dropdown.callback_register('on_value_changed',dropdown_callback)
..

    :示例 4: 

.. code-block:: python
    :linenos:

    # 當點擊 my_InputField 控制項改變其選中的值，值會發生改變，將資訊列印到控制台上

    def input_field_callback(widget,*args,**kw):
        print("the input_field's value is changed and the input_field's name is "+ widget.get_name())
        print("the input_field's value now is "+ str(args))
    my_InputField.callback_register('on_value_changed',input_field_callback)

