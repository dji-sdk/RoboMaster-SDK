==========
Connection
==========

*****************
Connection Modes
*****************

The robot supports multiple connection modes, and can access and use SDK functions through any connection mode

- **Direct connection**:

    1. *Wi-Fi direct connection*: Access SDK functions by setting the robot to direct connection mode and connecting the robot's Wi-Fi hotspot

    2. *USB connection*: Access SDK functions through the USB port on the robot's smart console (RNDIS function support required)

    3. *UART connection*: Access SDK functions through the UART interface on the robot's motion controller

- **Networking connection**:

    1. *Wi-Fi networking*: The network connection is achieved by setting the robot to networking mode and adding the computing device and the robot onto the same LAN

************************
Connection Parameters
************************

1. For Wi-Fi direct connection, Wi-Fi networking, and USB connection, please refer to the following parameter configuration:

- **IP address description**:

    - In Wi-Fi direct connection mode, the robot's default IP is 192.168.2.1

    - In Wi-Fi networking mode, the robot's IP is dynamically assigned by the router, and connection is made by listening to the *IP broadcast* data port to obtain the robot's IP address in the current LAN
 
    - In USB connection mode, the computing device needs to support the RNDIS function. The robot's default IP is 192.168.42.2

- **Port and connection mode description**:

=============== ======== =============== ==============================================================================
Data            Port No. Connection mode Description
=============== ======== =============== ==============================================================================
Video streaming 40921    TCP             To output data, you need to execute the command to enable video streaming push
Audio streaming 40922    TCP             To output data, you need to execute the command to enable audio streaming push
Control command 40923    TCP             SDK mode can be enabled through the current channel. See **SDK Mode Control**
Message push    40924    UDP             To output data, you need to execute the command to enable message push
Event reporting 40925    TCP             To output data, you need to execute the command to enable event reporting
IP broadcasting 40926    UDP             Data will be output when the robot is not connected to any device
=============== ======== =============== ==============================================================================

2. Please refer to the following UART parameter configuration for the UART connection mode

========= ========= ========= ===========
Baud rate Data bits Stop bits Parity bits
========= ========= ========= ===========
115200     8        1         None
========= ========= ========= ===========

.. warning:: Description of the data under the UART connection mode:

    Under the UART connection mode, only *control command, message push, and event reporting* data is provided. If *video streaming or audio streaming* data is required, please use the *Wi-Fi/USB* connection mode

*******************
Connection Examples
*******************

Next, we will introduce examples of using various connection modes based on the Python programming language. In all of the following examples, a Python 3.x environment is required to be integrated on the default PC (please refer to 'Python Getting Started <https://www.python.org/about/gettingstarted/>' for the installation method). No further details on this will be provided here.

Wi-Fi direct connection
---------------------------

- **Environmental preparation**

1. Prepare a PC with Wi-Fi.

- **Establish connection**

1. Power on

	Power on the robot and toggle the connection mode switch of the smart console to **direct connection mode**

	.. image:: ../images/direct_connection_change.png

2. Establish a Wi-Fi connection

	Open the computer's wireless network access list, select the corresponding Wi-Fi name that is displayed on the robot's sticker, enter the 8-digit password, and select Connect

3. Prepare a connection script

	After establishing the Wi-Fi connection, we also need to program a TPC/IP connection. The robot offers multiple connection ports for connection. First, we should connect via the **control command port** (in direct connection mode, the IP address of the robot is ``192.168.2.1``, and the control command port number is ``40923``), so as to enable the robot's SDK mode.

	Here we compose a script to *establish control connection and enable SDK mode* by using the Python programming language as an example

	The reference code is as follows

	.. code-block:: python 
		:linenos:

		# Test environment: Python version 3.6

		import socket
		import sys

		# In direct connection mode, the default IP address of the robot is 192.168.2.1, and the control command port number is 40923
		host = "192.168.2.1"
		port = 40923

		def main():

			address = (host, int(port))

			# Establish a TCP connection with the robot's control command port
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			print("Connecting...")

			s.connect(address)

			print("Connected!")

			while True:

				# Wait for the user to input a control command
				msg = input(">>> please input SDK cmd: ")

				# Exit the current program when the user enters Q or q
				if msg.upper() == 'Q':
					break

				# Add a ';' terminator to the end
				msg += ';'

				# Transmit the control command to the robot
				s.send(msg.encode('utf-8'))

				try:
					# Wait for the robot to return the execution result
					buf = s.recv(1024)

					print(buf.decode('utf-8'))
				except socket.error as e:
					print("Error receiving :", e)
					sys.exit(1)
				if not len(buf):
					break

			# Disable the port connection
			s.shutdown(socket.SHUT_WR)
			s.close()	

		if __name__ == '__main__':
			main()

4. Save the above code as rm_direct_connection_sdk.py

