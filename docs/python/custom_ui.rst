===================
Custom UI System
===================

Summary
-----------

The custom UI system is a way for users to expand the input and output of programs. Users compose their own programs to generate user-defined UI controls.

A very important part of our programming work is to process inputs and outputs. For our robot, the program output can be the action of the chassis, gimbal, water gun, and other modules, or the performance of light and sound effects. Input includes initial variables, the visual recognition of the robot, applause recognition, armor plate attack detection, and cell phone gyroscope, among others. We can now achieve the purpose of input through the interaction between the custom UI system and the generated UI control, or output the processing results of the program through UI controls.

We can compose a Python program in the RoboMaster app to generate UI controls and bind the event callback of the controls by calling the relevant interface of the custom UI system. After composing and debugging the program in the laboratory, we may assemble it into custom skills, which can be used in solo practice or multi-player competitions.

Interfaces
----------

.. toctree::
    :maxdepth: 1
    :caption: Common

    custom_ui_doc/Common.rst

.. toctree::
    :maxdepth: 1
    :caption: Stage

    custom_ui_doc/Stage.rst

.. toctree::
    :maxdepth: 1
    :caption: Button

    custom_ui_doc/Button.rst

.. toctree::
    :maxdepth: 1
    :caption: Toggle

    custom_ui_doc/Toggle.rst

.. toctree::
    :maxdepth: 1
    :caption: Text

    custom_ui_doc/Text.rst

.. toctree::
    :maxdepth: 1
    :caption: InputField

    custom_ui_doc/Input_field.rst

.. toctree::
    :maxdepth: 1
    :caption: Dropdown

    custom_ui_doc/Dropdown.rst
