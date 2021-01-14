=================
Stage
=================

When the system is initialized, a stage object of the Stage class is automatically created, which can be used directly without the need for users to create it themselves.

.. function:: stage.add_widget(widget_obj)

    :description: Adds the controls in the parameter to the UI

    :param object widget_obj: Control objects to be added to the UI

    :return: None

    :example: 
.. code-block:: python
    :linenos:

    #Create a Button object and add it to the UI

    my_button = Button()
    stage.add_widget(my_button)

.. function:: stage.remove_widget(widget_obj)

    :description: Removes the controls of the parameter from the UI 

    :param object widget_obj: The controls that need to be removed from the UI

    :return: None

    :example: ``stage.remove_widget(my_button)``

    :example description: Remove the my_button control from the UI 