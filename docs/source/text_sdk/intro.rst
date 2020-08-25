==================================
明文 SDK 介绍
==================================

RoboMaster EP 最重要的一个功能是支持明文 SDK，包含各个内置模块和拓展模块的控制接口，以及视频流、音频流的输出接口。 EP 支持 USB、 WIFI、 UART 等多种接入方式，用户可根据平台接口选择任意方式接入。

明文 SDK 极大的丰富了 EP 的扩展性，使其能够方便地与 :doc:`第三方平台通信 <../third_part_comm>`，提供了二次开发的可能性。下面将使用 **Wi-Fi 直接连接** 方式（其他连接模式请参考 :doc:`建立连接 <./connection>`），以完成 **控制发射器发射** 功能为例，介绍SDK中明文协议的使用。

开发前的准备
------------

1. 准备一台 PC 电脑，需具备 Wi-Fi 功能
2. PC 上搭建 Python 3.x 环境，安装方式请参考 `Python Getting Started <https://www.python.org/about/gettingstarted/>`_ 

建立连接
---------

1. 开启电源

	开启机器人电源，切换智能中控的连接模式开关至 **直连模式**，如下图所示：

	.. image:: ../images/direct_connection_change.png

2. 建立Wi-Fi连接

	打开电脑的无线网络访问列表，选择位于机身贴纸上对应的 Wi-Fi 名称，输入 8 位密码，选择连接

3. 准备连接脚本

	在完成 Wi-Fi 后，我们还需要编程与机器人建立 TPC/IP 连接，并在对应的端口上传输特定的 **明文协议**，就可以实现相应的控制，更多 **明文协议** 请参考 :doc:`协议内容 <./protocol_api>`。

	这里我们以 Python 编程语言为例，编写脚本来完成 *建立控制连接，接收用户指令，传输明文协议* 的过程，达到控制机器人的目的。

	参考代码如下

.. code-block:: python 
	:linenos:

	# -*- encoding: utf-8 -*-
	# 测试环境: Python 3.6 版本

	import socket
	import sys

	# 直连模式下，机器人默认 IP 地址为 192.168.2.1, 控制命令端口号为 40923
	host = "192.168.2.1"
	port = 40923

	def main():

		address = (host, int(port))

		# 与机器人控制命令端口建立 TCP 连接
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		print("Connecting...")

		s.connect(address)

		print("Connected!")

		while True:

			# 等待用户输入控制指令
			msg = input(">>> please input SDK cmd: ")

			# 当用户输入 Q 或 q 时，退出当前程序
			if msg.upper() == 'Q':
				break

			# 添加结束符
			msg += ';'

			# 发送控制命令给机器人
			s.send(msg.encode('utf-8'))

			try:
				# 等待机器人返回执行结果
				buf = s.recv(1024)

				print(buf.decode('utf-8'))
			except socket.error as e:
				print("Error receiving :", e)
				sys.exit(1)
			if not len(buf):
				break

		# 关闭端口连接
		s.shutdown(socket.SHUT_WR)
		s.close()

	if __name__ == '__main__':
		main()

4. 将上述代码保存为 rm_sdk.py

5. 运行脚本
	
	运行 rm_sdk.py 文件 (Windows系统在安装完成Python环境后可直接双击 \*.py 文件运行，若无法运行，请按键 ``win+r`` 并输入 ``cmd``，按回车后打开命令运行, 键入 ``python rm_sdk.py`` 运行；Linux系统请按键 ``ctrl+alt+t`` 打开命令行键入 ``python rm_sdk.py``)

6. 建立 TCP/IP 控制连接

	当运行窗口输出 ``Connecting...`` 时，代表正在尝试与机器人建立连接，当运行窗口输出 ``Connected!;`` 时，表示已经成功建立控制连接。


使能 SDK 模式
------------------

要进行 SDK 控制，我们需要控制机器人进入 SDK 模式。 在上述 Python 运行窗口输入 *command* 命令，按回车键，程序将会发送该命令至机器人，返回 *ok* 即机器人成功进入 SDK 模式::

	>>> please input SDK cmd: command
	ok

成功进入 SDK 模式后，我们就可以输入控制命令来控制机器人了。

发送控制命令
------------------

继续输入 *blaster fire* ，返回 *ok* ，同时，发射器会发射一次::

	>>> please input SDK cmd: blaster fire
	ok

此时，您可以输入其他控制指令来进行机器人控制，更多控制指令请参考 :doc:`明文协议 <./apis>`。

退出 SDK 模式
------------------

在完成所有控制指令之后，我们需要退出 SDK 模式，这样机器人的其他功能才可以正常使用。

输入 *quit*, 退出 SDK 模式，退出 SDK 模式后无法继续使用 SDK 功能，若要使用，请重新输入 *command* 进入 SDK 模式::

	>>> please input SDK cmd: quit
	ok

小结
------------------

上面我们通过与机器人建立物理连接，与机器人建立 TCP/IP 控制连接，控制机器人进入 SDK 模式，发送控制指令，退出 SDK 模式等几个步骤，实现了通过 SDK 对机器人进行相关的控制功能。您可以通过增加其中 *发送控制指令* 部分的内容，来实现更为复杂的逻辑，完成更为有趣的功能。

其中 Python 编程控制部分，如果您更熟悉其他语言的使用，也可以使用其他语言完成整个控制流程。

如果您手边的设备不支持 Wi-Fi ，无法使用 **Wi-Fi 直接连接**，可以参考 :doc:`连接 <./connection>` 使用其他连接模式。

以上就是 SDK 快速入门内容，更多使用细节请参见 :doc:`SDK文档 <./connection>`，更多示例代码请参见 `RoboMaster Sample Code <https://github.com/dji-sdk/RoboMaster-SDK>`_。
