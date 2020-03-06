=================
Stage
=================

系統初始化時會自動創建一個 Stage 類的對象 stage，直接使用即可，無需使用者自行創建。

.. function:: object.add_widget(widget_obj)

    :描述: 將參數中的控制項添加至 UI 介面中

    :param object widget_obj: 需要加入 UI 介面的控制項對象

    :return: 無

    :示例: 
.. code-block:: python
    :linenos:

    #創建一個 Button 物件，並將其加入 UI 介面

    my_button = Button()
    stage.add_widget(my_button)

.. function:: stage_object.remove_widget(widget_obj)

    :描述: 從 UI 介面移除參數傳入的控制項

    :param object widget_obj: 需從 UI 介面移除的控制項

    :return: 無

    :示例: ``stage.remove_widget(my_button)``

    :示例說明: 從 UI 介面中移除控制項 my_button 