========
接入方式
========

*********
连接方式
*********

机器人支持多种连接方式，可通过任意一种连接方式接入使用 SDK 功能

- **直接连接** ：

    1. *Wi-Fi 直连* ：通过将机器人设置为直连模式，并连接机器人的 Wi-Fi 热点进行接入

    2. *USB 连接* ：通过机器人的智能中控上的 USB 端口接入（需支持 RNDIS 功能）

    3. *UART 连接* ：通过机器人的运动控制器上的 UART 接口接入
	

- **组网连接** ：

     *Wi-Fi 组网* ：通过将机器人设置为组网模式，并将计算设备与机器人加入到同一个局域网内，实现组网连接

*********
连接参数
*********

Wi-Fi 直连/Wi-Fi 组网/USB 连接方式请参考以下参数配置：

- **IP 地址说明**：

    - Wi-Fi 直连模式下，机器人默认 IP 为 192.168.2.1

    - Wi-Fi 组网模式下，机器人 IP 由路由器动态分配，可通过监听 *IP 广播* 数据端口来获取当前局域网内机器人 IP 地址来进行连接
 
    - USB 连接模式下，需要计算设备支持 RNDIS 功能，机器人默认 IP 为 192.168.42.2

- **端口及连接方式说明**：

========= ======== ========== =================================================
数据       端口号   连接方式   说明
========= ======== ========== =================================================
视频流     40921     TCP       需执行开启视频流推送命令，才有数据输出
音频流     40922     TCP       需执行开启音频流推送命令，才有数据输出
控制命令   40923     TCP       可通过当前通道使能 SDK 模式，参见 **SDK 模式控制**
消息推送   40924     UDP       需执行开启消息推送命令，才有数据输出
事件上报   40925     TCP       需执行开启事件上报命令，才有数据输出
IP 广播    40926     UDP       当机器人未与任何设备建立连接时，会有数据输出
========= ======== ========== =================================================

2. UART 连接方式请参考以下 UART 参数配置

======== ======== ======== ========
波特率    数据位   停止位   校验位
======== ======== ======== ========
115200     8        1        None
======== ======== ======== ========

.. warning:: UART 连接方式下的数据说明：

    UART 连接方式下，仅提供 *控制命令/消息推送/事件上报* 数据，如需 *视频流/音频流* 数据，请使用 *Wi-Fi/USB* 连接模式

*********
连接示例
*********

下面我们将以 Python 编程语言为基础，介绍多种连接方式的使用范例。以下所有示例中，默认 PC 上需要集成 Python 3.x 环境（安装方式请参考 `Python Getting Started <https://www.python.org/about/gettingstarted/>`_），后面不再赘述。

.. _wifi_direct:

WIFI 直连模式
-------------

- **环境准备**

1. 准备一台 PC 电脑，需具备 Wi-Fi 功能。

- **建立连接**

1. 开启电源

	开启机器人电源，切换智能中控的连接模式开关至 **直连模式**，如下图所示：

	.. image:: ../images/direct_connection_change.png

2. 建立 Wi-Fi 连接

	打开电脑的无线网络访问列表，选择位于机身贴纸上对应的 Wi-Fi 名称，输入 8 位密码，选择连接

3. 准备连接脚本

	建立 Wi-Fi 连接后，我们还需要编程与机器人建立 TPC/IP 连接 机器人开放多个连接端口可供连接，我们首先应完成 **控制命令端口** 的连接（直连模式下机器人 IP 地址为 ``192.168.2.1``, 控制命令端口号: ``40923``），以使能机器人 SDK 模式。

	这里我们以 Python 编程语言为例，编写脚本来完成 *建立控制连接，使能 SDK 模式* 功能

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

4. 将上述代码保存为 rm_direct_connection_sdk.py

5. 运行脚本
	
	**Windows 系统** 在安装完成 Python 环境后可直接双击\*.py 文件运行，若无法运行，请按 ``win+r`` 并输入 ``cmd``，按回车后打开命令运行, 键入 ``python rm_direct_connection_sdk.py`` 运行；

	**Linux 系统** 请按 ``ctrl+alt+t`` 打开命令行键入 ``python rm_direct_connection_sdk.py`` 运行

6. 建立 TCP/IP 控制连接

	当运行窗口输出 ``Connecting...`` 时，代表正在尝试与机器人建立连接，当运行窗口输出 ``Connected!;`` 时，表示已经成功建立控制连接。

- **验证**

在成功建立控制连接后，在命令行里输入 ``command``, 机器人返回 ``ok;``，则表示已经完成连接，并且机器人进入 SDK 模式成功，之后您就可以输入任意控制指令控制机器人了。

- **其他**

