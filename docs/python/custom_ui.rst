===================
自訂 UI 系統
===================

簡介
-----------

自訂 UI 系統是使用者通過自己編寫的程式生成自訂的 UI 控制項來拓展程式的輸入和輸出的一種方式。

我們設計程式時很重要的一部分工作是處理輸入和輸出，對我們的機器人來說，程式輸出可以是底盤、雲台、水彈槍等模組的動作，也可以是燈光、音效等的表現，輸入的途徑則有初始的變數，機器人的視覺識別、掌聲識別、裝甲板擊打檢測，手機陀螺儀等。現在我們可以通過自訂 UI 系統與生成的的 UI 控制項進行交互達到輸入的目的，也可以將程式的處理結果通過 UI 控制項來進行資訊的輸出。

我們可以在 RoboMaster app 中編寫 Python 程式，調用自訂 UI 系統的相關接口，來生成 UI 控制項，綁定控制項的事件回檔。在實驗室中完成程式的編寫和調試後，可以將程式裝配成自訂技能，在單機駕駛或者多人競技中釋放出來。

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