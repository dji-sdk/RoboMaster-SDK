.. _beginngerDrone:

###############################
RoboMaster SDK 多機編隊TT
###############################

初始化無人機
__________________

在進行與無人機相關的操作之前，需要根據指定的配置初始化無人機對像

- 首先從安裝的 `multi_robomaster` 包中導入 `multi_robot` 模塊::

    from multi_robomaster import multi_robot

- 創建 `MultiDrone` 類的實例對像 `multi_drone`， `multi_drone` 即一個多機控制器的對象::

    multi_drone = multi_robot.MultiDrone()

- 初始化無人機，目前教育系列無人機的初始化需要傳入想要控制的飛機數量::

    multi_drone.initialize(drone_num)

至此，無人機的初始化工作就完成了。

對無人機進行編號編組
_____________________

在進行多機控制時我們希望能夠簡化對飛機控制的流程，需要對飛機進行組隊操作，由於SN碼是唯一識別一架飛機的信息，
所以在多機編隊時需要根據sn碼來對飛機進行編隊，為了簡化編隊時的複雜度，SDK要求用戶使用自定義的id來對飛機SN碼
進行映射

- 在初始化後，使用已經實例化後的 `multi_drone` 對SN進行編號::

    multi_drone.number_id_by_sn([1, "0TQZH79ED00H56"], [2, "0TQZH79ED00H89"])

用戶對飛機同一SN進行多個id的映射是被允許的，但是一個id只允許映射一個SN

- 使用已經實例化後的 `multi_drone` 對飛機進行編組::

    multi_drone_group1 = multi_drone.build_group([1, 2])

編組後的結果為 `multi_group` 對像為 `multi_drone_group1` ，用戶可以對同一架飛機進行多次編組，如::

    multi_drone_group1 = multi_drone.build_group([1])
    multi_drone_group2 = multi_drone.build_group([1, 2])

- 若用戶不期望對飛機進行編號，則可使用 `number_id_to_all_drone` API隱式的對飛機進行0~drone_num的隨機編號::

    multi_drone.number_id_to_all_drone()

至此，無人機的編組工作就完成了，接下來可以通過相關接口對無人機進行信息查詢、動作控制等操作

控制無人機執行命令
___________________

- 在完成動作編組後，使用已經實例化後的 `multi_drone` 執行動作::

    multi_drone.run([multi_drone_group1, base_action_1])

其中 `multi_drone_group1` 為編組後的 `multi_group` 對象， `base_action_1` 為用戶自定義的命令函數，格式為::

    def base_action_1(robot_group):
        robot_group.get_sn()
        robot_group.get_battery()

若想多group同時執行多組動作，可通過如下方式進行，以兩個group為例::

    multi_drone.run([multi_drone_group1, base_action_1],
                    [multi_drone_group2, base_action_2])

至此，無人機的執行命令就完成了

釋放無人機資源
__________________

在程序的最後，應該手動釋放無人機對像相關的資源，包括釋放網絡地址、結束相應後台線程、釋放相應地址空間等，
在 `multi_drone.close` 對像中，提供了用來釋放相關資源的方法 `close()`，使用方法如下::

    multi_drone.close()

.. tip:: 為了避免一些意外錯誤，記得在程序的最後調用 `close()` 方法哦！

查詢類接口的使用
____________________

查詢類接口即數據獲取類接口，用戶可以通過該類接口獲取無人機自身的狀態信息以及傳感器狀態等信息，
接下來將從查詢無人機SN信息與查詢無人機電量兩個例子來幫助用戶掌握該類型接口的用法

示例一：查詢機器人SN信息和電量
********************************

- 首先按照 `控制無人機執行命令`_ 章節的介紹完成無人機對象的各項操作

- 對 `base_action_1` (此例中為 `base_task` )進行編寫如下:

.. literalinclude:: ./../../../examples/15_multi_robot/multi_drone/02_basic.py
   :language: python
   :linenos:
   :lines: 19-21

飛機的SN號和電量會在控制台打印出來，打印格式為： "DRONE id: {}, reply: {}"

- 利用 `釋放無人機資源`_ 章節的介紹釋放相關資源

