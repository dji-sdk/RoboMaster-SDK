================
編隊控制
================

介紹
------------

編隊控制功能是通過明文 SDK 對連接在同一個局域網內的多個機器人進行動作編排，實現整體控制的功能。用戶可以使用該功能進行更複雜的動作控制，實現編隊舞蹈，很具有觀賞性。

原理為多台機器人通過 WIFI 路由器模式在同一個局域網內建立連接後，用戶在 PC 上通過 Python 腳本與多台機器人通信，同時向多台機器人下發明文 SDK 指令，從而實現編隊控制的功能。在本章節中主要介紹一個用 Python 腳本通過明文 SDK 實現編隊控制的簡單示例。

示例環境
------------

- 硬件設備：路由器、兩台 EP 機器人、 PC
- Python版本：Python 3.6

建立多機連接
------------

將 EP 機器人設置為 WIFI 路由器模式，使用 APP 將參與編隊控制的 EP 依次接入同一個路由器中，連接成功後打開 APP 設置中的連接頁面，記錄 EP 的 IP 地址。具體步驟請參考 :ref:`wifi_sta`。

運行示例程序
------------
1. 將IP地址依次填入參考代碼中的 IP_LIST 列表中，並將腳本代碼保存為 ep.py。

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
			#實例化機器人
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

2. 運行腳本

- Windows系統：完成Python環境後可直接點擊 ep.py 啟動腳本。
- Linux系統：在命令終端輸入 python ep.py 啟動腳本。

3. 運行效果

編隊控制的多台機器人云台步調一致的在 YAW 軸方向往復運動。

	.. image:: ../images/form_control.gif
		:align: center

4. 運行結果

命令行端口輸出多台機器人與主機之間的明文通訊數據。

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
