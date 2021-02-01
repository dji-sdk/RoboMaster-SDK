.. _beginnger:

####################################
RoboMaster SDK 新手入門 - 基礎篇
####################################

SDK 能做什麼?
_____________

RoboMaster SDK （以下簡稱 SDK）是一套面向大疆 RoboMaster 系列產品的開發工具包，
目前支持的產品包括 RoboMaster EP, RoboMaster EP Core, Tello EDU, Tello Talent 等。
通過 SDK， 用戶可以實現在PC上控制機器人運動以及獲取機器人傳感器的相關信息 （待補充？？？）

第一個SDK程序
_____________

接下來本文檔將從如何獲取 RoboMaster SDK（以下簡稱 SDK）的版本號來編寫第一個 SDK 程序

- 首先從安裝的的 `robomaster` 包中導入自己需要的模塊，這裡我們導入包含獲取SDK版本信息的 `version` 模塊::

    from robomaster import version

- 接下來通過 `version` 模塊中的 `__version__` 屬性可以獲得 SDK 的版本號，並將其打印::

    sdk_version = version.__version__
    print("sdk version:", sdk_version)

-  運行程序，可以看到打印的結果::

    sdk version: 0.1.1.29

示例文檔中提供了獲取 SDK 版本號的例程 :file:`/examples/00_general/01_sdk_version.py`

.. literalinclude:: ./../../../examples/00_general/01_sdk_version.py
   :language: python
   :linenos:
   :lines: 17-
