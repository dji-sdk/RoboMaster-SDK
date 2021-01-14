================
UART Interface
================

Introduction
-----------------

UART is used to connect third-party platforms with EP. You can easily establish a connection between the MCU mounted on EP and EP through UART and implement the interactive logic on the MCU. Then, you can use the cleartext SDK to communicate with the EP robot to implement automatic EP control.

.. _uart_pin:

Pin description
----------------------

The UART interface of EP is on the motion controller, and the pins are described as follows:

	.. image:: ../images/uart.png
		:align: center

Serial port configuration
------------------------------

========= ====== ====== ====== ==========
Communication interface    Baud rate    Data bit    Stop bit    Parity
========= ====== ====== ====== ==========
UART    115200    8    1    N/A
========= ====== ====== ====== ==========

Third-party platform connection method
----------------------------------------

Refer to :ref:`third_part_uart`.

Python programming example
---------------------------

1. The PC is connected to the UART interface of the EP motion controller through a serial-to-USB adapter.
2. Turn on the serial-port debugging assistant on the PC. Then, select and enable the COM port corresponding to the serial port.
3. Open the official app that has established a connection with EP and enter the Python programming mode.
4. On the Python programming page, write a simple program, using read_string() to read data from the serial port. Next, output the data and forward it with write_string(). Then, click the "Start" button to run the program.
5. Send a string by using the serial-port debugging assistant to see if you can receive the string correctly. Meanwhile, check whether the string is correctly output on the app.

	.. image:: ../images/uart_serial.png
		:align: center

	.. centered:: The serial debugging assistant sends and echoes the string

	.. image:: ../images/uart_pc.png
		:align: center

	.. centered:: The app outputs the received string and then forwards it

Cleartext SDK example
---------------------------

1. The PC is connected to the UART interface of the EP motion controller through a serial-to-USB adapter.
2. Turn on the serial-port debugging assistant on the PC. Then, select and enable the COM port corresponding to the serial port.
3. Send the ``command;`` string through the serial-port debugging assistant. If you receive ``ok'' from EP, the cleartext SDK successfully parsed the sent string.

	.. image:: ../images/uart_serial_sdk.png
		:align: center

	.. centered:: The serial debugging assistant sends the SDK string and receives the response

.. caution::

    When sending a cleartext SDK command through UART, you must append a semicolon (``;``) after the command, otherwise parsing will fail.

Python API
--------------------------

Refer to :doc:`UART<../python/uart>`.
