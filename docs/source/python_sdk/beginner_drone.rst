.. _beginngerDrone:

###########################################
RoboMaster SDK 新手入門 - 教育系列無人機篇
###########################################

初始化機器人
__________________

在進行與機器人相關的操作之前，需要根據指定的配置初始化機器人對像

- 首先從安裝的 `robomaster` 包中導入 `robot` 模塊::

    from robomaster import robot

- 指定 RoboMaster SDK 的本地ip地址（如需手動指定），在本示例中，查詢得到本地的ip地址為 `192.168.2.20`
  （比如在Windows操作系統下，通過 快捷鍵 `Win` + `R` 調出的窗口中輸入 `cmd`，
  然後在 CMD窗口中輸入 `ipconfig` ， 即可以查看設備ip的信息），
  如需指定ip使用以下語句::

    robomaster.config.LOCAL_IP_STR = "192.168.2.20"

.. tip:: 大部分情況下SDK能夠自動獲取正確的本地ip，無需手動指定這一步驟，但是當SDK運行在多網卡同時使用的設備時，
  自動獲取的ip可能不是與機器人進行連接的ip，此時需要手動指定ip

- 創建 `Drone` 類的實例對像 `tl_drone`， `tl_drone` 即一個機器人的對象::

    tl_drone = robot.Drone()

- 初始化機器人，目前教育系列無人機的初始化不需要傳入任何參數::

    tl_drone.initialize()

至此，機器人的初始化工作就完成了，接下來可以通過相關接口對機器人進行信息查詢、動作控制、多媒體使用等操作，
本文檔將在後面的部分對幾類接口的使用分別進行介紹

獲取模塊對像
__________________

部分 SDK 接口屬於 `Drone` 對像本身，因此可以通過 `Drone` 對像直接調用，
但是一些接口屬於 `Drone` 對像包含的其他模塊，比如飛機電池的信息獲取接口在 `led` 模塊對像中，
飛行器的控制接口在 `flight` 模塊對像中，等等。如果想使用這些接口需要首先獲得相應的對象，
這裡以獲取 `flight` 模塊對像舉例，介紹如何獲取這些對像

- 首先按照 `初始化機器人`_ 章節的介紹完成機器人對象的初始化操作

- 可以使用兩種方法獲取 `flight` 對像

  - 方法一：直接使用 `.` 運算符從 `Drone()` 對像中獲取 `flight` 對像::

        tl_flight = tl_drone.flight

  - 方法二：利用 `Drone` 對象的 `get_module()` 方法獲得指定的對象::

        tl_flight = tl_drone.get_module("flight")

獲取了相關對象，便可以通過該對像調用其所包含的 SDK 接口


釋放機器人資源
__________________

在程序的最後，應該手動釋放機器人對像相關的資源，包括釋放網絡地址、結束相應後台線程、釋放相應地址空間等，
在 `Drone` 對像中，提供了用來釋放相關資源的方法 `close()`，使用方法如下::

    tl_drone.close()

.. tip:: 為了避免一些意外錯誤，記得在程序的最後調用 `close()` 方法哦！

查詢類接口的使用
____________________

查詢類接口即數據獲取類接口，用戶可以通過該類接口獲取機器人自身的狀態信息以及傳感器狀態等信息，
接下來將從查詢機器人SDK固件版本信息與查詢機器人SN號兩個例子來幫助用戶掌握該類型接口的用法

示例一：查詢機器人固件SDK版本
********************************

- 首先按照 `初始化機器人`_ 章節的介紹完成機器人對象的初始化操作

- 使用 `Drone` 對象的 `get_sdk_version()` 方法，方法的返回值即為代表機器人SDK固件版本號的字符串，
  並且將獲取到的版本號打印出來::

    drone_version = tl_drone.get_sdk_version()
    print("Drone sdk version: {0}".format(drone_version))

- 利用 `釋放機器人資源`_ 章節的介紹釋放相關資源