UART物理链路连接示例请参考：:doc:`UART <../extension_module/uart>`

.. _wifi_sta:

WIFI 路由器模式
-------------------------

- **环境准备**

1. 准备一台 PC 电脑，具备网络功能（Wi-Fi 或者有线网络皆可）
2. 准备一台家用路由器

- **建立连接**

1. 开启电源

	开启机器人电源，切换智能中控的连接模式开关至 **组网模式**

	.. image:: ../images/networking_connection_change.png


2. 建立组网连接
	
	Wi-Fi：

		若使用 Wi-Fi 连接，请将 PC 电脑通过 Wi-Fi 连接至路由器上

	有线网络：

		若使用有线网络连接，请将 PC 电脑通过网线连接至路由器的 LAN 口

	确保 PC 已经接入路由器后，打开 RoboMaster App，进入组网连接页面，按下机器人智能中控上的扫码连接按键，扫描二维码进行组网连接，直到连接成功。

	.. image:: ../images/networking_connection_key.png

3. 获取机器人在局域网内的 IP 地址

	在完成组网连接后，我们的 PC 机已经和机器人处于同一个局域网内，接下来需要编程与机器人建立 TPC/IP 连接，并连接到 **控制命令端口** 端口，以使能机器人 SDK 模式。

	若您使用的路由器开启了 DHCP 服务，则机器人的 IP 地址为路由器动态分配，我们需要进一步获取机器人在局域网内的 IP 地址。这里提供两种办法获取：

		1. 若您通过 RoboMaster App 进行的组网连接，则进入 RoboMaster App的 *设置->连接* 页面，机器人在局域网内的 IP 地址会在此处显示。

		2. 若您通过其他方式进行的组网连接，则需要通过 *监听机器人地址广播* 来获取机器人在局域网内的 IP 地址，更多细节请参考 **广播** 部分。

		参考代码如下

		.. code-block:: python 
			:linenos:

			# -*- encoding: utf-8 -*-
			import socket

			ip_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

			# 绑定 IP 广播端口
			ip_sock.bind(('0.0.0.0', 40926))

			# 等待接收数据
			ip_str = ip_sock.recvfrom(1024)

			# 输出数据
			print(ip_str)

		将上述代码保存为 rm_get_robot_ip.py, 运行上述代码，命令行输出::

			robot ip 192.168.0.115

		我们可以看到，通过 *监听机器人地址广播* 可以获取到机器人在局域网内的 IP 地址为 ``192.168.0.115``

3. 准备连接脚本

	我们已经获取到机器人的 IP 地址，这里我们仍以 Python 编程语言为例，编写脚本来完成 *建立控制连接，使能 SDK 模式* 功能

	参考代码如下

	.. code-block:: python 
		:linenos:

		# -*- encoding: utf-8 -*-
		# 测试环境：Python 3.6 版本

		import socket
		import sys

		# 组网模式下，机器人当前 IP 地址为 192.168.0.115, 控制命令端口号为 40923
		# 机器人 IP 地址根据实际 IP 进行修改
		host = "192.168.0.115"
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

4. 将上述代码保存为 rm_networking_connection_sdk.py

5. 运行脚本
	
	**Windows 系统**：在安装完成 Python 环境后可直接双击\*.py 文件运行，若无法运行，请按 ``win+r`` 并输入 ``cmd``，按回车后打开命令运行, 键入 ``python rm_networking_connection_sdk.py`` 运行；

	**Linux 系统** 请按：``ctrl+alt+t`` 打开命令行键入 ``python rm_networking_connection_sdk.py`` 运行

6. 建立 TCP/IP 控制连接

	当运行窗口输出 ``Connecting...`` 时，代表正在尝试与机器人建立连接，当运行窗口输出 ``Connected!;`` 时，表示已经成功建立控制连接。

- **验证**

在成功建立控制连接后，在命令行里输入 ``command``, 机器人返回 ``ok;``，则表示已经完成连接，并且机器人进入 SDK 模式成功，之后你就可以输入任意控制指令进行机器人控制了。

.. _usb_conn:

USB 连接
-----------

USB 连接模式，实质上是使用 RNDIS 协议，将机器人上的 USB 设备虚拟为一张网卡设备，通过 USB 发起 TCP/IP 连接。更多 RNDIS 内容请参见 `RNDIS Wikipedia <https://www.wikipedia.org/wiki/RNDIS>`_。

- **环境准备**

1. 准备一台具备 RNDIS 功能的 PC 电脑（请确认 PC 电脑上已经配置好 RNDIS 功能）
2. 准备一根 Micro-USB 数据线


- **建立连接**

1. 开启电源

	开启机器人电源，无需关心连接模式开关位置

