=======================================
快速了解 RoboMaster SDK 的使用
=======================================

介紹
-----

RoboMaster EP 作為一款教育機器人，具有強大的擴展性和程式設計可能性，在程式設計方面提供了 Scratch、Python 以及 SDK，方便使用者對 RoboMaster EP 進行二次開發，擴展更加豐富的功能。

下面將使用 **Wi-Fi 直接連接** 方式（其他連接模式請參考 :doc:`連接 <./sdk/connection>`），來示範 **控制發射器發射** 功能，介紹 SDK 中明文協定的使用。

開發前的準備
------------

1. 準備一部個人電腦，需具備 Wi-Fi 功能。
2.電腦需搭建 Python 3.x 環境，安裝方式請查閱 `Python Getting Started <https://www.python.org/about/gettingstarted/>`_ 

建立連接
---------

1. 開啟電源

	開啟機器人電源，智能中控的連接模式開關切換至 **直連模式**

	.. image:: images/direct_connection_change.png

2. 建立 Wi-Fi 連接

	打開電腦的無線網路訪問清單，選擇位於機身貼紙上對應的 Wi-Fi 名稱，輸入 8 位密碼，選擇連接

3. 準備連接腳本

	在完成 Wi-Fi 連接後，我們還需要設計程式與機器人建立 TPC/IP 連接，並於對應的埠上傳輸特定的 **明文協議**，就可以實現相應的控制，更多 **明文協議** 請參考 :doc:`協議內容 <./sdk/protocol_api>`。

	這裡我們以 Python 程式設計語言為例，編寫腳本來完成 *建立控制連接，接收使用者指令，傳輸明文協議* 的過程，達到控制機器人的目的。

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

		# 關閉埠連接
		s.shutdown(socket.SHUT_WR)
		s.close()

	if __name__ == '__main__':
		main()

4. 將上述代碼存儲為 rm_sdk.py

5. 運行 rm_sdk.py 文檔 (Windows系統在安裝完成 Python 環境後可直接按兩下 \*.py 文檔運行，若無法運行，請按鍵 ``win+r`` 並輸入 ``cmd``，按回車後打開命令運行, 鍵入 ``python rm_sdk.py`` 運行；Linux系統請按鍵 ``ctrl+alt+t`` 打開命令列鍵入 ``python rm_sdk.py``)

6. 建立 TCP/IP 控制連接

	當運行視窗輸出 ``Connecting...`` 時，代表正在嘗試與機器人建立連接，當運行視窗輸出 ``Connected!`` 時，表示已經成功建立控制連接。


使能 SDK 模式
------------------

要進行 SDK 控制，我們需要控制機器人進入 SDK 模式。 在上述 Python 運行視窗輸入 *command* 命令，按回車鍵，程式將會發送該命令至機器人，返回 *ok* 即機器人成功進入 SDK 模式::

	>>> please input SDK cmd: command
	ok

成功進入 SDK 模式後，我們就可以輸入控制命令來進行機器人的控制了。

發送控制命令
------------------

續輸入 *blaster fire* ，返回 *ok* ，同時，發射器會發射一次::

	>>> please input SDK cmd: blaster fire
	ok

此時，您可以輸入其他控制指令來進行機器人控制，更多控制指令請參考 :doc:`協議 <./sdk/api>`

退出 SDK 模式
------------------

在完成我們的所有控制指令之後，我們需要退出 SDK 模式，這樣我們機器人的其他功能才可以正常使用。

輸入 *quit*, 退出 SDK 模式，退出 SDK 模式後無法繼續使用 SDK 功能，若要使用，請重新輸入 *command* 進入 SDK 模式::

	>>> please input SDK cmd: quit
	quit sdk mode successfully

小結
------------------

上面我們通過與機器人建立物理連接，與機器人建立 TCP/IP 控制連接，控制機器人進入 SDK 模式，發送控制指令，退出 SDK 模式等幾個步驟，實現了使用 SDK 對機器人進行相關的控制功能。您可以通過增加其中 *發送控制指令* 部分的內容，來實現更為複雜的邏輯，完成更為有趣的功能。

其中 Python 程式設計控制部分，如果您更熟悉其他語言的使用，也可以使用其他語言完成整個控制流程。

如果您手邊的設備不支援 Wi-Fi，無法使用 **Wi-Fi 直接連接**，可以參考 :doc:`連接 <./sdk/connection>` 使用其他連接模式。

以上就是 SDK 快速入門內容，更多使用細節請參見 :doc:`SDK文檔 <./sdk/connection>`。，更多示例代碼請參見 `RoboMaster Sample Code <https://github.com/dji-sdk/RoboMaster-SDK>`_