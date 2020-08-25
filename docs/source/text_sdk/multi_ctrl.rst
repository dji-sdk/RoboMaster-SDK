================
编队控制
================

介绍
------------

编队控制功能是通过明文 SDK 对连接在同一个局域网内的多个机器人进行动作编排，实现整体控制的功能。用户可以使用该功能进行更复杂的动作控制，实现编队舞蹈，很具有观赏性。

原理为多台机器人通过 WIFI 路由器模式在同一个局域网内建立连接后，用户在 PC 上通过 Python 脚本与多台机器人通信，同时向多台机器人下发明文 SDK 指令，从而实现编队控制的功能。在本章节中主要介绍一个用 Python 脚本通过明文 SDK 实现编队控制的简单示例。

示例环境
------------

- 硬件设备：路由器、两台 EP 机器人、 PC
- Python版本：Python 3.6

建立多机连接
------------

将 EP 机器人设置为 WIFI 路由器模式，使用 APP 将参与编队控制的 EP 依次接入同一个路由器中，连接成功后打开 APP 设置中的连接页面，记录 EP 的 IP 地址。具体步骤请参考 :ref:`wifi_sta`。

运行示例程序
------------
1. 将IP地址依次填入参考代码中的 IP_LIST 列表中，并将脚本代码保存为 ep.py。

	.. code-block:: python
		:linenos:

		#!/usr/bin/env python3
		# coding=utf-8

		import sys
		import time
		import threading
		import socket

		IP_LIST = ['192.168.1.103', '192.168.1.117']
		EP_DICT = {}

		class EP:
			def __init__(self, ip):
				self._IP = ip
				self.__socket_ctrl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.__socket_isRelease = True
				self.__socket_isConnect = False
				self.__thread_ctrl_recv = threading.Thread(target=self.__ctrl_recv)
				self.__seq = 0
				self.__ack_list = []
				self.__ack_buf = 'ok'

			def __ctrl_recv(self):
				while self.__socket_isConnect and not self.__socket_isRelease:
					try:
						buf = self.__socket_ctrl.recv(1024).decode('utf-8')
						print('%s:%s' % (self._IP, buf))
						buf_list = buf.split(' ')
						if 'seq' in buf_list:
							self.__ack_list.append(int(buf_list[buf_list.index('seq') + 1]))
						self.__ack_buf = buf
					except socket.error as msg:
						print('ctrl %s: %s' % (self._IP, msg))

			def start(self):
				try:
					self.__socket_ctrl.connect((self._IP, 40923))
					self.__socket_isConnect = True
					self.__socket_isRelease = False
					self.__thread_ctrl_recv.start()
					self.command('command')
					self.command('robot mode free')
				except socket.error as msg:
					print('%s: %s' % (self._IP, msg))

			def exit(self):
				if self.__socket_isConnect and not self.__socket_isRelease:
					self.command('quit')
				self.__socket_isRelease = True
				try:
					self.__socket_ctrl.shutdown(socket.SHUT_RDWR)
					self.__socket_ctrl.close()
					self.__thread_ctrl_recv.join()
				except socket.error as msg:
					print('%s: %s' % (self._IP, msg))

			def command(self, cmd):
				self.__seq += 1
				cmd = cmd + ' seq %d;' % self.__seq
				print('%s:%s' % (self._IP, cmd))
				self.__socket_ctrl.send(cmd.encode('utf-8'))
				timeout = 2
				while self.__seq not in self.__ack_list and timeout > 0:
					time.sleep(0.01)
					timeout -= 0.01
				if self.__seq in self.__ack_list:
					self.__ack_list.remove(self.__seq)
				return self.__ack_buf

		if __name__ == "__main__":
			#实例化机器人
			for ip in IP_LIST:
				print('%s connecting...' % ip)
				EP_DICT[ip] = EP(ip)
				EP_DICT[ip].start()

			for ip in IP_LIST:
				EP_DICT[ip].command('gimbal moveto p 0 y 0 vp 90 vy 90 wait_for_complete false')
			time.sleep(3)

			while True:
				for ip in IP_LIST:
					EP_DICT[ip].command('gimbal moveto p 0 y 45 vp 90 vy 90 wait_for_complete false')
				time.sleep(3)
				for ip in IP_LIST:
					EP_DICT[ip].command('gimbal moveto p 0 y -45 vp 90 vy 90 wait_for_complete false')
				time.sleep(3)
			for ip in IP_LIST:
				EP_DICT[ip].exit()

2. 运行脚本

- Windows系统：完成Python环境后可直接点击 ep.py 启动脚本。
- Linux系统：在命令终端输入 python ep.py 启动脚本。

3. 运行效果

编队控制的多台机器人云台步调一致的在 YAW 轴方向往复运动。

	.. image:: ../images/form_control.gif
		:align: center

4. 运行结果

命令行端口输出多台机器人与主机之间的明文通讯数据。

	.. code-block:: python
		:linenos:

		192.168.1.103 connecting...
		192.168.1.103:command seq 1
		192.168.1.103:ok seq 1
		192.168.1.103:robot mode free seq 2
		192.168.1.103:ok seq 2
		192.168.1.117 connecting...
		192.168.1.117:command seq 1
		192.168.1.117:ok seq 1
		192.168.1.117:robot mode free seq 2
		192.168.1.117:ok seq 2
		192.168.1.103:gimbal moveto p 0 y 0 vp 90 vy 90 wait_for_complete false seq 3
		192.168.1.103:ok seq 3
		192.168.1.117:gimbal moveto p 0 y 0 vp 90 vy 90 wait_for_complete false seq 3
		192.168.1.117:ok seq 3
