========
連接
========

*********
連接方式
*********

機器人支援多種連接方式，可通過任意一種連接方式接入使用 SDK 功能

- **直接連接** ：

    1. *Wi-Fi 直連* ：通過將機器人設定為直連模式，並連接機器人的 Wi-Fi 熱點進行接入

    2. *USB 連接* ：通過機器人的智能中控上的 USB 埠接入（需支援 RNDIS 功能）

    3. *UART 連接* ：通過機器人的運動控制器上的 UART 接口接入

- **組網連接** ：

    1. *Wi-Fi 組網* ：通過將機器人設定為組網模式，並將計算設備與機器人加入到同一個局域網內，實現組網連接

*********
連接參數
*********

1. Wi-Fi 直連/Wi-Fi 組網/USB 連接方式請參考以下參數配置：

- **IP 地址說明**：

    - Wi-Fi 直連模式下，機器人預設 IP 為 192.168.2.1

    - Wi-Fi 組網模式下，機器人 IP 由路由器動態分配，可通過監聽 *IP 廣播* 連接埠來獲取當前局域網內機器人 IP 位址來進行連接

    - USB 連接模式下，需要計算設備支援 RNDIS 功能，機器人預設 IP 為 192.168.42.2

- **連接埠及連接方式說明**：

========= ======== ========== ===================================================
資料      連接埠號  連接方式   說明
========= ======== ========== ===================================================
影片流     40921     TCP       需執行開啟影片流推送命令，才有資料輸出
音訊流     40922     TCP       需執行開啟音訊流推送命令，才有資料輸出
控制命令   40923     TCP       可通過當前通道使能 SDK 模式，參見 **SDK 模式控制**
消息推送   40924     UDP       需執行開啟消息推送命令，才有資料輸出
事件上報   40925     TCP       需執行開啟事件上報命令，才有資料輸出
IP 廣播    40926     UDP       當機器人未與任何設備建立連接時，會有資料輸出
========= ======== ========== ===================================================

2. UART 連接方式請參考以下 UART 參數配置

======== ======== ======== ========
波特率   數據位元 停止位   校验位
======== ======== ======== ========
115200     8        1        None
======== ======== ======== ========

.. warning:: UART 連接方式下的資料說明：

    UART 連接方式下，僅提供 *控制命令/消息推送/事件上報* 資料，如需 *影片流/音訊流* 資料，請使用 *Wi-Fi/USB* 連接模式

*********
連接示例
*********

下面我們將以 Python 程式設計語言為基礎，介紹多種連接方式的使用範例。以下所有示例中，預設個人電腦需要集成 Python 3.x 環境（安裝方式請參考 `Python Getting Started <https://www.python.org/about/gettingstarted/>`_），後面不再贅述。

Wi-Fi 直連
-------------

- **環境準備**

1. 準備一部電腦，需具備 Wi-Fi 功能。

- **建立連接**

1. 開啟電源

	開啟機器人電源，切換智能中控的連接模式開關至 **直連模式**

	.. image:: ../images/direct_connection_change.png

2. 建立 Wi-Fi 連接

	打開電腦的無線網路訪問清單，選擇位於機身貼紙上對應的 Wi-Fi 名稱，輸入 8 位密碼，選擇連接

