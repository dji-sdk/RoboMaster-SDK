==================================
明文 SDK 介紹
==================================

RoboMaster EP 最重要的一個功能是支持明文 SDK，包含各個內置模塊和拓展模塊的控制接口，以及視頻流、音頻流的輸出接口。 EP 支持 USB、 WIFI、 UART 等多種接入方式，用戶可根據平台接口選擇任意方式接入。

明文 SDK 極大的豐富了 EP 的擴展性，使其能夠方便地與 :doc:`第三方平台通信 <../third_part_comm>`，提供了二次開發的可能性。下面將使用 **Wi-Fi 直接連接** 方式（其他連接模式請參考 :doc:`建立連接 <./connection>`），以完成 **控制發射器發射** 功能為例，介紹SDK中明文協議的使用。

開發前的準備
------------

1. 準備一台 PC 電腦，需具備 Wi-Fi 功能
2. PC 上搭建 Python 3.x 環境，安裝方式請參考 `Python Getting Started <https://www.python.org/about/gettingstarted/>`_ 

建立連接
---------

1. 開啟電源

	開啟機器人電源，切換智能中控的連接模式開關至 **直連模式**，如下圖所示：

	.. image:: ../images/direct_connection_change.png

2. 建立Wi-Fi連接

	打開電腦的無線網絡訪問列表，選擇位於機身貼紙上對應的 Wi-Fi 名稱，輸入 8 位密碼，選擇連接

3. 準備連接腳本

	在完成 Wi-Fi 後，我們還需要編程與機器人建立 TPC/IP 連接，並在對應的端口上傳輸特定的 **明文協議**，就可以實現相應的控制，更多 **明文協議** 請參考 :doc:`協議內容 <./protocol_api>`。

	這裡我們以 Python 編程語言為例，編寫腳本來完成 *建立控制連接，接收用戶指令，傳輸明文協議* 的過程，達到控制機器人的目的。

	參考代碼如下

.. code-block:: python 
	:linenos:

	# -*- encoding: utf-8 -*-
	# 測試環境: Python 3.6 版本

	import socket
	import sys

	# 直連模式下，機器人默認 IP 地址為 192.168.2.1, 控制命令端口號為 40923
	host = "192.168.2.1"
	port = 40923

	def main():

		address = (host, int(port))

		# 與機器人控制命令端口建立 TCP 連接
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		print("Connecting...")

		s.connect(address)

		print("Connected!")

		while True:

			# 等待用戶輸入控制指令
			msg = input(">>> please input SDK cmd: ")

			# 當用戶輸入 Q 或 q 時，退出當前程序
			if msg.upper() == 'Q':
				break

			# 添加結束符
			msg += ';'

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

		# 關閉端口連接
		s.shutdown(socket.SHUT_WR)
		s.close()

	if __name__ == '__main__':
		main()

4. 將上述代碼保存為 rm_sdk.py

5. 運行腳本
	
	運行 rm_sdk.py 文件 (Windows系統在安裝完成Python環境後可直接雙擊 \*.py 文件運行，若無法運行，請按鍵 ``win+r`` 並輸入 ``cmd``，按回車後打開命令運行, 鍵入 ``python rm_sdk.py`` 運行；Linux系統請按鍵 ``ctrl+alt+t`` 打開命令行鍵入 ``python rm_sdk.py``)

6. 建立 TCP/IP 控制連接

	當運行窗口輸出 ``Connecting...`` 時，代表正在嘗試與機器人建立連接，當運行窗口輸出 ``Connected!;`` 時，表示已經成功建立控制連接。


使能 SDK 模式
------------------

要進行 SDK 控制，我們需要控制機器人進入 SDK 模式。 在上述 Python 運行窗口輸入 *command* 命令，按回車鍵，程序將會發送該命令至機器人，返回 *ok* 即機器人成功進入 SDK 模式::

	>>> please input SDK cmd: command
	ok

成功進入 SDK 模式後，我們就可以輸入控制命令來控制機器人了。

發送控制命令
------------------

繼續輸入 *blaster fire* ，返回 *ok* ，同時，發射器會發射一次::

	>>> please input SDK cmd: blaster fire
	ok

此時，您可以輸入其他控制指令來進行機器人控制，更多控制指令請參考 :doc:`明文協議 <./apis>`。

退出 SDK 模式
------------------

在完成所有控制指令之後，我們需要退出 SDK 模式，這樣機器人的其他功能才可以正常使用。

輸入 *quit*, 退出 SDK 模式，退出 SDK 模式後無法繼續使用 SDK 功能，若要使用，請重新輸入 *command* 進入 SDK 模式::

	>>> please input SDK cmd: quit
	ok

小結
------------------

上面我們通過與機器人建立物理連接，與機器人建立 TCP/IP 控制連接，控制機器人進入 SDK 模式，發送控制指令，退出 SDK 模式等幾個步驟，實現了通過 SDK 對機器人進行相關的控制功能。您可以通過增加其中 *發送控制指令* 部分的內容，來實現更為複雜的邏輯，完成更為有趣的功能。

其中 Python 編程控制部分，如果您更熟悉其他語言的使用，也可以使用其他語言完成整個控制流程。

如果您手邊的設備不支持 Wi-Fi ，無法使用 **Wi-Fi 直接連接**，可以參考 :doc:`連接 <./connection>` 使用其他連接模式。

以上就是 SDK 快速入門內容，更多使用細節請參見 :doc:`SDK文檔 <./connection>`，更多示例代碼請參見 `RoboMaster Sample Code <https://github.com/dji-sdk/RoboMaster-SDK>`_。