完整的程序參考示例文件 :file:`/examples/12_drone/02_get_version.py`

.. literalinclude:: ./../../../examples/12_drone/02_get_version.py
   :language: python
   :linenos:
   :lines: 17-

示例二：獲取機器人SN號
************************

- 首先按照 `初始化機器人`_ 章節的介紹完成機器人對象的初始化操作

- 利用 `Drone` 對像使用 `get_sn()` 方法，方法的返回值即為代表機器人SN號的字符串，
  並且將獲取到的SN號打印出來::

    SN = tl_drone.get_sn()
    print("drone sn: {0}".format(SN))

- 利用 `釋放機器人資源`_ 章節的介紹釋放相關資源

完整的程序參考示例文件 :file:`/examples/12_drone/03_get_sn.py`

.. literalinclude:: ./../../../examples/12_drone/03_get_sn.py
   :language: python
   :linenos:
   :lines: 17-

設置類接口的使用
_______________________

設置類接口可以完成對機器人的相關模塊的設置，本文檔接下來將通過設置擴展led模塊講解設置類接口的使用

.. tip:: 設置擴展led燈目前只有 Tello Talent 機器支持！

示例一：設置機器人擴展led模塊
********************************

下面介紹如何通過 SDK 實現設置機器人機器人擴展led模塊的操作

- 首先按照 `初始化機器人`_ 章節的介紹完成機器人對象的初始化操作,

- 機器人的裝甲燈設置接口屬於 `Drone`對像包含的 `led` 模塊，因此首先需要獲取 `led` 對象，
  按照 `獲取模塊對像`_ 章節的介紹獲取 `led` 對像, 本示例中使用方法一獲取模塊對像::

    tl_led = tl_robot.led

- 使用 `led` 對像中的 `set_led()` 方法設置機器人的擴展led燈效，
  在使用 `led` 方法時，通過 `r` `g` `b` 參數可以指定led的顏色，這了將其指定為紅色::

    tl_led.set_led(r=255, g=0, b=0)

- 利用 `釋放機器人資源`_ 章節的介紹釋放相關資源

示例程序中提供了一個完整的設置裝甲燈的例程 :file:`/examples/12_drone/20_led.py`，
例程中利用了for循環，實現了led燈的8次顏色變換，每次維持0.5秒鐘

.. literalinclude:: ./../../../examples/12_drone/20_led.py
   :language: python
   :linenos:
   :lines: 17-


動作類接口的使用
_____________________________

動作類接口是用來控制機器人執行某些指定動作的接口，根據動作本身特性的不同，
SDK中包含 *即時動作控制* 與 *任務動作控制* 兩類動作接口。
由於飛機類機器人本身的特性決定必須要起飛後才能進行控制，
因此本文檔將首先會介紹 *任務動作控制*，帶領大家熟悉了飛行類動作之後會再介紹 *即時動作控制* 類的接口使用

任務動作控制
**********************

任務動作是指需要持續一段時間才能完成的動作，比如控制底盤向前運動一米，
底盤對於該動作需要執行一段時間才能到達指定地點。通過 SDK 控制任務動作時，
SDK 將對應的任務發送給機器人，機器人收到任務後會選擇執行/拒絕執行（存在機器人當前時刻無法執行對應任務的情況）並通知 SDK，
如果選擇執行任務，會在任務完成時再次告知 SDK。在使用任務動作控制接口時，用戶需要注意以下兩點：

- 任務動作接口的返回值為 `action` 對象，`action` 對像提供 `wait_for_completed(timeout)` 方法，
  用戶可以通過 `timeout` 參數指定動作的超時時長。當調用 `wait_for_completed(timeout)` 方法時，
  程序會阻塞在該語句，直至動作執行完畢或執行超時


