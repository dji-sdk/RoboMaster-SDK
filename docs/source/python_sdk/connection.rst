.. _conn:


###########################################
Connect the RoboMaster SDK with Robots
###########################################

.. _EpConn:

EP connection method
***********************

The RoboMaster SDK can connect with EP through three methods: Wi-Fi direct connection, Wi-Fi networking, and USB (RNDIS) connection.

1. **Wi-Fi direct connection**

*Wi-Fi direct connection*: Set the connection method of the robot to direct connection and connect to the robot’s Wi-Fi hotspot. In Wi-Fi direct connection mode, the default IP address of the robot is 192.168.2.1.

- Turn on the robot and set the connection method switch of the smart central control to the **direct connection mode**, as shown in the figure below:

	.. image:: ./../images/direct_connection_change.png
            :scale: 70%
            :align: center

- Prepare a device with a Wi-Fi connection function, such as DJI Manifold, Jetson Nano, or your PC.

	.. image:: ./../images/wifi_direct.png
		    :align: center

    .. centered:: Directly connect DJI Manifold, Jetson Nano, or your PC to EP via Wi-Fi connection.

- Refer to the example in the :file:`/examples/01_robot/04_ap_conn.py` directory of the SDK code (`GitHub RoboMaster SDK repository <https://github.com/dji-sdk/robomaster-sdk>`_).

.. literalinclude:: ./../../../examples/01_robot/04_ap_conn.py
   :language: python
   :linenos:
   :lines: 17-

- Execution result::

    Robot Version: xx.xx.xx.xx


2. **USB connection**

*USB connection*: Connect via the USB port on the robot's smart central control. In this case, the default IP address of the robot is 192.168.42.2.

The USB connection method essentially uses the RNDIS protocol to virtualize the USB device on the robot as a network card.
For information about establishing TCP/IP connections to access more RNDIS content through the USB port, refer to `RNDIS Wikipedia <https://www.wikipedia.org/wiki/RNDIS>`_.

- Choose a third-party platform that has a Type-A USB port and supports RNDIS functions. In the following Raspberry Pi connection example, the blue line in the figure indicates the USB connection, and the red line indicates the power-supply line:

	.. image:: ./../images/raspberry.png
		    :align: center

	.. centered:: Raspberry Pi connection diagram

- Refer to the example in the :file:`/examples/01_robot/06_rndis_conn.py` directory of the SDK code (`GitHub RoboMaster SDK repository <https://github.com/dji-sdk/robomaster-sdk>`_).

.. literalinclude:: ./../../../examples/01_robot/06_rndis_conn.py
   :language: python
   :linenos:
   :lines: 17-

- Execution result::

    Robot Version: xx.xx.xx.xx


3. **Networking connection**

*Networking connection*: Set the network connection method of the robot to networking and add the computing device and the robot to the same LAN in order to network them.

- Turn on the robot and set the connection method switch of the smart central control to the **networking mode**.

	.. image:: ./../images/networking_connection_change.png
            :scale: 50%
            :align: center

- Connect the DJI Manifold, Jetson Nano, or your PC and the EP to the same LAN for EP communication.

	.. image:: ./../images/wifi_sta.png
		    :align: center

	.. centered:: Route the DJI Manifold, Jetson Nano, or PC to EP.

- Install the myqr library to generate a QR code, press the ``Win+R`` shortcut command, enter ``cmd`` in the window that appears to open the CLI, and then enter the following command on the CLI:::

   pip install myqr

- Refer to the example in the :file:`/examples/01_robot/05_sta_conn_helper.py` directory of the SDK code (`GitHub RoboMaster SDK repository <https://github.com/dji-sdk/robomaster-sdk>`_).

.. literalinclude:: ./../../../examples/01_robot/05_sta_conn_helper.py
   :language: python
   :linenos:
   :lines: 17-

.. warning:: In line 13 of the sample code, replace `ssid` (the router name) and `password` (the router password) with the actual name and password.

- Run the sample code to display the QR code. Then, press the scan button on the smart central control of the robot, and scan the QR code to connect to the network.

	.. image:: ./../images/networking_connection_key.png
            :align: center

- Execution result::

    Connected!

The light indicator of the robot changes from blinking white to solid turquoise.

.. tip:: In networking mode, you can connect to a specified robot by using its SN. To specify the SN of a robot, assign a value to the `sn` parameter during initialization.
  Refer to the example in :file:`/examples/01_robot/05_sta_conn_sn.py` (`GitHub RoboMaster SDK repository <https://github.com/dji-sdk/robomaster-sdk>`_). When `sn` is not specified, the SDK will establish a connection with the first robot detected by default.

    .. literalinclude:: ./../../../examples/01_robot/05_sta_conn_sn.py
       :language: python
       :linenos:
       :lines: 17-

.. _TelloConn:

Connection methods of education-series devices
***************************************************

Currently, the main education-series drones are Tello EDU and Tello Talent. The RoboMaster SDK supports connection with these products via Wi-Fi direct connection.

1. **Wi-Fi direct connection**

*Wi-Fi direct connection*: Set the connection method of the robot to direct connection and connect to the robot’s Wi-Fi hotspot. In Wi-Fi direct connection mode, the default IP address of the robot is 192.168.10.1.

