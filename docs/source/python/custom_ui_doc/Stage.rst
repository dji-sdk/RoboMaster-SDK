=================
Stage
=================

系統初始化時會自動創建一個 Stage 類的對象 stage ，直接使用即可，不需要用戶自己創建。

.. function:: stage.add_widget(widget_obj)

    :描述: 將參數中的控件添加到 UI 界面中

    :param object widget_obj: 需要添加進 UI 界面的控件對像

    :return: 無

    :示例: 
.. code-block:: python
    :linenos:

    #創建一個 Button 對象，並將其添加進 UI 界面

    my_button = Button()
    stage.add_widget(my_button)

.. function:: stage.remove_widget(widget_obj)

    :描述: 從 UI 界面移除參數傳入的控件 

    :param object widget_obj: 需要從 UI 界面移除的控件

    :return: 無

    :示例: ``stage.remove_widget(my_button)``

    :示例說明: 從 UI 界面中移除控件 my_button 