.. _conn:


###############################
RoboMaster SDK 和機器人建立連接
###############################

.. _EpConn:

EP連接方式
************

Robomaster SDK 支持3種與EP的連接方式：WiFi 直連模式，WiFi 組網模式和 USB(RNDIS) 連接模式。

1. **WIFI直連** ：

*Wi-Fi 直連* ：通過將機器人設置為直連模式，並連接機器人的 Wi-Fi 熱點進行接入，Wi-Fi 直連模式下，機器人默認 IP 為 192.168.2.1

- 開啟機器人電源，切換智能中控的連接模式開關至 **直連模式**，如下圖所示：

	.. image:: ./../images/direct_connection_change.png
            :scale: 70%
            :align: center

- 準備具有WIFI連接功能的設備，例如：DJI 妙算、Jetson Nano 或 PC：

	.. image:: ./../images/wifi_direct.png
		    :align: center

    .. centered:: DJI 妙算、Jetson Nano 或 PC 通過 WIFI 直連 到 EP

- 參考sdk代碼 :file:`/examples/01_robot/04_ap_conn.py` 目錄下的例程（`GitHub RoboMaster SDK repository <https://github.com/dji-sdk/robomaster-sdk>`_）

.. literalinclude:: ./../../../examples/01_robot/04_ap_conn.py
   :language: python
   :linenos:
   :lines: 17-

- 運行結果::

    Robot Version: xx.xx.xx.xx


2. **USB連接**

*USB 連接* ：通過機器人的智能中控上的 USB 端口接入，機器人默認 IP 為 192.168.42.2

USB 連接模式，實質上是使用 RNDIS 協議，將機器人上的 USB 設備虛擬為一張網卡設備，
通過 USB 發起 TCP/IP 連接更多 RNDIS 內容請參見 `RNDIS Wikipedia <https://www.wikipedia.org/wiki/RNDIS>`_。

- 選擇具有 TypeA USB 接口，並支持 RNDIS 功能的第三方平台，這邊列舉樹莓派的連接，圖中藍線即為USB連接，紅線為供電線：

	.. image:: ./../images/raspberry.png
		    :align: center

	.. centered:: 樹莓派連接示意圖

- 參考sdk代碼 :file:`/examples/01_robot/06_rndis_conn.py` 目錄下的例程（`GitHub RoboMaster SDK repository <https://github.com/dji-sdk/robomaster-sdk>`_）

.. literalinclude:: ./../../../examples/01_robot/06_rndis_conn.py
   :language: python
   :linenos:
   :lines: 17-

- 運行結果::

    Robot Version: xx.xx.xx.xx


3. **組網連接** ：

*Wi-Fi 組網* ：通過將機器人設置為組網模式，並將計算設備與機器人加入到同一個局域網內，實現組網連接

- 開啟機器人電源，切換智能中控的連接模式開關至 **組網模式**

	.. image:: ./../images/networking_connection_change.png
            :scale: 50%
            :align: center

- DJI 妙算、Jetson Nano 或 PC 和 EP 連接到同一個局域網後和 EP 進行通信。

	.. image:: ./../images/wifi_sta.png
		    :align: center

	.. centered:: DJI 妙算、Jetson Nano 或 PC 路由連接至 EP

- 安裝myqr庫生成二維碼，按 ``win+r``，在彈出窗口中輸入 ``cmd`` 打開命令提示符界面，在命令行裡面輸入::

   pip install myqr

- 參考sdk代碼 :file:`/examples/01_robot/05_sta_conn_helper.py` 目錄下的例程（`GitHub RoboMaster SDK repository <https://github.com/dji-sdk/robomaster-sdk>`_）

.. literalinclude:: ./../../../examples/01_robot/05_sta_conn_helper.py
   :language: python
   :linenos:
   :lines: 17-

.. warning:: 示例代碼13行中的，`ssid` （路由器名稱）和 `password` (路由器密碼)，需要根據實際的路由器信息進行填寫

- 運行示例代碼，會出現二維碼圖片，按下機器人智能中控上的掃碼連接按鍵，掃瞄二維碼進行組網連接。

	.. image:: ./../images/networking_connection_key.png
            :align: center

- 運行結果::

    Connected!

同時機器人的燈效變為白色呼吸變為青綠色常亮。

.. tip:: 支持在組網模式下通過SN連接指定的機器人，用戶通過在初始化時給 `sn` 參數賦值完成對機器人 sn 的輸入，
  參考例程 :file:`/examples/01_robot/05_sta_conn_sn.py` （`GitHub RoboMaster SDK repository <https://github.com/dji-sdk/robomaster-sdk>`_）。在不指定 sn 時，SDK默認與搜索到的第一台機器人建立連接。

    .. literalinclude:: ./../../../examples/01_robot/05_sta_conn_sn.py
       :language: python
       :linenos:
       :lines: 17-

.. _TelloConn:

教育無人機系列連接方式
**********************

教育無人機目前主要包括 Tello EDU 以及 Tello Talent，Robomaster SDK支持通過WIFI直連模式與這兩款產品建立連接。

1. **WIFI直連** ：