3. 準備連接腳本

	建立 Wi-Fi 連接後，我們還需要設計程式與機器人建立 TPC/IP 連接 機器人開放多個連接埠以供連接，我們首先應完成 **控制命令埠** 的連接（直連模式下機器人 IP 位址為 ``192.168.2.1``, 控制命令埠號: ``40923``），以使能機器人 SDK 模式。

	這裡我們以 Python 程式設計語言為例，編寫腳本來完成 *建立控制連接，使能 SDK 模式* 功能

	參考代碼如下

	.. code-block:: python 
		:linenos:

		# 測試環境: Python 3.6 版本

		import socket
		import sys

		# 直連模式下，機器人預設 IP 位址為 192.168.2.1, 控制命令埠號為 40923
		host = "192.168.2.1"
		port = 40923

		def main():

			address = (host, int(port))

			# 與機器人控制命令埠建立 TCP 連接
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			print("Connecting...")

			s.connect(address)

			print("Connected!")

			while True:

				# 等待使用者輸入控制指令
				msg = input(">>> please input SDK cmd: ")

				# 當用戶輸入 Q 或 q 時，退出當前程式
				if msg.upper() == 'Q':
					break

				# 發送控制命令給機器人
				s.send(msg.encode('utf-8'))

				try:
					# 等待機器人返回執行結果

					buf = s.recv(1024)

					print(buf.decode('utf-8'))
				except socket.error as e:
					print("Error receiving :", e)
					sys.exit(1)
				if not len(buf):
					break

			# 關閉連接埠連接
			s.shutdown(socket.SHUT_WR)
			s.close()	

		if __name__ == '__main__':
			main()

4. 將上述代碼保存為 rm_direct_connection_sdk.py

5. 運行腳本
	
	**Windows 系統** 在安裝完成 Python 環境後可直接按兩次\*.py 文檔運行，若無法運行，請按 ``win+r`` 並輸入 ``cmd``，按回車後打開命令運行, 鍵入 ``python rm_direct_connection_sdk.py`` 運行；

	**Linux 系統** 請按 ``ctrl+alt+t`` 打開命令列鍵入 ``python rm_direct_connection_sdk.py`` 運行

6. 建立 TCP/IP 控制連接

	當運行視窗輸出 ``Connecting...`` 時，代表正在嘗試與機器人建立連接，當運行視窗輸出 ``Connected!`` 時，表示已經成功建立控制連接。

- **驗證**

在成功建立控制連接後，在命令列裡輸入 ``command``, 機器人返回 ``ok``，則表示已經完成連接，並且機器人進入 SDK 模式成功，之後您就可以輸入任意控制指令進行機器人控制了。

Wi-Fi/有線網路組網連接
-------------------------

- **環境準備**

1. 準備一台個人電腦，具備網路功能（Wi-Fi 或者有線網路皆可）
2. 準備一台家用路由器


- **建立连接**

1. 開啟電源

	開啟機器人電源，切換智能中控的連接模式開關至 **組網模式**

	.. image:: ../images/networking_connection_change.png


2. 建立組網連接
	
	Wi-Fi：

		若使用 Wi-Fi 連接，請將個人電腦通過 Wi-Fi 與路由器連接

	有線網路：

		若使用有線網路連接，請將個人電腦通過網線連接至路由器的 LAN 口

	確保個人已經接入路由器後，打開 RoboMaster 程式，進入組網連接頁面，按下機器人智能中控上的掃碼連接按鍵，掃描二維碼進行組網連接，直到連接成功。

	.. image:: ../images/networking_connection_key.png

3. 獲取機器人在局域網內的 IP 位址

	在完成組網連接後，我們的個人電腦已經和機器人處於同一個局域網內，接下來需要設計程式與機器人建立 TPC/IP 連接，並連接到 **控制命令埠** 埠，以使能機器人 SDK 模式。

	若您使用的路由器開啟了 DHCP 服務，則機器人的 IP 位址為路由器動態分配，我們需要進一步獲取機器人在局域網內的 IP 位址。這裡提供兩種辦法獲取：

		1. 若您通過 RoboMaster 程式進行的組網連接，則進入 RoboMaster 程式的 *設定->連接* 頁面，機器人在局域網內的 IP 位址會在此處顯示。

		2. 若您通過其他方式進行的組網連接，則需要通過 *監聽機器人位址廣播* 來獲取機器人在局域網內的 IP 位址，更多細節請參考 **廣播** 部分。

		參考代碼如下

		.. code-block:: python 
			:linenos:

			import socket

			ip_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

			# 綁定 IP 廣播埠
			ip_sock.bind(('0.0.0.0', 40926))

			# 等待接收資料
			ip_str = ip_sock.recvfrom(1024)

			# 輸出數據
			print(ip_str)

		將上述代碼保存為 rm_get_robot_ip.py, 運行上述代碼，命令行輸出：

			robot ip 192.168.0.115

		我們可以看到，通過 *監聽機器人位址廣播* 可以獲取到機器人在局域網內的 IP 位址為 ``192.168.0.115``

