.. _beginngerEp:

####################################
RoboMaster SDK 新手入門 - EP 篇
####################################

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

- 創建 `Robot` 類的實例對像 `ep_robot`， `ep_robot` 即一個機器人的對象::

    ep_robot = robot.Robot()

- 初始化機器人，如果調用初始化方法時不傳入任何參數，則使用config.py中配置的默認連接方式（WIFI直連模式）
  以及默認的通訊方式（udp通訊）對機器人進行初始化，在本示例中我們手動指定機器人的連接方式為組網模式,
  不指定通訊方式使用默認配置::

    ep_robot.initialize(conn_type="sta")

..

  可以通過以下語句設置默認的連接方式與通訊方式，本例中將默認的連接方式設置為 `sta` 模式，
  默認的通訊方式設置為 `tcp` 方式::


    config.DEFAULT_CONN_TYPE = "sta"
    config.DEFAULT_PROTO_TYPE = "tcp"


至此，機器人的初始化工作就完成了，接下來可以通過相關接口對機器人進行信息查詢、動作控制、多媒體使用等操作，
本文檔將在後面的部分對幾類接口的使用分別進行介紹

獲取模塊對像
__________________

部分 SDK 接口屬於 `Robot` 對像本身，因此可以通過 `Robot` 對像直接調用，
但是一些接口屬於 `Robot` 對像包含的其他模塊，比如裝甲燈的設置接口在 `led` 模塊對像中，
底盤的控制接口在 `chassis` 模塊對像中，等等。如果想使用這些接口需要首先獲得相應的對象，
這裡以獲取 `led` 模塊對像舉例，介紹如何獲取這些對像

- 首先按照 `初始化機器人`_ 章節的介紹完成機器人對象的初始化操作

- 可以使用兩種方法獲取 `led` 對像

  - 方法一：直接使用 `.` 運算符從 `Robot()` 對像中獲取 `led` 對像::

        ep_led = ep_robot.led


  - 方法二：利用 `Robot` 對象的 `get_module()` 方法獲得指定的對象::

        ep_led = ep_robot.get_module("led")

獲取了相關對象，便可以通過該對像調用其所包含的 SDK 接口


釋放機器人資源
__________________

在程序的最後，應該手動釋放機器人對像相關的資源，包括釋放網絡地址、結束相應後台線程、釋放相應地址空間等，
在 `Robot` 對像中，提供了用來釋放相關資源的方法 `close()`，使用方法如下::

    ep_robot.close()

.. tip:: 為了避免一些意外錯誤，記得在程序的最後調用 `close()` 方法哦！

查詢類接口的使用
________________

查詢類接口即數據獲取類接口，用戶可以通過該類接口獲取機器人自身的狀態信息以及傳感器狀態等信息，
接下來將從查詢機器人版本信息與查詢機器人SN號兩個例子來幫助用戶掌握該類型接口的用法

示例一：查詢機器人版本
************************

- 首先按照 `初始化機器人`_ 章節的介紹完成機器人對象的初始化操作

- 使用`Robot` 對象的 `get_version()` 方法，方法的返回值即為代表機器人版本號的字符串，
  並且將獲取到的版本號打印出來::

    ep_version = ep_robot.get_version()
    print("Robot Version: {0}".format(ep_version))

- 利用 `釋放機器人資源`_ 章節的介紹釋放相關資源

完整的程序參考示例文件 :file:`/examples/01_robot/01_get_version.py`

.. literalinclude:: ./../../../examples/01_robot/01_get_version.py
   :language: python
   :linenos:
   :lines: 17-

示例二：獲取機器人SN號
************************

- 首先按照 `初始化機器人`_ 章節的介紹完成機器人對象的初始化操作

- 利用 `Robot` 對像使用 `get_sn()` 方法，方法的返回值即為代表機器人SN號的字符串，
  並且將獲取到的SN號打印出來::

    SN = ep_robot.get_sn()
    print("Robot SN:", SN)

- 利用 `釋放機器人資源`_ 章節的介紹釋放相關資源

完整的程序參考示例文件 :file:`/examples/01_robot/02_get_sn.py`

.. literalinclude:: ./../../../examples/01_robot/02_get_sn.py
   :language: python
   :linenos:
   :lines: 17-

設置類接口的使用
_______________________

設置類接口可以完成對機器人的相關模塊的設置，本文檔接下來將通過設置機器人整機運動模式與設置機器人裝甲燈兩個例子講解設置類接口的使用

示例一：設置機器人整機運動模式
********************************

