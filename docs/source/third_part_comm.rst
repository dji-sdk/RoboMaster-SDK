==================================
第三方平台通信
==================================

*********
介绍
*********

用户使用第三方平台跟 RoboMaster EP 建立连接后，通过明文 SDK 和 EP 机器人进行通信，可以控制各个内置模块和拓展模块，并获取 EP 机器人的视频流、音频流，极大地丰富了 EP 的扩展性，解锁更多玩法。

******************
第三方平台类型
******************

用户使用的第三方平台为有自主计算能力，具有 WIFI 、 USB 和 UART 接口的计算平台，包括但不限于 DJI 妙算、Arduino 开发板、Micro:bit、树莓派、Jetson Nano 和 PC。

	.. image:: ./images/third_part.png
		:align: center

******************
通信方式
******************

第三方平台和 RoboMaster EP 的通信方式包括三种： WIFI、 USB 和 UART。下面介绍这三种通信方式的连接方法。

WIFI 连接
------------
WIFI 连接包括直连模式和路由器模式，具体参考如下说明。

直连模式
^^^^^^^^^^^

	:条件: 第三方平台具有 WIFI 连接功能。
	:用途: 第三方平台使用 WIFI 连接到 EP 后，通过明文 SDK 和 EP 进行通信。
	:步骤: 
		1. 启动 EP，切换智能中控的连接模式开关至 **直连模式**。
		2. 打开第三方平台的无线网络，扫描 EP 的热点，进行连接。
		3. 通过明文 SDK 和 EP 进行通信。（详细步骤参考 :ref:`wifi_direct`)
	:应用举例: DJI 妙算、Jetson Nano 或 PC 使用 WIFI 连接到 EP 后，通过明文 SDK 和 EP 进行通信，并获取 EP 的视频流、音频流。
	:示意图:

	.. image:: ./images/wifi_direct.png
		:align: center

	.. centered:: DJI 妙算、Jetson Nano 或 PC 通过 WIFI 直连模式连接到 EP

路由器模式
^^^^^^^^^^^

	:条件: 第三方平台具有 WIFI 或有线网络连接功能。
	:用途: 第三方平台和 EP 连接到同一个局域网中，通过明文 SDK 和 EP 进行通信。
	:步骤: 
		1. 启动 EP，切换智能中控的连接模式开关 **路由器模式**。
		2. 通过官方 App 的扫码连接方式将 EP 连接到路由器。
		3. 第三方平台通过 WIFI 或有线网络连接到同一路由器。
		4. 通过官方 App 的设置页面或是编写脚本等方式获取到 EP 的 IP 地址。
		5. 通过明文 SDK 和 EP 进行通信。（详细步骤参考 :ref:`wifi_sta`)
	:应用举例: DJI 妙算、Jetson Nano 或 PC 和 EP 连接到同一个局域网后，通过明文 SDK 和 EP 进行通信，并获取 EP 的视频流、音频流。
	:示意图:

	.. image:: ./images/wifi_sta.png
		:align: center

	.. centered:: DJI 妙算、Jetson Nano 或 PC 通过 WIFI 路由器模式连接到 EP

USB 连接
------------

	:条件: 第三方平台具有 TypeA USB 接口，并支持 RNDIS 功能。
	:用途: 第三方平台通过 USB 线连接到 EP 的智能中控的 Micro USB 端口，使用明文 SDK 和 EP 进行通信。
	:步骤: 
		1. 启动 EP，无需关心智能中控的连接模式开关位置。
		2. 第三方平台通过 USB 线连接到 EP 的智能中控。
		3. 通过明文 SDK 和 EP 进行通信。（详细步骤参考 :ref:`usb_conn`)
	:应用举例: 树莓派或 Jetson Nano 固定在 EP 小车上，并由 EP 的电源转接模块供电，通过 USB 连接到 EP，使用明文 SDK 和 EP 进行通信，并获取 EP 的视频流、音频流。
	:示意图:

	.. image:: ./images/raspberry.png
		:align: center

	.. centered:: 树莓派连接示意图

	.. image:: ./images/nano.png
		:align: center

	.. centered:: Jetson Nano连接示意图

.. _third_part_uart:

UART 连接
------------

	:条件: 第三方平台具有 UART 接口或有串口转 USB 功能。
	:用途: 第三方平台通过 UART 连接到 EP 运动控制器的 UART 接口，使用明文 SDK 和 EP 进行通信。
	:步骤: 
		1. 启动 EP，无需关心智能中控的连接模式开关位置。
		2. 第三方平台 UART 的 TX/RX 和 GND 分别连接到 EP 运动控制器 UART 的 RX/TX 和 GND。（参考 :ref:`uart_pin`)
		3. 通过明文 SDK 和 EP 进行通信。（详细步骤参考 :ref:`uart_conn`)
	:应用举例: Arduino 或 Micro:bit 固定在 EP 小车上，并由 EP 的电源转接模块供电，通过 UART 连接到 EP 运动控制器，使用明文 SDK 和 EP 进行通信。
	:示意图:

	.. image:: ./images/arduino.jpg
		:align: center

	.. centered:: Arduino连接示意图

	.. image:: ./images/microbit.png
		:align: center

	.. centered:: Micro:bit连接示意图
