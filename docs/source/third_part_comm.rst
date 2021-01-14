==================================
Third-party Platform Communication
==================================

*********
Introduction
*********

After using a third-party platform to establish a connection with RoboMaster EP, you can communicate with the EP robot through the plaintext SDK. In addition, you can control each built-in module and extended module and obtain the video stream and audio stream of the EP robot, which greatly improves the extension capabilities of EP and enables more fun applications.

******************
Third-party platform types
******************

Applicable third-party platforms are computing platforms with autonomous computing capabilities and Wi-Fi, USB, and UART interfaces, such as DJI Manifold, Arduino Development Board, Micro:bit, Raspberry Pi, Jetson Nano, or PCs.

	.. image:: ./images/third_part.png
		:align: center

******************
Communication methods
******************

There are three communication methods between the third-party platform and RoboMaster EP: Wi-Fi, USB, and UART. The working principles of the three communication methods are described below.

Wi-Fi connection
------------
There are two Wi-Fi connection modes, direct connection mode and router mode, which are described as follows.

The direct connection mode
^^^^^^^^^^^

	:prerequisites: The third-party platform must have a Wi-Fi function.
	:purposes: After connecting to EP via Wi-Fi, the third-party platform communicates with EP through the plaintext SDK.
	:steps: 
		1. Turn on the EP and set the connection method switch of the smart central control to the **direct connection mode**.
		2. Turn on the wireless network of the third-party platform and then scan for and connect to the EP hotspot.
		3. Communicate with EP through the plaintext SDK. (For detailed instructions, refer to :ref:`wifi_direct`)
	:Application example: After connecting to EP via Wi-Fi, the DJI Manifold, Jetson Nano, or your PC communicates with EP through the plaintext SDK and obtains the video and audio streams from the EP.
	:schematic diagram:

	.. image:: ./images/wifi_direct.png
		:align: center

	.. centered:: DJI Manifold, Jetson Nano, or the PC connects to EP in Wi-Fi direct connection mode

The router mode
^^^^^^^^^^^

	:prerequisites: The third-party platform supports Wi-Fi or wireless connection.
	:purposes: The third-party platform and EP connect to the same LAN, and then the platform communicates with EP through the plaintext SDK.
	:steps: 
		1. Turn on EP and set the connection method switch of the smart central control to the **router mode**.
		2. Connect EP to the router by scanning the QR code in the official app.
		3. The third-party platform connects to the same router via Wi-Fi or a wired network.
		4. Obtain the IP address of EP from the settings page in the official app or by scripting.
		5. Communicate with EP through the plaintext SDK. (For detailed instructions, refer to :ref:`wifi_sta`)
	:application example: After connecting to the same LAN, the DJI Manifold, Jetson Nano, or your PC communicates with EP through the plaintext SDK and obtains the video and audio streams of EP.
	:schematic diagram:

	.. image:: ./images/wifi_sta.png
		:align: center

	.. centered:: DJI Manifold, Jetson Nano, or the PC connects to EP in Wi-Fi router mode

USB connection
------------

	:prerequisites: The third-party platform has a Type-A USB interface and supports the RNDIS function.
	:purposes: The third-party platform connects to the micro USB port of the smart central control of EP through a USB cable and uses the plaintext SDK to communicate with EP.
	:steps: 
		1. Turn on EP without concerning yourself with the current connection method.
		2. The third-party platform connects to the smart central control of EP through a USB cable.
		3. Communicate with EP through the plaintext SDK. (For detailed instructions, refer to :ref:`usb_conn`)
	:application example: Secure the Raspberry Pi or Jetson Nano, which is powered by the EP power adapter module, on the EP vehicle. Then, connect the powered device to EP via the USB port, communicate with EP through the plaintext SDK, and obtain the video and audio streams of EP.
	:schematic diagram:

	.. image:: ./images/raspberry.png
		:align: center

	.. centered:: Raspberry Pi connection diagram

	.. image:: ./images/nano.png
		:align: center

	.. centered:: Jetson Nano connection diagram

.. _third_part_uart:

UART connection
------------

	:prerequisites: The third-party platform has a UART interface or a serial-to-USB function.
	:purposes: The third-party platform connects to the UART port of the EP motion controller through UART and uses the plaintext SDK to communicate with EP.
	:steps: 
		1. Turn on EP without concerning yourself with the current connection method.
		2. Connect the TX/RX and GND terminals of the UART module of the third-party platform to the RX/TX and GND terminals of the UART module of the EP motion controller. (Refer to :ref:`uart_pin`)
		3. Communicate with EP through the plaintext SDK. (For detailed instructions, refer to :ref:`uart_conn`)
	:application example: Secure the Arduino or Micro:bit, which is powered by the EP power adapter module, on the EP vehicle. Then, connect the powered device to the EP motion controller via UART and use the plaintext SDK to communicate with EP.
	:schematic diagram:

	.. image:: ./images/arduino.jpg
		:align: center

	.. centered:: Arduino connection diagram

	.. image:: ./images/microbit.png
		:align: center

	.. centered:: Micro:bit connection diagram
