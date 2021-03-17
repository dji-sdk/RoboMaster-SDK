.. _conn:


###############################
RoboMaster SDK 和机器人建立连接
###############################

EP固件升级
************

请通过RoboMaster App查看EP固件，确保EP固件版本在01.01.0500及其以上版本，如果不是请通过RoboMaster APP进行升级，不然会影响到RoboMaster SDK的使用。

.. _EpConn:

EP连接方式
************

Robomaster SDK 支持3种与EP的连接方式：WiFi 直连模式，WiFi 组网模式和 USB(RNDIS) 连接模式。

1. **WIFI直连** ：

*Wi-Fi 直连* ：通过将机器人设置为直连模式，并连接机器人的 Wi-Fi 热点进行接入，Wi-Fi 直连模式下，机器人默认 IP 为 192.168.2.1

- 开启机器人电源，切换智能中控的连接模式开关至 **直连模式**，如下图所示：

	.. image:: ./../images/direct_connection_change.png
            :scale: 70%
            :align: center

- 准备具有WIFI连接功能的设备，例如：DJI 妙算、Jetson Nano 或 PC：

	.. image:: ./../images/wifi_direct.png
		    :align: center

    .. centered:: DJI 妙算、Jetson Nano 或 PC 通过 WIFI 直连 到 EP

- 参考sdk代码 :file:`/examples/01_robot/04_ap_conn.py` 目录下的例程（`GitHub RoboMaster SDK repository <https://github.com/dji-sdk/robomaster-sdk>`_）

.. literalinclude:: ./../../../examples/01_robot/04_ap_conn.py
   :language: python
   :linenos:
   :lines: 17-

- 运行结果::

    Robot Version: xx.xx.xx.xx


2. **USB连接**

*USB 连接* ：通过机器人的智能中控上的 USB 端口接入，机器人默认 IP 为 192.168.42.2

USB 连接模式，实质上是使用 RNDIS 协议，将机器人上的 USB 设备虚拟为一张网卡设备，
通过 USB 发起 TCP/IP 连接更多 RNDIS 内容请参见 `RNDIS Wikipedia <https://www.wikipedia.org/wiki/RNDIS>`_。

- 选择具有 TypeA USB 接口，并支持 RNDIS 功能的第三方平台，这边列举树莓派的连接，图中蓝线即为USB连接，红线为供电线：

	.. image:: ./../images/raspberry.png
		    :align: center

	.. centered:: 树莓派连接示意图

- 参考sdk代码 :file:`/examples/01_robot/06_rndis_conn.py` 目录下的例程（`GitHub RoboMaster SDK repository <https://github.com/dji-sdk/robomaster-sdk>`_）

.. literalinclude:: ./../../../examples/01_robot/06_rndis_conn.py
   :language: python
   :linenos:
   :lines: 17-

- 运行结果::

    Robot Version: xx.xx.xx.xx


3. **组网连接** ：

*Wi-Fi 组网* ：通过将机器人设置为组网模式，并将计算设备与机器人加入到同一个局域网内，实现组网连接

- 开启机器人电源，切换智能中控的连接模式开关至 **组网模式**

	.. image:: ./../images/networking_connection_change.png
            :scale: 50%
            :align: center

- DJI 妙算、Jetson Nano 或 PC 和 EP 连接到同一个局域网后和 EP 进行通信。

	.. image:: ./../images/wifi_sta.png
		    :align: center

	.. centered:: DJI 妙算、Jetson Nano 或 PC 路由连接至 EP

- 安装myqr库生成二维码，按 ``win+r``，在弹出窗口中输入 ``cmd`` 打开命令提示符界面，在命令行里面输入::

   pip install myqr

- 参考sdk代码 :file:`/examples/01_robot/05_sta_conn_helper.py` 目录下的例程（`GitHub RoboMaster SDK repository <https://github.com/dji-sdk/robomaster-sdk>`_）

.. literalinclude:: ./../../../examples/01_robot/05_sta_conn_helper.py
   :language: python
   :linenos:
   :lines: 17-

.. warning:: 示例代码13行中的，`ssid` （路由器名称）和 `password` (路由器密码)，需要根据实际的路由器信息进行填写

- 运行示例代码，会出现二维码图片，按下机器人智能中控上的扫码连接按键，扫描二维码进行组网连接。

	.. image:: ./../images/networking_connection_key.png
            :align: center

- 运行结果::

    Connected!

同时机器人的灯效变为白色呼吸变为青绿色常亮。

.. tip:: 支持在组网模式下通过SN连接指定的机器人，用户通过在初始化时给 `sn` 参数赋值完成对机器人 sn 的输入，
  参考例程 :file:`/examples/01_robot/05_sta_conn_sn.py` （`GitHub RoboMaster SDK repository <https://github.com/dji-sdk/robomaster-sdk>`_）。在不指定 sn 时，SDK默认与搜索到的第一台机器人建立连接。

    .. literalinclude:: ./../../../examples/01_robot/05_sta_conn_sn.py
       :language: python
       :linenos:
       :lines: 17-

.. _TelloConn:

教育无人机系列连接方式
**********************

教育无人机目前主要包括 Tello EDU 以及 Tello Talent，Robomaster SDK支持通过WIFI直连模式与这两款产品建立连接。