機器人的運動模式有三種：自由模式（FREE）、雲台跟隨底盤（CHASSIS_LEAD）、底盤跟隨雲台（GIMBAL_LEAD），
本文檔以設置機器人的運動模式為底盤跟隨雲台（CHASSIS_LEAD）為例帶大家熟悉如何使用設置類接口

- 首先按照 `初始化機器人`_ 章節的介紹完成機器人對象的初始化操作

- 使用`Robot` 對像中的 `set_robot_mode()` 方法設置機器人的整機運動模式，
  機器人的模式定義在 :file:`/examples/01_robot/02_get_sn.py` 中，
  `FREE` ， `GIMBAL_LEAD` , `CHASSIS_LEAD` 是可選的三個參數，
  本示例中設置機器人的整機運動模式為底盤跟隨雲台模式（`GIMBAL_LEAD`）::

    ep_robot.set_robot_mode(mode=robot.GIMBAL_LEAD)

- 利用 `釋放機器人資源`_ 章節的介紹釋放相關資源

完整的程序參考示例文件 :file:`/examples/01_robot/09_set_mode.py`

.. literalinclude:: ./../../../examples/01_robot/09_set_mode.py
   :language: python
   :linenos:
   :lines: 17-

示例二：設置機器人裝甲燈
********************************

下面介紹如何通過 SDK 實現設置機器人裝甲燈的操作

- 首先按照 `初始化機器人`_ 章節的介紹完成機器人對象的初始化操作,
  另外由於設置燈效時要使用 `led` 模塊中關於裝甲燈的一些定義，因此需要額外導入 `led` 模塊::

    from robomaster import led

- 機器人的裝甲燈設置接口屬於 `Robot`對像包含的 `led` 模塊，因此首先需要獲取 `led` 對象，
  按照 `獲取模塊對像`_ 章節的介紹獲取 `led` 對像, 本示例中使用方法一獲取模塊對像::

    ep_led = ep_robot.led

- 使用 `led` 對像中的 `set_led()` 方法設置機器人的裝甲燈效果，
  在使用 `led` 方法時，通過 `comp` 參數選定要控制的裝甲燈， 通過 `r` `g` `b` 參數指定燈的顏色，
  通過 `effect` 參數指定led燈的顯示效果。
  在本例中，控制的裝甲燈對像通過 `comp` 選定為所有裝甲燈， `r` `g` `b` 顏色指定為紅色，
  `effect` 選定的燈效為常亮燈效::

    ep_led.set_led(comp=led.COMP_ALL, r=255, g=0, b=0, effect=led.EFFECT_ON)

- 利用 `釋放機器人資源`_ 章節的介紹釋放相關資源

示例程序中提供了一個完整的設置裝甲燈的例程 :file:`/examples/01_robot/09_set_mode.py`，
例程中利用了for循環，實現了led燈的8次顏色變換，每次維持1秒鐘

.. literalinclude:: ./../../../examples/07_led/01_set_led.py
   :language: python
   :linenos:
   :lines: 17-


動作類接口的使用
_____________________________

動作類接口是用來控制機器人執行某些指定動作的接口，根據動作本身特性的不同，
SDK中包含 *即時動作控制* 與 *任務動作控制* 兩類動作接口

即時動作控制
*************

即時控制類動作是指設置後馬上生效的動作，特指宏觀上是「瞬時」執行的動作，
接下來本文檔將通過控制發射器射擊與控制底盤速度兩個例子帶大家熟悉此類動作接口

示例一：控制發射器射擊
++++++++++++++++++++++++++++

- 首先按照 `初始化機器人`_ 章節的介紹完成機器人對象的初始化操作,
  另外由於使用發射器接口時要使用 `blaster` 模塊中關於發射器的一些定義，因此需要額外導入 `blaster` 模塊::

    from robomaster import blaster

- 發射器的控制接口屬於 `blaster` 模塊，首先按照 `獲取模塊對像`_ 章節的介紹獲取 `blaster` 對像,
  本示例中使用方法一獲取模塊對像::

    ep_blaster = ep_robot.blaster

- 使用 `blaster` 對像中的 `fire()` 方法控制發射器射擊， 方法的參數 `fire_type` 可以指定發射的類型，
  可選水彈、紅外彈，在本示例中我們使用水彈， 參數 `times` 設置發射的次數，本示例中指定發射的次數為1::

    ep_balseter.fire(fire_type=balseter.WATER_FIRE, times=1)

- 利用 `釋放機器人資源`_ 章節的介紹釋放相關資源

