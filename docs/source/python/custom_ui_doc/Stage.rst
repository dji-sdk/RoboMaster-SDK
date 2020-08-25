=================
Stage
=================

系统初始化时会自动创建一个 Stage 类的对象 stage ，直接使用即可，不需要用户自己创建。

.. function:: stage.add_widget(widget_obj)

    :描述: 将参数中的控件添加到 UI 界面中

    :param object widget_obj: 需要添加进 UI 界面的控件对象

    :return: 无

    :示例: 
.. code-block:: python
    :linenos:

    #创建一个 Button 对象，并将其添加进 UI 界面

    my_button = Button()
    stage.add_widget(my_button)

.. function:: stage.remove_widget(widget_obj)

    :描述: 从 UI 界面移除参数传入的控件 

    :param object widget_obj: 需要从 UI 界面移除的控件

    :return: 无

    :示例: ``stage.remove_widget(my_button)``

    :示例说明: 从 UI 界面中移除控件 my_button 