5. Run the script
	
	**Windows system**	After installing the Python environment, you can double-click the \*.py file to run it. If it does not run, press ``win+r`` and enter ``cmd``. Press Enter to open and run the command, and then type and run ``python rm_direct_connection_sdk.py``;

	**Linux system**	Please press ``Ctrl+Alt+T`` to open the command line, and type and run ``python rm_direct_connection_sdk.py``

6. Establish a TCP/IP control connection

	When the run window displays ``Connecting...``, it is trying to establish a connection with the robot. When the run window displays ``Connected!``, it indicates that the control connection has been successfully established.

- **Validation**

After a successful control connection is established, enter ``command`` in the command line. If the robot returns ``OK``, the connection has been completed and the robot has successfully entered SDK mode. Then you can enter any control command to control the robot.

Wi-Fi/Wired network connection
------------------------------

- **Environmental preparation**

1. Prepare a PC with a network function (either Wi-Fi or wired network is accepted)
2. Prepare a home router

- **Establish connection**

1. Power on

	Power on the robot and toggle the connection mode switch of the smart console to **networking mode**

	.. image:: ../images/networking_connection_change.png


2. Establish a network connection
	
	Wi-Fi：

		If you use Wi-Fi connection, connect your PC to the router via Wi-Fi

	Wired network:

		If you use a wired network connection, connect your PC to the LAN port of the router via a network cable

	After your PC is connected to the router, open the RoboMaster program, go to the Networking Connection page, and press the Scan Code to Connect button on the robot's smart console to scan the QR code to connect to the network.

	.. image:: ../images/networking_connection_key.png

3. Obtain the IP address of the robot in the LAN

	After completing the networking connection, the PC should be in the same LAN as the robot. Next, we need to program a TPC/IP connection with the robot and connect to the **control command port** to enable SDK mode.

	If you are using a router with DHCP service enabled, the IP address of the robot is dynamically assigned by the router. You need to further obtain the IP address of the robot in the LAN. There are two ways to obtain the IP address:

		1. If you have connected through the RoboMaster program, go to the *Settings - > Connection* page of the RoboMaster program. The IP address of the robot in the LAN is displayed here.

		2. If you have established network connection via other means, you need to obtain the robot's IP address in the LAN by *listening to the address broadcast of the robot*. For more details, please refer to the **Broadcast** section.

		The reference code is as follows

		.. code-block:: python 
			:linenos:

			import socket

			ip_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

			# Bind the IP broadcast port
			ip_sock.bind(('0.0.0.0', 40926))

			# Wait to receive data
			ip_str = ip_sock.recvfrom(1024)

			# Output data
			print(ip_str)

		Save the above code as rm_get_robot_ip.py, and run it. The command line shall output:

			robot ip 192.168.0.115

		We can see that the IP address of the robot in the LAN, as obtained by *listening to the address broadcast of the robot*, is ``192.168.0.115``

3. Prepare a connection script

	Now we have obtained the robot's IP address, we shall compose a script to *establish control connection and enable SDK mode* by using the Python programming language as an example

	The reference code is as follows

	.. code-block:: python 
		:linenos:

		# Test environment: Python version 3.6

		import socket
		import sys

		# In networking mode, the current IP address of the robot is 192.168.0.115, and the control command port number is 40923
		# The robot's IP address is modified according to the actual IP address
		host = "192.168.0.115"
		port = 40923

		def main():

			address = (host, int(port))

			# Establish a TCP connection with the robot's control command port
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			print("Connecting...")

			s.connect(address)

			print("Connected!")

			while True:

				# Wait for the user to input a control command
				msg = input(">>> please input SDK cmd: ")

				# Exit the current program when the user enters Q or q
				if msg.upper() == 'Q':
					break
				
				# Add a ';' terminator to the end
				msg += ';'

				# Transmit the control command to the robot
				s.send(msg.encode('utf-8'))

				try:
					# Wait for the robot to return the execution result
					buf = s.recv(1024)

					print(buf.decode('utf-8'))
				except socket.error as e:
					print("Error receiving :", e)
					sys.exit(1)
				if not len(buf):
					break

			# Disable the port connection
			s.shutdown(socket.SHUT_WR)
			s.close()	

		if __name__ == '__main__':
			main()

4. Save the above code as rm_networking_connection_sdk.py

5. Run the script
	
	**Windows system**	After installing the Python environment, you can double-click the \*.py file to run it. If it does not run, press ``win+r`` and enter ``cmd``. Press Enter to open and run the command, and then type and run ``python rm_networking_connection_sdk.py``;

	**Linux system**	Please press ``Ctrl+Alt+T`` to open the command line, and type and run ``python rm_networking_connection_sdk.py``

6. Establish a TCP/IP control connection

	When the run window displays ``Connecting...``, it is trying to establish a connection with the robot. When the run window displays ``Connected!``, it indicates that the control connection has been successfully established.

- **Validation**

