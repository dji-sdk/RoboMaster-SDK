===================
自定义 UI 系统
===================

简介
-----------

自定义 UI 系统是用户通过自己编写的程序生成自定义的 UI 控件来拓展程序的输入和输出的一种方式。

我们编程时很重要的一部分工作是处理输入和输出，对我们的机器人来说，程序输出可以是底盘、云台、水弹枪等模块的动作，也可以是灯光、音效等的表现，输入的途径则有初始的变量，机器人的视觉识别、掌声识别、装甲板打击检测，手机陀螺仪等。现在我们可以通过自定义 UI 系统与生成的的 UI 控件进行交互达到输入的目的，也可以将程序的处理结果通过 UI 控件来进行信息的输出。

我们可以在 RoboMaster app 中编写 Python 程序，调用自定义 UI 系统的相关接口，来生成 UI 控件，绑定控件的事件回调。在实验室中完成程序的编写和调试后，可以将程序装配成自定义技能，在单机驾驶或者多人竞技中释放出来。

接口
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