完整的程序參考示例文件 :file:`/examples/15_multi_robot/multi_drone/02_basic.py`

.. literalinclude:: ./../../../examples/15_multi_robot/multi_drone/02_basic.py
   :language: python
   :linenos:
   :lines: 16-

設置類接口的使用
_______________________

設置類接口可以完成對無人機的相關模塊的設置，本文檔接下來將通過設置擴展led模塊講解設置類接口的使用

.. tip:: 設置擴展led燈目前只有 Tello Talent 機器支持！

示例一：設置無人機擴展led模塊
********************************

下面介紹如何通過 SDK 實現設置無人機擴展led模塊的操作

- 首先按照 `控制無人機執行命令`_ 章節的介紹完成無人機對象的各項操作

- 對 `base_action_1` 進行編寫如下:

.. literalinclude:: ./../../../examples/15_multi_robot/multi_drone/06_led.py
   :language: python
   :linenos:
   :lines: 19-22

使用 `set_led(255, 255, 255)` 接口可以令當前group中所有飛機亮白燈，若想實現不同飛機分別亮不同顏色的燈，
可以使用 `command_dict` 關鍵字，當使用了 `command_dict` 且其參數類型為dict時，將實現當前group下
不同飛機分別亮燈，如上例所示，1號飛機亮紅燈，2號飛機亮綠燈。

值得注意的是，當使用了 `command_dict` 關鍵字且其參數類型為dict時以後，其他參數將被自動忽略，字典中的飛機數
必須等於當前group中的飛機數，不支持默認設置。

- 利用 `釋放無人機資源`_ 章節的介紹釋放相關資源

完整的程序參考示例文件 :file:`/examples/15_multi_robot/multi_drone/06_led.py`

.. literalinclude:: ./../../../examples/15_multi_robot/multi_drone/06_led.py
   :language: python
   :linenos:
   :lines: 15-

動作類接口的使用
_____________________________

動作類接口是用來控制無人機執行飛行動作的接口，本文檔接下來將講解飛行類接口的使用

.. warning:: 飛機固件版本v2.5.1.4 和 wifi模塊版本v1.0.0.33 以下的用戶，請升級後再使用動作類接口，否則會導致執行飛行動作異常，查詢方式請參考單機接口文檔

示例一：控制飛機起飛並前後飛行
********************************

在本例程中，首先需要控制兩組共兩架飛機起飛，之後控制飛機起飛並向前向後各飛行100cm

- 首先按照 `控制無人機執行命令`_ 章節的介紹完成無人機對象的各項操作,隨後編寫如下程序:

.. literalinclude:: ./../../../examples/15_multi_robot/multi_drone/03_takeoff_land.py
   :language: python
   :linenos:
   :lines: 16-

- 利用 `釋放無人機資源`_ 章節的介紹釋放相關資源

.. warning:: 不同於單機，多機執行飛行動作時，wait_for_completed()接口為必寫項，如忘記書寫則可能導致當前動作的下一動作無法運行，在等待一段時間後會執行當前動作之後的第二個動作

示例二：控制飛機移動到目標坐標點
********************************

在本例程中，首先需要控制兩架飛機起飛，之後控制飛機起飛並以大地毯中點為圓心，
以50cm為邊長，在100cm高度上以100cm/s的速度按正方形軌跡運動

- 首先按照 `控制無人機執行命令`_ 章節的介紹完成無人機對象的各項操作

- 對 `base_action_1` 進行編寫如下:

.. literalinclude:: ./../../../examples/15_multi_robot/multi_drone/05_go.py
   :language: python
   :linenos:
   :lines: 19-29

值得注意的是，多機編隊的go指令強制用戶使用地毯坐標進行運動，為了編程安全不支持飛機自身坐標系移動，
字典中的飛機數必須等於當前group中的飛機數，不支持默認設置。

- 利用 `釋放無人機資源`_ 章節的介紹釋放相關資源

完整的程序參考示例文件 :file:`/examples/15_multi_robot/multi_drone/05_go.py`

.. literalinclude:: ./../../../examples/15_multi_robot/multi_drone/05_go.py
   :language: python
   :linenos:
   :lines: 16-