======================================
 Programming Environment Installation
======================================

Introduction
--------------

After you establish a connection between your PC and the EP through Wi-Fi, USB, or UART, you can use the plaintext SDK to communicate with the EP for more complex secondary development. You can use C++, C#, Python, or other languages for programming on the PC based on your development capabilities.

This document describes the procedure for installing Python on your PC to help you understand the various modules and functions of the EP and to help you use the Python sample code on this website.


Install Python on Windows
-------------------------

**Environment:** Windows 10 64-bit

1. Locate the Python installation package on the `Python official website <https://www.python.org/downloads/windows/>`_ (Python 3.7.8 in this example) and download the installer in the package.

.. warning:: Ensure that the downloaded `python.exe` file is for 64-bit installation and the Python version is between 3.6.6 and 3.8.9. Otherwise, you cannot use the Python SDK properly due to compatibility issues.

.. image:: ./images/win_python_setup1.png


2. Step 1: Check that the installation package is for ``64-bit`` installation, otherwise you cannot use the Python SDK properly.

   Step 2: Select ``Add Python 3.7 to Path``.

   Step (3): Select ``Install Now'' to begin installation, as shown in the figure below:

.. image:: ./images/win_python_setup2.png


3. After the installation is complete, press the ``Win+R`` shortcut command, enter ``cmd`` in the window that appears to open the CLI, and then enter ``python'' on the CLI to confirm that Python 3.7.8 has been installed successfully.

.. image:: ./images/python_version.png

.. note:: The cmd window will display the corresponding version information. If you cannot see this information, reinstall Python by repeating the preceding steps.


Install Python on Ubuntu
-------------------------

**Environment:** Ubuntu 16.04 64-bit and Python 3.7.8

1. Ubuntu 16.04 provides Python 2.7 or 3.5 by default. By entering the ``python`` command, you can view the default version of the installed Python program. Note that the Python program that comes with the system must not be uninstalled.

2. Run the following commands to install Python 3.7:

::

	sudo add-apt-repository ppa:jonathonf/python-3.7
	sudo apt-get update
	sudo apt-get install python3.7

3. Run the following commands to adjust the priority of Python 3 so that Python 3.7 has a higher priority:

::

		sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
		sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 2
		sudo update-alternatives --install /usr/bin/python python /usr/bin/python2 100
		sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 150

4. Run the ``python`` command again to verify that Python 3.7 has been installed successfully.


