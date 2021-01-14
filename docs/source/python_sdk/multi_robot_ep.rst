.. _multi_robot_EP:

####################################################################
Implement Multi-device Formation for EP by Using the RoboMaster SDK
####################################################################

This document uses the Windows 64-bit operating system as an example to illustrate how to implement EP formation by using the RoboMaster SDK.

Demo environment requirements and materials checklist
--------------------------------------------------------

1. **Programming environment**

(1) Download the RoboMaster-SDK compressed package from GitHub at `RoboMaster-SDK compressed package <https://github.com/dji-sdk/RoboMaster-SDK/>`_ (alternative Gitee download address: `RoboMaster-SDK compressed package <https://gitee.com/xitinglin/RoboMaster-SDK>`_) by completing the following steps:

* Click ``Code`` and then ``Download ZIP`` to download the compressed package.

.. image:: ./../images/download_sdk.png
            :scale: 50%
            :align: center

* Decompress the downloaded RoboMaster-SDK-master.zip compressed package:

.. image:: ./../images/zip.png
			:align: center

* The compressed archive contains the following files:

	1. The VS-related runtime library: **VisualCppRedist_AIO_20200707.exe**

	2. The VS build tool:  **visualcppbuildtools_full.exe**

	3. RoboMaster SDK sample code:  **examples**

	4. The third-party library installation script: **lib_install.bat**


(2) Install the required VC library:

Run **VisualCppRedist_AIO_20200707.exe** in the decompressed RoboMaster-SDK archive and complete the installation:

.. image:: ./../images/vc_exe.png

.. warning:: The following error occurs if you use the SDK without installing the VC library:

	.. image:: ./../images/libmedia_err.png

(3) Install the VS build tool:

Run **visualcppbuildtools_full.exe** in the decompressed RoboMaster-SDK archive and complete the installation:

.. image:: ./../images/vs_build_tool.png

(4) Installation process in Python:

a. Locate the Python installation package on the `Python official website <https://www.python.org/downloads/windows/>`_ (Python 3.7.8 in this example) and download the installer in the package.

.. warning:: Ensure that the downloaded `python.exe` file is for 64-bit installation and the Python version is 3.6.6 or later. Otherwise, you cannot use the Python SDK properly due to compatibility issues. If you have already installed Python on your PC, we recommend that you uninstall it and install the required version.

.. image:: ./../images/win_python_setup1.png


b. Step 1: Check that the installation package is for ``64-bit`` installation, otherwise you cannot use the Python SDK properly.

   Step 2: Select ``Add Python 3.7 to Path``.

   Step (3): Select ``Install Now'' to begin installation, as shown in the figure below:

.. image:: ./../images/win_python_setup2.png


c. After the installation is complete, press the ``Win+R`` shortcut command, enter ``cmd`` in the window that appears to open the CLI, and then enter ``python'' on the CLI to confirm that Python 3.7.8 has been installed successfully.

.. image:: ./../images/python_version.png


(5) Install the dependent Python third-party library:

    Method 1: Locate the lib_install.bat file in the downloaded RoboMaster-SDK archive (:file:`RoboMaster-SDK-master/lib_install.bat`), right-click the file, and select "Run as Administrator".

    Method 2: Install RoboMaster SDK, click the start menu on your PC, and enter ``cmd`` in the search box. In the search results, right-click the CLI program and select ``Run as Administrator`` in the menu that appears. Then, enter the following commands in sequence::

		pip install robomaster
		pip install netaddr
		pip install netifaces
		pip install myqr

2. **EP vehicles**

- Quantity: 6 EP infantry vehicles

.. tip:: If you do not have 6 EP vehicles, use 2 EP vehicles. In this case, replace the rest of the code by referring to :file:`/examples/15_muti_robot/multi_ep/02_two_ep_demo.py`.

- Firmware version: 01.01.0500

.. tip:: You can upgrade the firmware version in the RoboMaster app to ensure that the firmware version is 01.01.0500 or later.

EP networking connection
----------------------------
Step 1: Set the network connection method of each EP robot to networking and add the PC and the robots to the same LAN for networking,

as shown in the figure below:

.. image:: ./../images/networking_connection_change.png
            :align: center

Step 2: Generate a QR code

- Refer to the example in the sample code directory of :file:`/examples/01_robot/05_sta_conn_helper.py` in the downloaded and decompressed RoboMaster-SDK archive.

.. literalinclude:: ./../../../examples/01_robot/05_sta_conn_helper.py
   :language: python
   :linenos:
   :lines: 17-

.. warning:: In line 13 of the sample code:

		info = helper.build_qrcode_string(ssid="RoboMaster_SDK_WIFI", password="12341234")

		Replace `ssid` (the router name) and `password` (the router password) with the actual name and password.

- Run the sample code to display the QR code. Then, press the scan button on the smart central control of the robot, and scan the QR code to connect to the network.

	.. image:: ./../images/networking_connection_key.png
            :align: center

- Execution result::

    Connected!

The light indicator of the robot changes from blinking white to solid turquoise.

.. note:: A total of 6 EP vehicles need to be connected to the Wi-Fi hotspot. When connecting the 6 EP vehicles one by one for the first time, repeatedly run the sample code to connect to each vehicle. After successful connection, the vehicles will be automatically connected upon the next startup.


Run the sample code for multi-device formation
---------------------------------------------------

- Refer to the example in the sample code directory of :file:`/examples/15_muti_robot/multi_ep/03_six_ep_demo.py` in the downloaded and decompressed RoboMaster-SDK archive.

1. After each robot is successfully connected to the same router, you need to manually change the robot SNs in the sample code. The SN of each robot can be found on the label of the smart central control, as shown in the figure below:

.. image:: ./../images/sn_num.jpg
            :scale: 40%
            :align: center

2. Edit the sample code and locate line 203:

	.. literalinclude:: ./../../../examples/15_multi_robot/multi_ep/03_six_ep_demo.py
	   :language: python
	   :linenos:
	   :lines: 203-204

	Change the SNs in the sample code based on the actual SNs of the robots.

3. According to the order of the six SNs, place the six robots in sequence as shown in the figure below. The direction of the arrow is the direction of the robots.

.. image:: ./../images/6EPlocate.png
            :scale: 50%
            :align: center


Run the modified sample program
-----------------------------------

- Go to the: file:`/examples/15_muti_robot/multi_ep/` directory, press and hold the Shift key, right-click any blank area in the directory, and then select "Open Powershell Window Here" or "Open Command Window Here".

- Run the code and enter the following in the command window:::

	python 03_six_ep_demo.py