示例程序中提供了一個完整的控制發射器射擊的例程 :file:`examples/06_blaster/01_fire.py`

.. literalinclude:: ./../../../examples/06_blaster/01_fire.py
   :language: python
   :linenos:
   :lines: 17-

示例二：控制底盤速度
++++++++++++++++++++++++++++

控制底盤速度是一種典型的即時控制，發出控制指令後機器人將會立即按照指定速度運動

- 首先按照 `初始化機器人`_ 章節的介紹完成機器人對象的初始化操作

- 底盤控制接口屬於 `chassis` 模塊，首先按照 `獲取模塊對像`_ 章節的介紹獲取 `chassis` 對像,
  本示例中使用方法一獲取模塊對像::

    ep_chassis= ep_robot.chassis

- 使用 `chassis` 對像中的 `dirve_speed()` 方法控制底盤的速度，
  方法的參數 `x` `y` `z` 分別代表前進、橫移、旋轉速度， 本示例中指定 `x` 前進速度點為 0.5 m/s,
  `timeout` 參數可以指定一個時間，超過該時間未接收到控制速度指令，SDK 將會主動控制機器人停止，
  本示例中指定 `timeout` 為 5s, 在機器人按照指定速度運行3s後，將速度設置為 0 ::

    ep_chassis.drive_speed(x=0.5, y=0, z=0, timeout=5)
    time.sleep(3)
    ep_chassis.drive_speed(x=0, y=0, z=0, timeout=5)

- 利用 `釋放機器人資源`_ 章節的介紹釋放相關資源

示例程序中提供了一個完整的控制底盤速度的例程 :file:`examples/02_chassis/03_speed.py`，
例程中每次令機器人按照指定速度運動三秒鐘，然後改變速度

.. literalinclude:: ./../../../examples/02_chassis/03_speed.py
   :language: python
   :linenos:
   :lines: 17-

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


示例一：控制底盤移動指定距離
+++++++++++++++++++++++++++++++

控制底盤移動指定距離是一種任務動作控制

- 首先按照 `初始化機器人`_ 章節的介紹完成機器人對象的初始化操作

- 底盤控制接口屬於 `chassis` 模塊，首先按照 `獲取模塊對像`_ 章節的介紹獲取 `chassis` 對像,
  由於本示例中同時也會控制裝甲燈，因此也需要獲取 `led` 模塊，
  本示例中使用方法一獲取模塊對像::

    ep_chassis = ep_robot.chassis
    ep_led = ep_robot.led

- 在本示例中為了說明任務類動作的特點，在控制底盤運動後會設置裝甲燈燈效。
  使用 `chassis` 對像中的 `move()` 方法控制底盤的相對位置移動，
  方法的參數 `x` `y` 代表 `x` 軸 `y` 軸的運動距離， 參數 `z` 代表 `z` 軸的旋轉速度，
  本示例中指定 `x` 軸的運動距離為 0.5 m, `y` `z` 兩參數為 0，
  `xy_speed` 參數可以指定 `xy` 兩軸的運動速度， `z_speed` 參數用來指定 `z` 軸的旋轉速度，
  本示例中指定 `xy` 軸的運動速度為 0.7 m/s, `z` 軸的旋轉速度設置為 0。
  設置裝甲燈燈效可以參考 `示例二：設置機器人裝甲燈`_ 。接下來本文檔會使用三種方法控制底盤移動的任務動作：

  - 方法一：執行任務動作後，立即調用 `wait_for_completed()` 方法::

     ep_chassis.move(x=x_val, y=0, z=0, xy_speed=0.7).wait_for_completed()
     ep_led.set_led(comp=led.COMP_ALL, r=255, g=0, b=0, effect=led.EFFECT_ON)

  - 方法二：在執行其他命令後再調用 `wait_for_completed()` 方法::

     chassis_action = ep_chassis.move(x=x_val, y=0, z=0, xy_speed=0.7)
     ep_led.set_led(comp=led.COMP_ALL, r=255, g=0, b=0, effect=led.EFFECT_ON)
     chassis_action.wait_for_completed()

  - 方法三：不使用 `wait_for_completed()` 方法，利用延時來保證動作執行結束::

     ep_chassis.move(x=x_val, y=0, z=0, xy_speed=0.7)
     ep_led.set_led(comp=led.COMP_ALL, r=255, g=0, b=0, effect=led.EFFECT_ON)
     time.sleep(10)

  三種任務動作接口的調用形式對應機器人的行為不同，*方法一* 機器人會先移動到指定位置之後裝甲燈再全亮紅色，
  而 *方法二* 與 *方法三* 則會在移動的過程中裝甲燈全亮紅色。