1. **WIFI直连** ：

*Wi-Fi 直连* ：通过将机器人设置为直连模式，并连接机器人的 WIFI 热点进行接入，WIFI 直连模式下，机器人默认 IP 为 192.168.10.1

- 首先将机器人设置为 WIFI 直连模式

    -  *Tello EDU* : 短按图中红色剪头所示电源按键，等待黄灯快闪开机完成，机器人出厂默认即为 WIFI 直连模式，如果开机时为组网模式，
       可以通过电源按键重置 WIFI：在开机状态下，长按电源键 5s，期间状态指示灯将熄灭后再闪烁黄灯。
       状态指示灯显示黄灯快闪后， WIFI 的 SSI 和密码将重置为出厂设置，默认无密码

	.. image:: ./../images/tello_power.png
            :scale: 50%
            :align: center

    -  *Tello Talent* :: 开启机器人电源，切换扩展模块的模式开关至 **直连模式**，如下图所示：

	.. image:: ./../images/direct_connection_change.png
            :scale: 70%
            :align: center

- 准备具有WIFI连接功能的设备连接教育无人机的 WIFI，例如：DJI 妙算、Jetson Nano 或 PC：

- 参考sdk代码 :file:`/examples/12_drone/01_ap_conn.py` 目录下的例程（`GitHub RoboMaster SDK repository <https://github.com/dji-sdk/robomaster-sdk>`_）

.. literalinclude:: ./../../../examples/12_drone/01_ap_conn.py
   :language: python
   :linenos:
   :lines: 17-

- 运行结果::

    Drone SDK Version: xx.xx.xx.xx


2. **组网模式** ：

*组网模式* ：将机器人设置为组网模式，并连接SDK运行设备所在的局域网进行接入，

- 首先将飞机设置为 *直连模式*，并且与运行SDK的设备连接，具体操作参考上一小节

- 运行提供的示例程序 :file:`/examples/12_drone/23_set_sta.py` （`GitHub RoboMaster SDK repository <https://github.com/dji-sdk/robomaster-sdk>`_），
  将程序中的 `ssis` 与 `password` 参数改为当前使用的路由器的账号与密码

.. literalinclude:: ./../../..//examples/12_drone/23_set_sta.py
   :language: python
   :linenos:
   :lines: 17-

- 切换扩展模块的模式开关至组网模式，之后机器会自动连接到指定的路由器所在的局域网内

- 将运行SDK的设备也连接至该局域网内，此时SDK与机器即在同一网络内

通讯方式
**********

EP通讯方式
___________

Robomaster SDK 与EP的3种连接方式在通讯协议上支持 TCP 和 UDP 通讯。

======== ======================== ==================================
 参数          TCP                    UDP
======== ======================== ==================================
可靠性	      可靠	                  不可靠
连接性	      面向连接                无连接
效率	       低	                    高
场景	   对数据准确性要求高	      对数据传输的实时性要求高
======== ======================== ==================================

.. tip:: 机器人要实时的控制运动的可以选用 UDP, 机器人进行事件型控制可以选用 TCP

用户可以根据自己的运用场景去设置对应的通讯方式
更多TCP通讯内容可以参考：`TCP Wikipedia <https://en.wikipedia.org/wiki/Transmission_Control_Protocol>`_ 
，UDP通讯可以参考：`UDP Wikipedia <https://en.wikipedia.org/wiki/User_Datagram_Protocol>`_。

1. TCP通讯

- 参考sdk代码 :file:`/examples/01_robot/07_tcp_protocol.py` 目录下的例程（`GitHub RoboMaster SDK repository <https://github.com/dji-sdk/robomaster-sdk>`_）

.. literalinclude:: ./../../../examples/01_robot/07_tcp_protocol.py
   :language: python
   :linenos:
   :lines: 17-

- 组网连接

这边可以根据代码第8行中的 *connect_type* 参数进行修改 :file:`sta` 对应组网连接，:file:`ap` 对应WIFI直连，:file:`rndis` 对应USB连接。

- 运行程序，并得到结果返回::

    Robot Version: xx.xx.xx.xx

2. UDP 通讯

- 参考sdk代码 :file:`/examples/01_robot/08_udp_protocol.py` 目录下的例程（`GitHub RoboMaster SDK repository <https://github.com/dji-sdk/robomaster-sdk>`_）

.. literalinclude:: ./../../../examples/01_robot/08_udp_protocol.py
   :language: python
   :linenos:
   :lines: 17-

- 进行组网连接

这边可以根据代码第8行中的 *connect_type* 参数进行修改 :file:`sta` 对应组网连接，:file:`ap` 对应WIFI直连，:file:`rndis` 对应USB连接

.. tip:: 不同的通讯方式，实际是根据代码第8行中的对 *robot.initialize()* 函数的 *proto_type* 传递的参数来变更的，:file:`tcp` 对应TCP通讯， :file:`udp` 对应UDP通讯

- 运行程序，并得到结果返回::

    Robot Version: xx.xx.xx.xx

教育无人机 通讯方式
___________________________

目前 Tello EDU 与 Tello Talent 只支持UDP通信方式，因此不需要额外的配置

