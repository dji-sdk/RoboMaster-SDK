=======================================
Get Started Quickly with RoboMaster SDK
=======================================

Introduction
-------------

As an education robot, RoboMaster EP features strong scalability and programmability. In terms of programmability, it provides Scratch programming, Python programming, and SDK to facilitate users in conducting secondary development on RoboMaster EP and expanding more functions.

Next, we will complete the **Control the blaster emission** function as an example and use the **Wi-Fi direct connection** mode (for other connection modes, please refer to :doc:`Connection <./sdk/connection>`) to introduce the use of the plain-text protocol in the SDK.

Pre-development preparation
---------------------------

1. Prepare a PC with Wi-Fi.
2. Establish a Python 3.x environment on the PC. For installation methods, please refer to `Python Getting Started <https://www.python.org/about/gettingstarted/>`_ 

Establish connection
--------------------

1. Power on

	Power on the robot and toggle the connection mode switch of the smart console to **direct connection mode**

	.. image:: images/direct_connection_change.png

2. Establish a Wi-Fi connection

	Open the computer's wireless network access list, select the corresponding Wi-Fi name that is displayed on the robot's sticker, enter the 8-digit password, and select Connect

3. Prepare a connection script

	After completing the Wi-Fi connection, we also need to program a TPC/IP connection with the robot, and transmit the specific **plain-text protocol** on the corresponding port, so as to implement corresponding control. For more information on **plain-text protocol**, please refer to :doc:`Protocol Content<./sdk/protocol_api>`.

	Here we take Python programming language as an example and compose a script to complete the process of *establishing control connection, receiving instructions from the user, and transmitting plain-text protocol* for the purpose of controlling the robot.

	The reference code is as follows

.. code-block:: python 
	:linenos:

	# Test environment: Python version 3.6

	import socket
	import sys

	# In direct connection mode, the robot's default IP address is 192.168.2.1, and the control command port number is 40923
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

4. Save the above code as rm_sdk.py

5. Run the script
	
	Run the rm_sdk.py file (For a Windows system, you can double-click the \*.py file to run it directly after the Python environment is installed. If it can't run, press ``Win+R`` and enter ``cmd``. Press Enter to open the command line, and type ``python rm_sdk.py`` to run it; for Linux system, press ``Ctrl+Alt+T`` to open the command line and type ``python rm_sdk.py`` to run it)

6. Establish a TCP/IP control connection

	When the Run window displays ``Connecting...``, it is trying to establish a connection with the robot. When the Run window displays ``Connected!``, it means that the control connection has been successfully established.


Enable SDK mode
------------------

To implement SDK control, we need to control the robot to enter SDK mode. Enter *command* in the Python Run window above, press Enter, and then the program will send the command to the robot. If it returns *OK*, it means the robot has successfully entered SDK mode:

	>>> please input SDK cmd: command
	ok

After entering SDK mode, we can input control commands to control the robot.

Transmit control commands
-------------------------

Proceed to input *blaster fire*, and it should return *OK*. At the same time, the blaster fires once:

	>>> please input SDK cmd: blaster fire
	ok

Then, you can input other control commands to control the robot. For more control commands, please refer to :doc:`Protocol <./sdk/api>`

Exit SDK mode
------------------

After completing all our control commands, we need to exit from SDK mode so that other functions of our robot can be used normally.

Enter *quit* to exit SDK mode. After exiting SDK mode, you cannot continue to use the SDK functions. To use them, please re-enter *command* to enter SDK mode::

	>>> please input SDK cmd: quit
	quit sdk mode successfully

Summary
------------------

In the foregoing, we implemented relevant robot control functions via SDK through several steps, including establishing a physical connection and then TCP/IP control connection with the robot, controlling the robot to enter SDK mode, transmitting control commands, and exiting SDK mode. You can implement more complex logic and more interesting functions by adding to the content of the *Transmitting control commands* section.

In the Python programming control section, if you are more familiar with other languages, you can also use other languages to complete the whole control process.

If your device doesn't support Wi-Fi and can't use **Wi-Fi direct connection**, please refer to :doc:`Connection <./sdk/connection>` to use other connection modes.

This concludes how to get started with SDK. For more details, see :doc:`SDK documentation <./sdk/connection>`.