3. 準備連接腳本

	我們已經獲取到機器人的 IP 地址，這裡我們仍以 Python 程式設計語言為例，編寫腳本來完成 *建立控制連接，使能 SDK 模式* 功能

	參考代碼如下

	.. code-block:: python 
		:linenos:

		# 測試環境：Python 3.6 版本

		import socket
		import sys

		# 組網模式下，機器人當前 IP 位址為 192.168.0.115, 控制命令埠號為 40923
		# 機器人 IP 位址根據實際 IP 進行修改
		host = "192.168.0.115"
		port = 40923

		def main():

			address = (host, int(port))

			# 與機器人控制命令埠建立 TCP 連接
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			print("Connecting...")

			s.connect(address)

			print("Connected!")

			while True:

				# 等待使用者輸入控制指令
				msg = input(">>> please input SDK cmd: ")

				# 當用戶輸入 Q 或 q 時，退出當前程式
				if msg.upper() == 'Q':
					break

				# 發送控制命令給機器人
				s.send(msg.encode('utf-8'))

				try:
					# 等待機器人返回執行結果
					buf = s.recv(1024)

					print(buf.decode('utf-8'))
				except socket.error as e:
					print("Error receiving :", e)
					sys.exit(1)
				if not len(buf):
					break

			# 關閉連接埠連接
			s.shutdown(socket.SHUT_WR)
			s.close()	

		if __name__ == '__main__':
			main()

4. 將上述代碼保存為 rm_networking_connection_sdk.py

5. 運行腳本
	
	**Windows 系統** 在安裝完成 Python 環境後可直接按兩下\*.py 文檔運行，若無法運行，請按 ``win+r`` 並輸入 ``cmd``，按回車後打開命令運行, 鍵入 ``python rm_networking_connection_sdk.py`` 運行；

	**Linux 系統** 請按 ``ctrl+alt+t`` 打開命令列鍵入 ``python rm_networking_connection_sdk.py`` 運行

6. 建立 TCP/IP 控制連接

	當運行視窗輸出 ``Connecting...`` 時，代表正在嘗試與機器人建立連接，當運行視窗輸出 ``Connected!`` 時，表示已經成功建立控制連接。

- **驗證**

在成功建立控制連接後，在命令列裡輸入 ``command``, 機器人返回 ``ok``，則表示已經完成連接，並且機器人成功進入 SDK 模式，之後您就可以輸入任意控制指令進行機器人控制了。

USB 連接
-----------

USB 連接模式，實質上是使用 RNDIS 協定，將機器人上的 USB 設備虛擬為一張網卡設備，通過 USB 發起 TCP/IP 連接。更多 RNDIS 內容請參見 `RNDIS Wikipedia <https://www.wikipedia.org/wiki/RNDIS>`_

- **環境準備**

1. 準備一台具備 RNDIS 功能的電腦（請確認電腦已經配置好 RNDIS 功能）
2. 準備一條 Micro-USB 數據線


- **建立連接**

1. 開啟電源

	開啟機器人電源，無需關心連接模式開關位置

2. 建立 USB 連接

	將 USB 資料線接入到機器人智能中控上的 USB 口，另一端與電腦相連

