==================================
第三方平台通信
==================================

*********
介紹
*********

用戶使用第三方平台跟 RoboMaster EP 建立連接後，通過明文 SDK 和 EP 機器人進行通信，可以控制各個內置模塊和拓展模塊，並獲取 EP 機器人的視頻流、音頻流，極大地豐富了 EP 的擴展性，解鎖更多玩法。

******************
第三方平台類型
******************

用戶使用的第三方平台為有自主計算能力，具有 WIFI 、 USB 和 UART 接口的計算平台，包括但不限於 DJI 妙算、Arduino 開發板、Micro:bit、樹莓派、Jetson Nano 和 PC。

	.. image:: ./images/third_part.png
		:align: center

******************
通信方式
******************

第三方平台和 RoboMaster EP 的通信方式包括三種： WIFI、 USB 和 UART。下面介紹這三種通信方式的連接方法。

WIFI 連接
------------
WIFI 連接包括直連模式和路由器模式，具體參考如下說明。

直連模式
^^^^^^^^^^^

	:條件: 第三方平台具有 WIFI 連接功能。
	:用途: 第三方平台使用 WIFI 連接到 EP 後，通過明文 SDK 和 EP 進行通信。
	:步驟: 
		1. 啟動 EP，切換智能中控的連接模式開關至 **直連模式**。
		2. 打開第三方平台的無線網絡，掃瞄 EP 的熱點，進行連接。
		3. 通過明文 SDK 和 EP 進行通信。（詳細步驟參考 :ref:`wifi_direct`)
	:應用舉例: DJI 妙算、Jetson Nano 或 PC 使用 WIFI 連接到 EP 後，通過明文 SDK 和 EP 進行通信，並獲取 EP 的視頻流、音頻流。
	:示意圖:

	.. image:: ./images/wifi_direct.png
		:align: center

	.. centered:: DJI 妙算、Jetson Nano 或 PC 通過 WIFI 直連模式連接到 EP

路由器模式
^^^^^^^^^^^

	:條件: 第三方平台具有 WIFI 或有線網絡連接功能。
	:用途: 第三方平台和 EP 連接到同一個局域網中，通過明文 SDK 和 EP 進行通信。
	:步驟: 
		1. 啟動 EP，切換智能中控的連接模式開關 **路由器模式**。
		2. 通過官方 App 的掃碼連接方式將 EP 連接到路由器。
		3. 第三方平台通過 WIFI 或有線網絡連接到同一路由器。
		4. 通過官方 App 的設置頁面或是編寫腳本等方式獲取到 EP 的 IP 地址。
		5. 通過明文 SDK 和 EP 進行通信。（詳細步驟參考 :ref:`wifi_sta`)
	:應用舉例: DJI 妙算、Jetson Nano 或 PC 和 EP 連接到同一個局域網後，通過明文 SDK 和 EP 進行通信，並獲取 EP 的視頻流、音頻流。
	:示意圖:

	.. image:: ./images/wifi_sta.png
		:align: center

	.. centered:: DJI 妙算、Jetson Nano 或 PC 通過 WIFI 路由器模式連接到 EP

USB 連接
------------

	:條件: 第三方平台具有 TypeA USB 接口，並支持 RNDIS 功能。
	:用途: 第三方平台通過 USB 線連接到 EP 的智能中控的 Micro USB 端口，使用明文 SDK 和 EP 進行通信。
	:步驟: 
		1. 啟動 EP，無需關心智能中控的連接模式開關位置。
		2. 第三方平台通過 USB 線連接到 EP 的智能中控。
		3. 通過明文 SDK 和 EP 進行通信。（詳細步驟參考 :ref:`usb_conn`)
	:應用舉例: 樹莓派或 Jetson Nano 固定在 EP 小車上，並由 EP 的電源轉接模塊供電，通過 USB 連接到 EP，使用明文 SDK 和 EP 進行通信，並獲取 EP 的視頻流、音頻流。
	:示意圖:

	.. image:: ./images/raspberry.png
		:align: center

	.. centered:: 樹莓派連接示意圖

	.. image:: ./images/nano.png
		:align: center

	.. centered:: Jetson Nano連接示意圖

.. _third_part_uart:

UART 連接
------------

	:條件: 第三方平台具有 UART 接口或有串口轉 USB 功能。
	:用途: 第三方平台通過 UART 連接到 EP 運動控制器的 UART 接口，使用明文 SDK 和 EP 進行通信。
	:步驟: 
		1. 啟動 EP，無需關心智能中控的連接模式開關位置。
		2. 第三方平台 UART 的 TX/RX 和 GND 分別連接到 EP 運動控制器 UART 的 RX/TX 和 GND。（參考 :ref:`uart_pin`)
		3. 通過明文 SDK 和 EP 進行通信。（詳細步驟參考 :ref:`uart_conn`)
	:應用舉例: Arduino 或 Micro:bit 固定在 EP 小車上，並由 EP 的電源轉接模塊供電，通過 UART 連接到 EP 運動控制器，使用明文 SDK 和 EP 進行通信。
	:示意圖:

	.. image:: ./images/arduino.jpg
		:align: center

	.. centered:: Arduino連接示意圖

	.. image:: ./images/microbit.png
		:align: center

	.. centered:: Micro:bit連接示意圖
