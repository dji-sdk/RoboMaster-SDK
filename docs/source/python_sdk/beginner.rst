.. _beginnger:

####################################
RoboMaster SDK 新手入门 - 基础篇
####################################

SDK 能做什么?
_____________

RoboMaster SDK （以下简称 SDK）是一套面向大疆 RoboMaster 系列产品的开发工具包，
目前支持的产品包括 RoboMaster EP, RoboMaster EP Core, Tello EDU, Tello Talent 等。
通过 SDK， 用户可以实现在PC上控制机器人运动以及获取机器人传感器的相关信息 （待补充？？？）

第一个SDK程序
_____________

接下来本文档将从如何获取 RoboMaster SDK（以下简称 SDK）的版本号来编写第一个 SDK 程序

- 首先从安装的的 `robomaster` 包中导入自己需要的模块，这里我们导入包含获取SDK版本信息的 `version` 模块::

    from robomaster import version

- 接下来通过 `version` 模块中的 `__version__` 属性可以获得 SDK 的版本号，并将其打印::

    sdk_version = version.__version__
    print("sdk version:", sdk_version)

-  运行程序，可以看到打印的结果::

    sdk version: 0.1.1.29

示例文档中提供了获取 SDK 版本号的例程 :file:`/examples/00_general/01_sdk_version.py`

.. literalinclude:: ./../../../examples/00_general/01_sdk_version.py
   :language: python
   :linenos:
   :lines: 17-
