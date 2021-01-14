==================================
Introduction to the Plaintext SDK
==================================

A major function of RoboMaster EP is its support for the plaintext SDK, which includes the control interfaces of each built-in module and extended module, as well as the output interfaces of video streams and audio streams. EP supports multiple access methods such as USB, Wi-Fi, and UART. Users can choose any access methods based on their platform interfaces.

The plaintext SDK greatly enriches the extensibility of EP, enabling easy :doc:`communication with third-party platforms<../third_part_comm>` for secondary development. This document explains how to use plaintext protocols in the SDK through the **Wi-Fi direct connection** method (for other available connection methods, refer to :doc:`Establish a Connection<./connection>`) to **control blaster firing** as an example.

Development preparations
----------------------------

1. Prepare a PC with a Wi-Fi connection function.
2. Install the Python 3.x environment on the PC. For the installation process, refer to `Python Getting Started <https://www.python.org/about/gettingstarted/>`_. 

Establish a connection
--------------------------

1. Turn on the robot.

	Turn on the robot and set the connection method switch of the smart central control to the **direct connection mode**, as shown in the figure below:

	.. image:: ../images/direct_connection_change.png

2. Establish a Wi-Fi connection.

	Open the wireless network access list on the PC, select the Wi-Fi hotspot name displayed on the sticker on the robot body, enter the 8-digit password, and then select "Connect".

3. Prepare the connection script.

	After establishing the Wi-Fi connection, write code to establish a TPC/IP connection with the robot and transmit a specific **plaintext protocol** on the corresponding port for control. For more information about **plaintext protocols**, refer to :doc:`Protocol Content<./protocol_api>`.

	The following example uses the Python programming language to write a script to *Establish control connection, receive user instructions, and transmit plaintext protocols*. This allows you to control the robot.

	The sample code is as follows:

.. code-block:: python 
	:linenos:

	# -*- encoding: utf-8 -*-
	# Test environment: Python 3.6

	import socket
	import sys

	# In direct connection mode, the default IP address of the robot is 192.168.2.1 and the control command port is port 40923.
	host = "192.168.2.1"
	port = 40923

	def main():

		address = (host, int(port))

		# Establish a TCP connection with the control command port of the robot.
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		print("Connecting...")

		s.connect(address)

		print("Connected!")

		while True:

			# Wait for the user to enter control commands.
			msg = input(">>> please input SDK cmd: ")

			# When the user enters Q or q, exit the current program.
			if msg.upper() == 'Q':
				break

			# Add the ending character.
			msg += ';'

			# Send control commands to the robot.
			s.send(msg.encode('utf-8'))

			try:
				# Wait for the robot to return the execution result.
				buf = s.recv(1024)

				print(buf.decode('utf-8'))
			except socket.error as e:
				print("Error receiving :", e)
				sys.exit(1)
			if not len(buf):
				break

		# Disconnect the port connection.
		s.shutdown(socket.SHUT_WR)
		s.close()

	if __name__ == '__main__':
		main()

4. Save the preceding code as rm_sdk.py.

5. Run the script.
	
	Run the rm_sdk.py file. (In Windows, after installing the Python environment, double-click the \*.py file to run it. If you fail to run the file, press the ``Win+R`` shortcut command and enter ``cmd``. Then, press Enter to open the CLI and enter ``python rm_sdk.py`` to run the file. In Linux, press ``Ctrl+Alt+T`` to open the CLI and enter ``python rm_sdk.py``.)

6. Establish a TCP/IP control connection.

	When ``Connecting...'' appears in the running window, the system is attempting to establish a connection with the robot. When ``Connected!;`` appears in the running window, the control connection has been established.


Enable the SDK mode
---------------------

To perform SDK control, you need to have the robot enter SDK mode. To do this, enter *command* in the aforementioned Python running window and press Enter. The program will then send the command to the robot. If the robot returns *ok*, it has entered SDK mode.::

	>>> please input SDK cmd: command
	ok

After entering SDK mode, you can enter control commands to control the robot.

Send control commands
----------------------

When you enter *blaster fire*, *ok* is returned and the blaster fires once.::

	>>> please input SDK cmd: blaster fire
	ok

Now, you can enter other control commands to further control the robot. For more control commands, refer to :doc:`Plaintext Protocols<./apis>`.

Exit SDK mode.
------------------

After completing all control commands, you need to exit SDK mode to allow the use of other robot functions.

Enter *quit* to exit SDK mode. After exiting SDK mode, you can no longer use SDK functions. To use them, enter *command* again to re-enter SDK mode.::

	>>> please input SDK cmd: quit
	ok

Summary
------------------

In the preceding steps, we established a physical connection with the robot, established a TCP/IP control connection with the robot, instructed the robot to enter SDK mode, sent control commands, and quit SDK mode. This illustrated the use of relevant control functions through the SDK. You can implement more complex logic and more interesting functions by building on the content in the *Send control commands* section.

When writing the control code, if you are more familiar with other languages, you can use them for the entire control process.

If your device does not support Wi-Fi connection and cannot use **Wi-Fi direct connection**, refer to :doc:`连接 <./connection>` for other available connection methods.

For more information about the SDK, refer to the :doc:`SDK documentation<./connection>`. For more sample code, refer to `RoboMaster Sample Code <https://github.com/dji-sdk/RoboMaster-SDK>`_.