- 同一模塊同一時間只能執行一個動作， 因此同一模塊的任務之間互斥；不同模塊之間的相互獨立，動作可以同時執行。
  比如在使用任務動作控制接口後不立即調用 `wait_for_completed()` 方法時，用戶在控制雲台移動到指定角度的同時可以控制底盤移動到指定位置，
  但是不支持在上次控制雲台的任務動作還未完成時再次發送其他的控制雲台的任務動作


.. tip:: 如果在使用任務動作控制接口時不馬上調用 `wait_for_completed()` 方法，切記程序中要控制好邏輯，
  避免在該任務執行完畢前發送與其互斥的其他任務動作命令！

接下來本文檔會通過控制底盤移動指定距離來幫助大家熟悉該類接口的使用


示例一：控制飛機起飛並前後飛行
+++++++++++++++++++++++++++++++

在本例程中，首先需要控制飛機起飛，之後控制飛機起飛並向前飛行50cm

- 首先按照 `初始化機器人`_ 章節的介紹完成機器人對象的初始化操作

- 飛行控制接口屬於 `flight` 模塊，首先按照 `獲取模塊對像`_ 章節的介紹獲取 `flight` 對像,
  由於本示例中同時也會控制擴展led模塊，因此也需要獲取 `led` 模塊，
  本示例中使用方法一獲取模塊對像::

    tl_flight = tl_drone.flight
    tl_led = tl_drone.led

- 之後控制飛機起飛昇空，控制起飛時通過調用任務動作接口返回的 `action` 中的 `wait_for_completed()` 方法阻塞程序直至起飛完成::

    tl_flight.takeoff().wait_for_completed()

- 接下來會控制飛機向前飛行50cm，本示例為了說明任務類動作的特點，在控制飛機飛行後會設置擴展led燈效。
  使用 `flight` 對像中的 `forward()` 方法控制底盤向前飛行，該方法都只有一個參數 `distance` ， 用來指定飛行距離。
  設置擴展led模塊可以參考 `示例一：設置機器人擴展led模塊`_ 。接下來本文檔會使用三種方法使用任務動作接口


  - 方法一：執行任務動作後，立即調用 `wait_for_completed()` 方法::

     tl_flight.forward(distance=50).wait_for_completed()
     tl_led.set_led(r=255, g=0, b=0)

  - 方法二：在執行其他命令後再調用 `wait_for_completed()` 方法::

     flight_action = tl_flight.forward(distance=50)
     tl_led.set_led(r=255, g=0, b=0)
     flight_action.wait_for_completed()

  - 方法三：不使用 `wait_for_completed()` 方法，利用延時來保證動作執行結束::

     flight_action = tl_flight.forward(distance=50)
     tl_led.set_led(r=255, g=0, b=0)
     time.sleep(8)

  三種任務動作接口的調用形式對應機器人的行為不同，*方法一* 機器人會向前飛行到達指定地點後再將擴展led模塊設置為紅色，
  而 *方法二* 與 *方法三* 向前飛行的過程中將擴展led模塊設置為紅色。


.. note:: *方法二* 與 *方法三* 中，要注意不能在飛行過程使用其他 `ack` 為 `ok/error` 的接口！機器人的 `ack` 參考 《 Tello SDK 使用說明》


.. tip:: 建議使用 *方法一* 以及 *方法二* ，在合適的時機調用 `wait_for_completed()` 是比較安全的做法


- 飛機降落::

    tl_flight.land().wait_for_completed()

- 利用 `釋放機器人資源`_ 章節的介紹釋放相關資源

示例程序中提供了一個完整的控制底盤前後各飛行50cm的例程 :file:`examples/12_drone/07_forward_backward.py`，

.. literalinclude:: ./../../../examples/12_drone/07_forward_backward.py
   :language: python
   :linenos:
   :lines: 17-


即時動作控制
*************

即時控制類動作是指設置後馬上生效的動作，特指宏觀上是「瞬時」執行的動作，
接下來本文檔將通過控制遙控器桿量帶大家熟悉此類動作接口

示例一：控制遙控器桿量
++++++++++++++++++++++++++++