3. 測試連接

	打開命令列視窗，運行::

		ping 192.168.42.2

	若命令行輸出通訊成功, 則表示鏈路正常，可以進行下一步，如::

		PING 192.168.42.2 (192.168.42.2) 56(84) bytes of data.
		64 bytes from 192.168.42.2: icmp_seq=1 ttl=64 time=0.618 ms
		64 bytes from 192.168.42.2: icmp_seq=2 ttl=64 time=1.21 ms
		64 bytes from 192.168.42.2: icmp_seq=3 ttl=64 time=1.09 ms
		64 bytes from 192.168.42.2: icmp_seq=4 ttl=64 time=0.348 ms
		64 bytes from 192.168.42.2: icmp_seq=5 ttl=64 time=0.342 ms

		--- 192.168.42.2 ping statistics ---
		5 packets transmitted, 5 received, 0% packet loss, time 4037ms
		rtt min/avg/max/mdev = 0.342/0.723/1.216/0.368 ms	

	若命令行輸出 **無法訪問...** 或者顯示超時，則需要檢查 PC 上 RNDIS 服務是否配置正常，並重啟設備重試，如::

		PING 192.168.42.2 (192.168.42.2) 56(84) bytes of data.

		--- 192.168.42.2 ping statistics ---

4. 準備連接

	連接過程與 `Wi-Fi 直連`_-> **準備連接腳本** 類似，需要將機器人 IP 位址替換為 USB 模式下的 IP 位址，其餘代碼與步驟保持不變即可，這裡不再贅述

	參考代碼變更如下

	.. code-block:: python 
		:linenos:

		# 測試環境: Python 3.6 版本

		import socket
		import sys

		# USB 模式下，機器人預設 IP 位址為 192.168.42.2, 控制命令埠號為 40923
		host = "192.168.42.2"
		port = 40923

		# other code

- **驗證**

在成功建立控制連接後，在命令列裡輸入 ``command``, 機器人返回 ``ok``，則表示已經完成連接，並且機器人成功進入 SDK 模式，之後您就可以輸入任意控制指令進行機器人控制了。


UART 連接
-----------

- **環境準備**

1. 一部電腦，並確定已安裝 USB 轉串口模組驅動
2. USB 轉串口模組
3. 三根杜邦線

- **建立連接**

1. 開啟電源

	开启机器人电源，无需关心连接模式开关位置

2. 連接 UART

	將杜邦線插在機器人底盤主控上的 UART 接口上，分別插在 GND, RX, TX 引腳上，另一端對應插在 USB 轉串口模組的 GND, TX, RX 引腳

3. 配置 UART，建立通訊連接

	這裡，我們仍以 Python 程式設計為例，進行 Windows 系統下 UART 相關配置。

	1. 確認電腦已識別 USB 轉串口模組，並在 **電腦裝置管理員** 中的 **埠** 裡確認對應的串口號，如 COM3。

	2. 安裝 serial 模組::

		pip install pyserial

	3. 編寫代碼進行 UART 控制，參考代碼如下

	.. code-block:: python
		:linenos:

		# 測試環境：Python 3.6 版本
		import serial

		ser = serial.Serial()

		# 配置串口 傳送速率 115200，數據位元 8 位元，1 個停止位，無校驗位，超時時間 0.2 秒
		ser.port = 'COM3'
		ser.baudrate = 115200
		ser.bytesize = serial.EIGHTBITS
		ser.stopbits = serial.STOPBITS_ONE
		ser.parity = serial.PARITY_NONE
		ser.timeout = 0.2

		# 打開串口
		ser.open()
		 
		while True:

			# 等待使用者輸入控制指令
			msg = input(">>> please input SDK cmd: ")

			# 當用戶輸入 Q 或 q 時，退出當前程式
			if msg.upper() == 'Q':
				break

		 	ser.write(msg)

		 	recv = ser.read()

		 	print(recv)

		# 關閉串口
		ser.close()

	4. 將上述程式保存為 rm_uart.py, 並運行

- **驗證**

在成功建立控制連接後，在命令列裡輸入 ``command``, 機器人返回 ``ok``，則表示已經完成連接，並且機器人成功進入 SDK 模式，之後您就可以輸入任意控制指令進行機器人控制了。

.. tip:: 示例代碼                                                               
                                                                                
   更多連接相關示例代碼請參考 `RoboMaster Sample Code <https://github.com/dji-sdk/RoboMaster-SDK>`_
 