==================================
 编程环境安装
==================================

介绍
-----------

用户在 PC 上通过 WIFI、 USB 和 UART 跟 EP 建立连接后，可以使用明文 SDK 跟 EP 进行通信，进行更复杂的二次开发。用户可以在 PC 上使用 C++、 C#、 Python 或是其他语言进行编程，用户可根据自身开发能力选择开发语言。

为了让用户尽快熟悉 EP 的各个模块和功能，并方便使用本网站中的 Python 示例代码，我们介绍一下 Python 在 PC 上的安装步骤。


在 Windows 上安装 Python
-------------------------

**环境：** Windows 10 64 位

1. 从python官网  `python 官网链接 <https://www.python.org/downloads/windows/>`_ 找到可以下载的安装包，以Python3.7.8 为例，选择安装文件进行下载。

.. warning:: 请确保下载的 `python.exe` 是64位的，python sdk适配3.6.6以上至3.8.9版本python版本，否则会影响python sdk的使用，切记。

.. image:: ./images/win_python_setup1.png


2. 步骤（1）：确认安装包版本是 ``64-bit``, 否则会影响Python sdk使用。

   步骤（2）：勾选 ``Add Python 3.7 to Path``。

   步骤（3）：选择 ``Install Now`` 进行安装，如下图所示。

.. image:: ./images/win_python_setup2.png


3. 安装完成后按 ``win+r``，在弹出窗口中输入 ``cmd`` 打开命令提示符界面，在命令行里面输入 ``python``, 确认 Python 3.7.8 安装成功。

.. image:: ./images/python_version.png

.. note:: cmd窗口会显示对应的版本信息，否则，请从第一步重新安装


在 Ubuntu 上安装 Python
-------------------------

**环境：** ubuntu 16.04 64 位，Python 3.7.8

1. Ubuntu16.04 默认安装了Python2.7和3.5，输入命令 ``python``，可以查看 Python 默认版本。请注意，系统自带的python千万不能卸载。

2. 输入如下命令安装 python 3.7 软件包：

::

	sudo add-apt-repository ppa:jonathonf/python-3.7
	sudo apt-get update
	sudo apt-get install python3.7

3. 输入如下命令，调整 Python3 的优先级，使得 Python 3.7 优先级较高。

::

		sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
		sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 2
		sudo update-alternatives --install /usr/bin/python python /usr/bin/python2 100
		sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 150

4. 此时再输入命令 ``python`` ，确认 Python 3.7 安装成功。