2. 建立 USB 连接

	将 USB 数据线接入到机器人智能中控上的 USB 口，另一端与电脑相连

3. 测试连接

	打开命令行窗口，运行::

		ping 192.168.42.2

	若命令行输出通信成功，则表示链路正常，可以进行下一步，如::

		PING 192.168.42.2 (192.168.42.2) 56(84) bytes of data.
		64 bytes from 192.168.42.2: icmp_seq=1 ttl=64 time=0.618 ms
		64 bytes from 192.168.42.2: icmp_seq=2 ttl=64 time=1.21 ms
		64 bytes from 192.168.42.2: icmp_seq=3 ttl=64 time=1.09 ms
		64 bytes from 192.168.42.2: icmp_seq=4 ttl=64 time=0.348 ms
		64 bytes from 192.168.42.2: icmp_seq=5 ttl=64 time=0.342 ms

		--- 192.168.42.2 ping statistics ---
		5 packets transmitted, 5 received, 0% packet loss, time 4037ms
		rtt min/avg/max/mdev = 0.342/0.723/1.216/0.368 ms

	若命令行输出 **无法访问...** 或者显示超时，则需要检查 PC 上 RNDIS 服务是否配置正常，并重启小车重试，如::

		PING 192.168.42.2 (192.168.42.2) 56(84) bytes of data.

		--- 192.168.42.2 ping statistics ---

4 packets transmitted, 0 received, 100% packet loss, time 3071ms

4. 准备连接

	连接过程与 :ref:`wifi_direct` -> **准备连接脚本** 类似，需要将机器人 IP 地址替换为 USB 模式下的 IP 地址，其余代码与步骤保持不变即可，这里不再赘述。

	参考代码变更如下

	.. code-block:: python 
		:linenos:

		# -*- encoding: utf-8 -*-
		# 测试环境: Python 3.6 版本

		import socket
		import sys

		# USB 模式下，机器人默认 IP 地址为 192.168.42.2, 控制命令端口号为 40923
		host = "192.168.42.2"
		port = 40923

		# other code

- **验证**

在成功建立控制连接后，在命令行里输入 ``command``, 机器人返回 ``ok;``，则表示已经完成连接，并且机器人进入 SDK 模式成功，之后你就可以输入任意控制指令进行机器人控制了。

.. _uart_conn:

UART 连接
-----------

- **环境准备**

1. 一台 PC 电脑，并确定已安装 USB 转串口模块驱动
2. USB 转串口模块
3. 三根杜邦线

- **建立连接**

1. 开启电源

	开启机器人电源，无需关心连接模式开关位置

2. 连接 UART

	将杜邦线插在机器人底盘主控上的 UART 接口上，分别插在 GND, RX, TX 引脚上，另一端对应插在 USB 转串口模块的 GND, TX, RX 引脚

3. 配置 UART，建立通信连接

	这里，我们仍以 Python 编程为例，进行 Windows 系统下 UART 相关配置。

	1. 确认 PC 已识别 USB 转串口模块，并在 **电脑设备管理器** 中的 **端口** 里确认对应的串口号，如 COM3。

	2. 安装 serial 模块::

		pip install pyserial

	3. 编写代码进行 UART 控制，参考代码如下：

	.. code-block:: python
		:linenos:

		# -*- encoding: utf-8 -*-
		# 测试环境：Python 3.6 版本
		import serial

		ser = serial.Serial()

		# 配置串口 波特率 115200，数据位 8 位，1 个停止位，无校验位，超时时间 0.2 秒
		ser.port = 'COM3'
		ser.baudrate = 115200
		ser.bytesize = serial.EIGHTBITS
		ser.stopbits = serial.STOPBITS_ONE
		ser.parity = serial.PARITY_NONE
		ser.timeout = 0.2

		# 打开串口
		ser.open()
		 
		while True:

			# 等待用户输入控制指令
			msg = input(">>> please input SDK cmd: ")

			# 当用户输入 Q 或 q 时，退出当前程序
			if msg.upper() == 'Q':
				break

			# 添加结束符
			msg += ';'

			ser.write(msg.encode('utf-8'))

		 	recv = ser.readall()

		 	print(recv.decode('utf-8'))

		# 关闭串口
		ser.close()

	4. 将上述程序保存为 rm_uart.py, 并运行

- **验证**

在成功建立控制连接后，在命令行里输入 ``command;``, 机器人返回 ``ok;``，则表示已经完成连接，并且机器人进入 SDK 模式成功，之后您就可以输入任意控制指令进行机器人控制了。


.. tip:: 示例代码

	更多连接相关示例代码请参考 `RoboMaster Sample Code <https://github.com/dji-sdk/RoboMaster-SDK>`_