控制遙控器桿量是一種典型的即時控制，發出控制指令後機器人將會立即按照指定速度與方向飛行

- 首先按照 `初始化機器人`_ 章節的介紹完成機器人對象的初始化操作

- 飛行控制接口屬於 `flight` 模塊，首先按照 `獲取模塊對像`_ 章節的介紹獲取 `flight` 對像,
  本示例中使用方法一獲取模塊對像::

    tl_flight = tl_drone.flight

- 之後控制飛機起飛昇空，控制起飛時通過調用任務動作接口返回的 `action` 中的 `wait_for_completed()` 方法阻塞程序直至起飛完成::

    tl_flight.takeoff().wait_for_completed()

- 接下來會控制飛機以指定的速度向左飛行三秒鐘然後停止。
  使用 `flight` 對像中的 `rc()` 方法控制底盤向前飛行，方法有控制橫滾、俯仰、油門、偏航四個速度的參數，可以通過api文檔中的介紹詳細瞭解，
  本示例中令橫滾的控制參數 `a` 的值為 20， 來達到飛機左飛的目的, 在三秒後將飛機的所有速度全設為0，達到停止飛行的目的::

    tl_flight.rc(a=20, b=0, c=0, d=0)
    time.sleep(4)

- 飛機降落::

    tl_flight.land().wait_for_completed()

- 利用 `釋放機器人資源`_ 章節的介紹釋放相關資源

示例程序中提供了一個完整的通過遙控器桿量控制飛機飛行的例程 :file:`examples/12_drone/13_rc.py`，

.. literalinclude:: ./../../../examples/12_drone/13_rc.py
   :language: python
   :linenos:
   :lines: 17-

多媒體接口的使用
______________________________________

教育系列無人機的多媒體部分主要指獲取視頻流

示例一：獲取視頻流
**********************

獲取機器人採集到的視頻流有助於實現一些非常實用的案例，下面本文檔將介紹如何通過 SDK 獲取視頻流

- 首先按照 `初始化機器人`_ 章節的介紹完成機器人對象的初始化操作，
  由於示例中會用到 `camera` 模塊的相關定義，因此還需要導入 `camera` 模塊::

    from robomaster import camera

- 獲取視頻流相關的接口屬於屬於 `camera` 模塊，首先按照 `獲取模塊對像`_ 章節的介紹獲取 `camera` 對像,
  本示例中使用`獲取模塊對像`_ 章節介紹的方法一獲取模塊對像::

    tl_camera= tl_robot.camera

- `camera` 模塊的 `start_video_stream` 方法有兩個參數， `display` 參數指定是否顯示獲取到的視頻流，在本示例中，向大家介紹兩種獲取視頻流的方法，

  - 方法一：獲取視頻流並直接播放顯示十秒::

        tl_camera.start_video_stream(display=True)
        time.sleep(10)
        tl_camera.stop_video_stream()

  - 方法二：獲取視頻流，通過cv2提供的方法顯示200幀圖像::

        tl_camera.start_video_stream(display=False)
        for i in range(0, 200):
            img = tl_camera.read_cv2_image()
            cv2.imshow("Drone", img)
            cv2.waitKey(1)
        cv2.destroyAllWindows()
        tl_camera.stop_video_stream()

  第一種方法直接通過 `camera` 對象的 `start_video_tream()` 方法將機器人些採集到的視頻流通過SDK獲取並播放；
  第二種方法通過 `camera` 對象的 `start_video_stream` 方法獲取到視頻流，之後通過 `cv2.inshow()` 播放獲取到的視頻流

- 利用 `釋放機器人資源`_ 章節的介紹釋放相關資源

示例程序中同時提供了一個完整的獲取視頻流之後利用cv2提供的方法顯示圖像的例程 :file:`examples/04_camera/01_video_with_display.py`

.. literalinclude:: ./../../../examples/12_drone/16_video_stream.py
   :language: python
   :linenos:
   :lines: 17-