- First, set the robot to work in Wi-Fi direct connection mode.

    -  *Tello EDU*: Short-press the power button indicated by the red arrow in the figure and wait for the yellow light to flash quickly to indicate successful device startup. The factory default connection method of the robot is Wi-Fi direct connection. If the robot is in networking mode after startup,
       press the power button to reset the Wi-Fi connection. To do this, long-press the power button for five seconds when the robot is on. During this operation, the status indicator will turn off and then flash yellow.
       When the status indicator flashes yellow quickly, the SSI and password of the Wi-Fi connection will be reset to their factory default settings. By default, there is no password.

	.. image:: ./../images/tello_power.png
            :scale: 50%
            :align: center

    -  *Tello Talent*:: Turn on the robot and set the mode switch of the extended module to the **direct connection mode**, as shown in the figure below:

	.. image:: ./../images/direct_connection_change.png
            :scale: 70%
            :align: center

- Prepare a device with a Wi-Fi connection function to connect to the Wi-Fi hotspot of the education-series device. This can be a DJI Manifold, Jetson Nano, or your PC.

- Refer to the example in the :file:`/examples/12_drone/01_ap_conn.py` directory of the SDK code (`GitHub RoboMaster SDK repository <https://github.com/dji-sdk/robomaster-sdk>`_).

.. literalinclude:: ./../../../examples/12_drone/01_ap_conn.py
   :language: python
   :linenos:
   :lines: 17-

- Execution result::

    Drone SDK Version: xx.xx.xx.xx


2. **Networking**

*Networking mode*: Set the robot to work in networking mode and connect to the LAN of the device running the SDK.

- First, set the connection method of the robot to the *direct connection mode* and connect to the device running the SDK. For details, see the previous section.

- Run the provided :file:`/examples/12_drone/23_set_sta.py` sample program (`GitHub RoboMaster SDK repository <https://github.com/dji-sdk/robomaster-sdk>`_)
  and replace the `ssis` and `password` parameters in the program with the account and password of the current router.

.. literalinclude:: ./../../..//examples/12_drone/23_set_sta.py
   :language: python
   :linenos:
   :lines: 17-

-  Set the connection method switch of the extended module to the networking mode.Then, the device will automatically connect to the LAN of the specified router.

- Connect the device running the SDK to the same LAN so that the SDK and the device are on the same network.

Communication method
************************

Communication method for EP
____________________________

The three methods of connecting the RoboMaster SDK and EP support TCP and UDP communication.

======== ======================== ==================================
 Parameter        TCP        UDP
======== ======================== ==================================
Reliability	      Reliable	                  Unreliable
Connectivity	      Connection-oriented        No connection
Efficiency	       Low	                    High
Scenarios	   Scenarios with high data accuracy requirements	      Scenarios with high real-time data transfer requirements
======== ======================== ==================================

.. tip:: Use UDP if the robot needs to control movement in real time, and use TCP if the robot needs to perform event-based control.

Select an appropriate communication method based on your application scenario.
For more information about TCP communication, refer to `TCP Wikipedia <https://en.wikipedia.org/wiki/Transmission_Control_Protocol>`_. 
For more information about UDP communication, refer to `UDP Wikipedia <https://en.wikipedia.org/wiki/User_Datagram_Protocol>`_.

1. TCP communication

- Refer to the example in the :file:`/examples/01_robot/07_tcp_protocol.py` directory of the SDK code (`GitHub RoboMaster SDK repository <https://github.com/dji-sdk/robomaster-sdk>`_).

.. literalinclude:: ./../../../examples/01_robot/07_tcp_protocol.py
   :language: python
   :linenos:
   :lines: 17-

- Networking connection

Here, you can modify the *connect_type* parameter in line 8 of the code. :file:`sta` corresponds to networking connection, :file:`ap` corresponds to Wi-Fi direct connection, and :file:`rndis` corresponds to USB connection.

- Run the program and obtain the execution result returned.::

    Robot Version: xx.xx.xx.xx

2. UDP communication

- Refer to the example in the :file:`/examples/01_robot/08_udp_protocol.py` directory of the SDK code (`GitHub RoboMaster SDK repository <https://github.com/dji-sdk/robomaster-sdk>`_).

.. literalinclude:: ./../../../examples/01_robot/08_udp_protocol.py
   :language: python
   :linenos:
   :lines: 17-

- Perform networking connection

Here, you can modify the *connect_type* parameter in line 8 of the code. :file:`sta` corresponds to networking connection, :file:`ap` corresponds to Wi-Fi direct connection, and :file:`rndis` corresponds to USB connection.

.. tip:: Different communication methods are implemented by modifying the *proto_type* parameter of the *robot.initialize()* function in line 8, where :file:`tcp` corresponds to TCP communication and :file:`udp` corresponds to UDP communication.

- Run the program and obtain the execution result returned.::

    Robot Version: xx.xx.xx.xx

Communication methods of education-series robots
_________________________________________________

Currently, Tello EDU and Tello Talent support only UDP communication. Therefore, no extra configuration is required.