.. tip:: 建議使用 *方法一* 以及 *方法二* ，在合適的時機調用 `wait_for_completed()` 是比較安全的做法

- 利用 `釋放機器人資源`_ 章節的介紹釋放相關資源

示例程序中提供了一個完整的控制底盤移動指定距離的例程 :file:`examples/02_chassis/01_move.py`，

.. literalinclude:: ./../../../examples/02_chassis/01_move.py
   :language: python
   :linenos:
   :lines: 17-


多媒體接口的使用
______________________________________

多媒體接口主要包括視頻流與音頻流兩部分，接下來將通過兩個示例介紹該類型接口的使用

示例一：獲取視頻流
**********************

獲取機器人採集到的視頻流有助於實現一些非常實用的案例，下面本文檔將介紹如何通過 SDK 獲取視頻流

- 首先按照 `初始化機器人`_ 章節的介紹完成機器人對象的初始化操作，
  由於示例中會用到 `camera` 模塊的相關定義，因此還需要導入 `camera` 模塊::

    from robomaster import camera

- 獲取視頻流相關的接口屬於屬於 `camera` 模塊，首先按照 `獲取模塊對像`_ 章節的介紹獲取 `camera` 對像,
  本示例中使用`獲取模塊對像`_ 章節介紹的方法一獲取模塊對像::

    ep_camera= ep_robot.camera

- `camera` 模塊的 `start_video_stream` 方法有兩個參數， `display` 參數指定是否顯示獲取到的視頻流，
  `resolution` 參數指定視頻的尺寸大小。在本示例中，向大家介紹兩種獲取視頻流的方法，

  - 方法一：獲取視頻流並直接播放顯示十秒::

        ep_camera.start_video_stream(display=True, resolution=camera.STREAM_360P)
        time.sleep(10)
        ep_camera.stop_video_stream()

  - 方法二：獲取視頻流，通過cv2提供的方法顯示200幀圖像::

        ep_camera.start_video_stream(display=False)
        for i in range(0, 200):
            img = ep_camera.read_cv2_image()
            cv2.imshow("Robot", img)
            cv2.waitKey(1)
        cv2.destroyAllWindows()
        ep_camera.stop_video_stream()

  第一種方法直接通過 `camera` 對象的 `start_video_tream()` 方法將機器人些採集到的視頻流通過SDK獲取並播放；
  第二種方法通過 `camera` 對象的 `start_video_stream` 方法獲取到視頻流，之後通過 `cv2.inshow()` 播放獲取到的視頻流

- 利用 `釋放機器人資源`_ 章節的介紹釋放相關資源

示例程序中提供了一個完整的獲取並直接顯示視頻流的例程 :file:`examples/04_camera/01_video_with_display.py`

.. literalinclude:: ./../../../examples/04_camera/01_video_with_display.py
   :language: python
   :linenos:
   :lines: 17-

示例程序中同時提供了一個完整的獲取視頻流之後利用cv2提供的方法顯示圖像的例程 :file:`examples/04_camera/03_video_without_display.py`

.. literalinclude:: ./../../../examples/04_camera/03_video_without_display.py
   :language: python
   :linenos:
   :lines: 17-

示例二：獲取音頻流
**********************

本示例將會通過 SDK 獲取機器人採集到的音頻流， 並將獲取到的音頻信息以 `wav` 文件的形式保存在本地

- 首先按照 `初始化機器人`_ 章節的介紹完成機器人對象的初始化操作

- 獲取視頻流相關的接口屬於屬於 `camera` 模塊，首先按照 `獲取模塊對像`_ 章節的介紹獲取 `camera` 對像,
  本示例中使用`獲取模塊對像`_ 章節介紹的方法一獲取模塊對像::

    ep_camera= ep_robot.camera

- 通過調用 `camera` 模塊的 `record_audio()` 方法，將獲取到的音頻流保存在本地，
  方法的 `save_file` 參數可以指定保存文件的名稱， `seconds` 參數可以指定採集的音頻時長，
  `sample_rate` 參數指定採集頻率::

    ep_camera.record_audio(save_file="output.wav", seconds=5, sample_rate=16000)

- 利用 `釋放機器人資源`_ 章節的介紹釋放相關資源

示例程序中提供了一個完整的獲取音頻流並保存在本地的例程 :file:`examples/04_camera/05_record_audio.py`

.. literalinclude:: ./../../../examples/04_camera/05_record_audio.py
   :language: python
   :linenos:
   :lines: 17-