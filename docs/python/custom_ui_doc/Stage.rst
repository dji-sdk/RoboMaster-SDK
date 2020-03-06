=================
Stage
=================

As the system initializes, it automatically creates a Stage class object stage, which can be used directly, and does not need to be created by the user.

.. function:: object.add_widget(widget_obj)

    :Description: Add controls from parameters to the UI

    :param object widget_obj: The control object to be added to the UI

    :return: None

    :Example: 
.. code-block:: python
    :linenos:

    #Create a Button object and add it to the UI

    my_button = Button()
    stage.add_widget(my_button)

.. function:: stage_object.remove_widget(widget_obj)

    :Description: Remove the control passed in by the parameter from the UI 

    :param object widget_obj: The control that needs to be removed from the UI

    :return: N/A

    :Example: ``stage.remove_widget(my_button)``

    :Example description: Remove the my_button control from the UI 