*Wi-Fi 直連* ：通過將機器人設置為直連模式，並連接機器人的 WIFI 熱點進行接入，WIFI 直連模式下，機器人默認 IP 為 192.168.10.1

- 首先將機器人設置為 WIFI 直連模式

    -  *Tello EDU* : 短按圖中紅色剪頭所示電源按鍵，等待黃燈快閃開機完成，機器人出廠默認即為 WIFI 直連模式，如果開機時為組網模式，
       可以通過電源按鍵重置 WIFI：在開機狀態下，長按電源鍵 5s，期間狀態指示燈將熄滅後再閃爍黃燈。
       狀態指示燈顯示黃燈快閃後， WIFI 的 SSI 和密碼將重置為出廠設置，默認無密碼

	.. image:: ./../images/tello_power.png
            :scale: 50%
            :align: center

    -  *Tello Talent* :: 開啟機器人電源，切換擴展模塊的模式開關至 **直連模式**，如下圖所示：

	.. image:: ./../images/direct_connection_change.png
            :scale: 70%
            :align: center

- 準備具有WIFI連接功能的設備連接教育無人機的 WIFI，例如：DJI 妙算、Jetson Nano 或 PC：

- 參考sdk代碼 :file:`/examples/12_drone/01_ap_conn.py` 目錄下的例程（`GitHub RoboMaster SDK repository <https://github.com/dji-sdk/robomaster-sdk>`_）

.. literalinclude:: ./../../../examples/12_drone/01_ap_conn.py
   :language: python
   :linenos:
   :lines: 17-

- 運行結果::

    Drone SDK Version: xx.xx.xx.xx


2. **組網模式** ：

*組網模式* ：將機器人設置為組網模式，並連接SDK運行設備所在的局域網進行接入，

- 首先將飛機設置為 *直連模式*，並且與運行SDK的設備連接，具體操作參考上一小節

- 運行提供的示例程序 :file:`/examples/12_drone/23_set_sta.py` （`GitHub RoboMaster SDK repository <https://github.com/dji-sdk/robomaster-sdk>`_），
  將程序中的 `ssis` 與 `password` 參數改為當前使用的路由器的賬號與密碼

.. literalinclude:: ./../../..//examples/12_drone/23_set_sta.py
   :language: python
   :linenos:
   :lines: 17-

- 切換擴展模塊的模式開關至組網模式，之後機器會自動連接到指定的路由器所在的局域網內

- 將運行SDK的設備也連接至該局域網內，此時SDK與機器即在同一網絡內

通訊方式
**********

EP通訊方式
___________

Robomaster SDK 與EP的3種連接方式在通訊協議上支持 TCP 和 UDP 通訊。

======== ======================== ==================================
 參數          TCP                    UDP
======== ======================== ==================================
可靠性	      可靠	                  不可靠
連接性	      面向連接                無連接
效率	       低	                    高
場景	   對數據準確性要求高	      對數據傳輸的實時性要求高
======== ======================== ==================================

.. tip:: 機器人要實時的控制運動的可以選用 UDP, 機器人進行事件型控制可以選用 TCP

用戶可以根據自己的運用場景去設置對應的通訊方式
更多TCP通訊內容可以參考：`TCP Wikipedia <https://en.wikipedia.org/wiki/Transmission_Control_Protocol>`_ 
，UDP通訊可以參考：`UDP Wikipedia <https://en.wikipedia.org/wiki/User_Datagram_Protocol>`_。

1. TCP通訊

- 參考sdk代碼 :file:`/examples/01_robot/07_tcp_protocol.py` 目錄下的例程（`GitHub RoboMaster SDK repository <https://github.com/dji-sdk/robomaster-sdk>`_）

.. literalinclude:: ./../../../examples/01_robot/07_tcp_protocol.py
   :language: python
   :linenos:
   :lines: 17-

- 組網連接

這邊可以根據代碼第8行中的 *connect_type* 參數進行修改 :file:`sta` 對應組網連接，:file:`ap` 對應WIFI直連，:file:`rndis` 對應USB連接。

- 運行程序，並得到結果返回::

    Robot Version: xx.xx.xx.xx

2. UDP 通訊

- 參考sdk代碼 :file:`/examples/01_robot/08_udp_protocol.py` 目錄下的例程（`GitHub RoboMaster SDK repository <https://github.com/dji-sdk/robomaster-sdk>`_）

.. literalinclude:: ./../../../examples/01_robot/08_udp_protocol.py
   :language: python
   :linenos:
   :lines: 17-

- 進行組網連接

這邊可以根據代碼第8行中的 *connect_type* 參數進行修改 :file:`sta` 對應組網連接，:file:`ap` 對應WIFI直連，:file:`rndis` 對應USB連接

.. tip:: 不同的通訊方式，實際是根據代碼第8行中的對 *robot.initialize()* 函數的 *proto_type* 傳遞的參數來變更的，:file:`tcp` 對應TCP通訊， :file:`udp` 對應UDP通訊

- 運行程序，並得到結果返回::

    Robot Version: xx.xx.xx.xx

教育無人機 通訊方式
___________________________

目前 Tello EDU 與 Tello Talent 只支持UDP通信方式，因此不需要額外的配置

