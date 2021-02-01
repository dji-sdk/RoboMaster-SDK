.. _multi_robot_EP:

###############################
RoboMaster SDK 多機編隊EP
###############################

這裡以window 64位為例，介紹robomaster SDK的EP編隊教程：

Demo的環境要求及物料清單
--------------------------

1. **編程環境**

（1）下載RoboMaster-SDK壓縮包，Github下載鏈接：`RoboMaster-SDK壓縮包 <https://github.com/dji-sdk/RoboMaster-SDK/>`_ (備用Gitee下載鏈接：`RoboMaster-SDK壓縮包 <https://gitee.com/xitinglin/RoboMaster-SDK>`_)，下載步驟：

* 點擊 ``Code`` ,點擊 ``Download ZIP`` 下載壓縮包。

.. image:: ./../images/download_sdk.png
            :scale: 50%
            :align: center

* 解壓下載完的RoboMaster-SDK-master.zip壓縮包：

.. image:: ./../images/zip.png
			:align: center

* 壓縮文件包含：

	1.VS相關運行庫： **VisualCppRedist_AIO_20200707.exe**

	2.VS build tool:  **visualcppbuildtools_full.exe**

	3.RoboMaster SDK示例代碼:  **examples**

	4.第三方庫安裝腳本： **lib_install.bat**


（2）安裝必要的VC庫：

運行RoboMaster-SDK壓縮包中的 **VisualCppRedist_AIO_20200707.exe** ，並完成安裝：

.. image:: ./../images/vc_exe.png

.. warning:: 不安裝VC庫，使用SDK，會引起以下問題:

	.. image:: ./../images/libmedia_err.png

（3）安裝VS Build Tool：

運行RoboMaster-SDK壓縮包中的 **visualcppbuildtools_full.exe** ，並完成安裝：

.. image:: ./../images/vs_build_tool.png

（4）python環境安裝：

a. 從 `python 官網上 <https://www.python.org/downloads/windows/>`_ 找到可以下載的安裝包，以Python3.7.8 為例，選擇安裝文件進行下載。

.. warning:: 請確保下載的 `python.exe` 是64位的，python sdk適配3.6.6以上python版本，否則會影響python sdk的使用，如果電腦上已經安裝了python環境，建議卸載重新安裝。

.. image:: ./../images/win_python_setup1.png


b. 步驟（1）：確認安裝包版本是 ``64-bit``, 否則會影響Python sdk使用。

   步驟（2）：勾選 ``Add Python 3.7 to Path``。

   步驟（3）：選擇 ``Install Now`` 進行安裝，如下圖所示。

.. image:: ./../images/win_python_setup2.png


c. 安裝完成後按 ``win+r``，在彈出窗口中輸入 ``cmd`` 打開命令提示符界面，在命令行裡面輸入 ``python``, 確認 Python 3.7.8 安裝成功。

.. image:: ./../images/python_version.png


（5）python第三方依賴庫安裝：

    方法一：在下載的RoboMaster-SDK壓縮包目錄(:file:`RoboMaster-SDK-master/lib_install.bat` )中找到lib_install.bat文件，鼠標右鍵單擊該文件，選擇以管理員身份運行即可。

    方法二：安裝RoboMaster SDK，點擊電腦開始菜單，在搜索框中輸入 ``cmd`` ，在搜索結果中，對著命令提示符程序，單擊鼠標右鍵，菜單中點擊選擇 ``以管理員身份運行`` ,並依次輸入以下指令::

		pip install robomaster
		pip install netaddr
		pip install netifaces
		pip install myqr

2. **EP小車**

- 數量：6台EP步兵車

.. tip:: 如果沒有6台EP小車，2台EP小車也可以，後面的示例代碼請更換參考 :file:`/examples/15_muti_robot/multi_ep/02_two_ep_demo.py`

- 固件版本：01.01.0500

.. tip:: 固件版本升級可以通過Robomaster App進行，確保固件版本號在01.01.0500及以上版本。

EP組網連接
----------------
步驟1：首先將每台EP機器人設置為路由器組網模式並將電腦與機器人加入到同一個局域網內，實現組網連接

如下圖所示：

.. image:: ./../images/networking_connection_change.png
            :align: center

步驟2：生成二維碼

- 參考下載的RoboMaster-SDK壓縮包目錄下的示例代碼 :file:`/examples/01_robot/05_sta_conn_helper.py` 目錄下的例程

.. literalinclude:: ./../../../examples/01_robot/05_sta_conn_helper.py
   :language: python
   :linenos:
   :lines: 17-

.. warning:: 示例代碼13行中的：

		info = helper.build_qrcode_string(ssid="RoboMaster_SDK_WIFI", password="12341234")

		`ssid` （路由器名稱）和 `password` (路由器密碼)，需要根據實際的路由器信息進行填寫

- 運行示例代碼，會出現二維碼圖片，按下機器人智能中控上的掃碼連接按鍵，掃瞄二維碼進行組網連接。

	.. image:: ./../images/networking_connection_key.png
            :align: center

- 運行結果::

    Connected!

同時機器人的燈效變為白色呼吸變為青綠色常亮。

.. note:: 一共6台EP小車需要連接WiFi，首次逐個連接6台EP小車時，連接每台小車都要重複運行示例代碼，連接完成後，下次重啟小車時會自動連接。


運行多機編隊示例代碼
--------------------------------------

- 參考下載的RoboMaster-SDK壓縮包目錄下的示例代碼 :file:`/examples/15_muti_robot/multi_ep/03_six_ep_demo.py` 目錄下的例程

1. 待每台機器人連接同一個路由器成功後，需手動修改示例代碼中的機器人SN編號，每台機器人的SN編號位於智能中控的標籤中，如下圖所示：

.. image:: ./../images/sn_num.jpg
            :scale: 40%
            :align: center

2.編輯示例代碼，找到示例代碼的203行：

	.. literalinclude:: ./../../../examples/15_multi_robot/multi_ep/03_six_ep_demo.py
	   :language: python
	   :linenos:
	   :lines: 203-204

	根據機器人的SN依次修改示例代碼裡的SN。

3. 根據6個SN的順序，依次按照下圖擺放6台機器人，箭頭方向為機器人朝向。

.. image:: ./../images/6EPlocate.png
            :scale: 50%
            :align: center


運行修改後的示例程序
----------------------

- 打開 :file:`/examples/15_muti_robot/multi_ep/` 目錄，按住鍵盤shift，然後再目錄任意空白處單擊鼠標右鍵，單擊選擇 「在此處打開Powershell窗口」 ，或 「在此處打開命令窗口」

- 運行代碼,命令窗口輸入::

	python 03_six_ep_demo.py
