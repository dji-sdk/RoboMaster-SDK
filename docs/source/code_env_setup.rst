==================================
 編程環境安裝
==================================

介紹
-----------

用戶在 PC 上通過 WIFI、 USB 和 UART 跟 EP 建立連接後，可以使用明文 SDK 跟 EP 進行通信，進行更複雜的二次開發。用戶可以在 PC 上使用 C++、 C#、 Python 或是其他語言進行編程，用戶可根據自身開發能力選擇開發語言。

為了讓用戶盡快熟悉 EP 的各個模塊和功能，並方便使用本網站中的 Python 示例代碼，我們介紹一下 Python 在 PC 上的安裝步驟。


在 Windows 上安裝 Python
-------------------------

**環境：** Windows 10 64 位

1. 從python官網  `python 官網鏈接 <https://www.python.org/downloads/windows/>`_ 找到可以下載的安裝包，以Python3.7.8 為例，選擇安裝文件進行下載。

.. warning:: 請確保下載的 `python.exe` 是64位的，python sdk適配3.6.6以上至3.8.9版本python版本，否則會影響python sdk的使用，切記。

.. image:: ./images/win_python_setup1.png


2. 步驟（1）：確認安裝包版本是 ``64-bit``, 否則會影響Python sdk使用。

   步驟（2）：勾選 ``Add Python 3.7 to Path``。

   步驟（3）：選擇 ``Install Now`` 進行安裝，如下圖所示。

.. image:: ./images/win_python_setup2.png


3. 安裝完成後按 ``win+r``，在彈出窗口中輸入 ``cmd`` 打開命令提示符界面，在命令行裡面輸入 ``python``, 確認 Python 3.7.8 安裝成功。

.. image:: ./images/python_version.png

.. note:: cmd窗口會顯示對應的版本信息，否則，請從第一步重新安裝


在 Ubuntu 上安裝 Python
-------------------------

**環境：** ubuntu 16.04 64 位，Python 3.7.8

1. Ubuntu16.04 默認安裝了Python2.7和3.5，輸入命令 ``python``，可以查看 Python 默認版本。請注意，系統自帶的python千萬不能卸載。

2. 輸入如下命令安裝 python 3.7 軟件包：

::

	sudo add-apt-repository ppa:jonathonf/python-3.7
	sudo apt-get update
	sudo apt-get install python3.7

3. 輸入如下命令，調整 Python3 的優先級，使得 Python 3.7 優先級較高。

::

		sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
		sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 2
		sudo update-alternatives --install /usr/bin/python python /usr/bin/python2 100
		sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 150

4. 此時再輸入命令 ``python`` ，確認 Python 3.7 安裝成功。