After a successful control connection is established, enter ``command`` in the command line. If the robot returns ``OK``, the connection has been completed and the robot has successfully entered SDK mode. Then you can enter any control command to control the robot.

USB Connection
---------------

USB connection mode essentially uses the RNDIS protocol to virtualize the USB device on the robot as a network card device, and initiate a TCP/IP connection via USB. For more information about RNDIS, see XXXXX

- **Environmental preparation**

1. Prepare a PC with the RNDIS function (please check that the RNDIS function is configured on the PC)
2. Prepare a micro-USB cable


- **Establish connection**

1. Power on

	Power on the robot. The position of the connection mode switch is not important

2. Establish a USB connection

	Connect the USB cable to the USB port on the smart console of the robot, and connect the other end of the cable to the computer

3. Test the connection

	Open a command line window and run::

		ping 192.168.42.2

	If the command line outputs **Reply from 192.168.42.2...**, it indicates that the link works. You can proceed to the next step, such as::

		PING 192.168.42.2 (192.168.42.2) 56(84) bytes of data.
		64 bytes from 192.168.42.2: icmp_seq=1 ttl=64 time=0.618 ms
		64 bytes from 192.168.42.2: icmp_seq=2 ttl=64 time=1.21 ms
		64 bytes from 192.168.42.2: icmp_seq=3 ttl=64 time=1.09 ms
		64 bytes from 192.168.42.2: icmp_seq=4 ttl=64 time=0.348 ms
		64 bytes from 192.168.42.2: icmp_seq=5 ttl=64 time=0.342 ms

		--- 192.168.42.2 ping statistics ---
		5 packets transmitted, 5 received, 0% packet loss, time 4037ms
		rtt min/avg/max/mdev = 0.342/0.723/1.216/0.368 ms	

	If the command line outputs ** Cannot access... ** or the display times out, you need to check whether the RNDIS service on the PC is configured properly and restart the robot to try again, such as::

		PING 192.168.42.2 (192.168.42.2) 56(84) bytes of data.

		--- 192.168.42.2 ping statistics ---

4. Prepare for connection

	The connection process is similar to `Wi-Fi Direct Connection` - > **Prepare a Connection Script**. You need to replace the robot's IP address with the IP address in USB mode, and the rest of the codes and steps remain unchanged, which will not be repeated here

	The reference code is changed as follows

	.. code-block:: python 
		:linenos:

		# Test environment: Python version 3.6

		import socket
		import sys

		# In USB mode, the robot's default IP address is 192.168.42.2, and the control command port number is 40923
		host = "192.168.42.2"
		port = 40923

		# other code

- **Validation**

After a successful control connection is established, enter ``command`` in the command line. If the robot returns ``OK``, the connection has been completed and the robot has successfully entered SDK mode. Then you can enter any control command to control the robot.


UART Connection
------------------

- **Environmental preparation**

1. Prepare a PC and confirm that the USB to serial port module driver is installed
2. Prepare a USB to serial port module
3. Prepare three DuPont cables

- **Establish connection**

1. Power on

	Power on the robot. The position of the connection mode switch is not important

2. Connecting the UART

	Plug the DuPont cables into the UART interface on the main controller of the robot chassis, that is into the GND, RX, and TX pins, respectively, and the other ends into the corresponding GND, TX, and RX pins of the USB serial port module

3. Configure the UART and establish a communication connection

	Here, we still use Python programming as an example to configure the UART for a Windows system.

	1. Confirm that the PC has recognized the USB to serial port module, and confirm the corresponding serial port number from the **Port** in the **Computer Device Manager**, such as COM3.

	2. Install the serial module:

		pip install pyserial

	3. Write the code for UART control. The reference code is as follows

	.. code-block:: python
		:linenos:

		# Test environment: Python version 3.6
		import serial

		ser = serial.Serial()

		# Configure the serial port: baud rate: 115200; data bits: 8; stop bits: 1; parity bits: 0; timeout: 0.2s
		ser.port = 'COM3'
		ser.baudrate = 115200
		ser.bytesize = serial.EIGHTBITS
		ser.stopbits = serial.STOPBITS_ONE
		ser.parity = serial.PARITY_NONE
		ser.timeout = 0.2

		# Open the serial port
		ser.open()
		 
		while True:

			# Wait for the user to input a control command
			msg = input(">>> please input SDK cmd: ")

			# Exit the current program when the user enters Q or q
			if msg.upper() == 'Q':
				break

			# Add a ';' terminator to the end
			msg += ';'

			ser.write(msg.encode('utf-8'))

			recv = ser.readall()

			print(recv.decode('utf-8'))

		# Close the serial port
		ser.close()

	4. Save the above program as rm_uart.py and run it

- **Validation**

After a successful control connection is established, enter ``command`` in the command line. If the robot returns ``OK``, the connection has been completed and the robot has successfully entered SDK mode. Then you can enter any control command to control the robot.


