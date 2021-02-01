.. _beginnger:

###########################################
RoboMaster SDK 新手入門 - 多機控制篇
###########################################

多機控制簡介
__________________

RobomasterSDK 支持多機控制，用戶可以調用相應的多機接口，輕鬆控制多台機器，實現複雜的多機編隊等任務

多機控制流程
__________________

多機控制主要分為以下方面：

    - *多機初始化* ，與局域網內的多台機器建立連接，並初始化相關機器人
    - *多機編號* ，通過飛機的SN號對飛機進行編號，便於後面進行多機的選中控制
    - *多機分組* & *群組控制* ，通過將多台機器進行分組，實現多機選中的效果
    - *任務控制* ，通過任務控制的方式可以同時控制不同組執行不同的動作

接下來本文檔將對這幾部分別進行介紹。

多機初始化
__________________

環境準備安裝netifaces包::

	pip install netifaces

.. tip:: 如果出現以下問題，請下載安裝visualcppbuildtools_full.exe(`下載地址：GitHub RoboMaster SDK repository <https://github.com/dji-sdk/robomaster-sdk>`_)

	.. image:: ./../images/neti_err.jpg


1. 首先將機器人設置為路由器組網模式，並將所有機器人與運行 RobomasterSDK 的設備連接至同一個局域網內。
關於本部分如何操作，RobomasterEP參考 :ref:`EpConn` ，教育飛機參考 :ref:`TelloConn`

2. 導入多機控制相關的包::

    from multi_robomaster import multi_robot

3. 生成多機對像

  - 示例一：生成EP機器人多機對像::

      multi_robot = multi_robot.MultiEP()

  - 示例二：生成教育機器人多機對像::

      multi_drones = multi_robot.MultiDrone()


4. 調用多機初始化函數，完成對多機器的掃瞄以及初始化步驟，EP多機的初始化函數不需要輸入參數，
教育飛機的多機初始化函數需要指明需要掃瞄的飛機數量

  - 示例一：初始化EP機器人多機對像::

      multi_robots.initialize()

  - 示例二：初始化教育無人機對象，飛機的數量為2::

      multi_drones.initialize(2)

.. note:: 注意EP機器人與教育機器人在多機初始化時的區別！

多機編號
_________________

通過將機器人編號，可以方便用戶進行多機控制。
目前支持的編號策略為根據輸入的SN進行機器人與編號的綁定,多機對像包含以下編號方法::

    number_id_by_sn([id1, SN1], [id2, SN2], [id2, SN3] ...)

方法的參數為一系列包含機器人編號信息的列表，每一個列表包含兩個元素:[id, SN]，
第一個元素為期望的編號數字，第二個元素為包含機器人SN信息的字符串, 列表的個數為用戶需要編號的機器台數，
且該方法的返回值為成功編號的機器數目

本文檔接下來會通過一個EP多機編號的例子帶領大家熟悉如何使用該功能，教育無人機的多機編號與EP類似：

    - 示例一：假設我們有兩台EP機器人需要編號，且經過之前的步驟創建了並初始化了多機對像 `multi_robots`，
      希望將SN號為 `3JKDH2T001ULTD` 的機器人編號為 `0` 號機器人，
      希望將SN號為 `3JKDH3B001NN0E` 的機器人編號為 `1` 號機器人，則可以使用如下代碼完成該編號操作::

        multi_robots.number_id_by_sn([0, '3JKDH2T001ULTD'], [1, '3JKDH3B001NN0E'])

多機分組 & 群組控制
_________________________

通過將機器人分為不同組，可以更加簡單的進行多機控制。在進行控制時， `組對像` 的控制接口調用形式與單機類似，在大多數控制情況下，用戶可以將一個 `組對像` 想像成一個單機對像使用

生成 `組對像`
##################

用戶可以利用包含不同機器人編號（多機編號參考上一小節）的列表，生成包含多個機器人的 `組對像` ，
在之後對該 `組對像` 的操作將作用於組內每個單體機器人上，多機對像支持一下創建 `組對像` 的接口::

    build_group(robot_id_list)

方法的輸入參數為包含需要分組的機器人的id信息的列表，方法的返回值為創建的 `組對像` ，接下來本文檔會以EP的分組操作舉例，
教育機器人的分組方法與其類似：

    - 示例一：假設我們有三台EP機器人，且前面幾步驟的操作都已經完成，三台機器人的編號分別為 `0` `1` `2` 號，接下來想將
      `0` 號機器人與 `1` 號機器人放到一組中，將 `2` 號機器人放到一組中，三台機器人同時又屬於另一組，則::

        robot_group1 = multi_robots.build_group([0, 1])
        robot_group2 = multi_robots.build_group([2])
        robot_group_all = multi_robots.build_group([0, 1, 2])

      通過以上代碼，創建的 `robot_group1` 對象是包含 `0` 號與 `1` 號機器人的 `組對像` ，
      創建的 `robot_group2` 對象是包含 `2` 號機器人的 `組對像` ，
      創建的 `robot_group_all` 對象是包含全部三台機器人的 `組對像` ，我們可以通過這些 `組對像` 控制組內機器人執行同樣的命令


`組對像` 的相關操作
#####################



更新成員
+++++++++++++++++

`組對像` 提供支持增添/刪除指定成員的功能，對應的對象方法分別是::

    append(self, robots_id_list)
    remove(self, robots_id_list)

方法的輸入參數為包含需要添加/刪除的機器人的編號的列表，返回值為操作結果，接下來以EP舉例，教育飛機類似：

    - 示例一：通過前面的步驟，我們得到了 `組對像` `robot_group_all` ，現在需要將其中的 `1` 號機器人
      與 `2` 號機器人從群組中移除::

        robot_group_all.remove([1, 2])

    - 示例二： 經過思考後，我們認為刪除的 `1` 號機器人與 `2` 號機器人還是需要被添加回來::

        robot_group_all.append([1, 2])

群組控制
+++++++++++++++++

在大多數情況下，群組控制的 `動作類接口` 形式與單機控制的接口形式一致，因此用戶基本上可以將前面生成的 `組對像` 當成單機對像使用,
一下分別舉例EP與教育機器人的兩個控制示例：

    - 示例一：假設前面的操作都已經完成，生成的EP `組對像` 為 `robot_group` ，本示例利用該 `組對像` 控制所有EP機器人進行
      底盤與機器人的移動::

        # 組內所有機器人前進1米，程序阻塞至所有機器人動作完成
        robot_group.chassis.move(1, 0, 0, 2, 180).wait_for_completed()

        # 組內所有機器人云台向向左旋轉90度，程序阻塞至所有機器人動作完成
        robot_group.gimbal.move(0, 90).wait_for_completed()

目前群組控制支持的api接口列表參考 `多機API列表` ，
列表中的接口參數類別以及取值範圍與單機部分相同，使用形式也相同

單機控制
++++++++++++++++

在某些多機控制的場景下，用戶可能需要單獨控制群組中的某一台機器，RobomasterSDK也支持從群組中獲取單機對象，從而進行單機控制。

用戶可以通過 `組對像` 的 `get_robot(robot_id)` 方法獲取到單機對象，從而進行單機控制，該方法的輸入參數為相應機器的編號數字，
返回值為該單機對象。另外用戶可以通過"組對像"的 `robot_id_list` 屬性獲取組內所有機器人的編號列表，
下面本文檔將會以教育飛機舉例說明，EP機器人使用方法類似：

    - 示例一：假設前面的準備工作都已經完成，`drone_group` 為獲取到的「組對像」，可以通過以下代碼實現組內的教育飛機依次起飛::

        for drone_id in drone_group.robots_id_list:
            drone_obj = drone_group.get_robot(drone_id)
            drone_obj.flight.takeoff().wait_for_completed()

任務控制
__________________

上一節有介紹如何通過 `組對像` 進行簡單的群組控制，但是如何同時讓不同組同時做不同的動作？如何在實現不同組同時執行任務的時候保證同步？
本節課來介紹多機對象的 `任務控制` 方法的使用，接口如下::

    run([robot_group1, action_task1], [robot_group2, action_task2], [robot_group3, action_task3]...)

通過該接口，用戶可以實現不同的組同時執行不同的動作，並且 `run` 方法會保證該語句執行結束時，方法輸入的所有動作任務都執行完畢。
`run` 接口的輸入參數為儲存任務信息的列表，列表包含兩個元素，第一個元素是期望執行任務的 `組對像` ，第二個元素為用戶自己編寫的的任務函數。
*用戶定義的任務函數必須滿足固定的接口形式* ，函數應只有一個參數，參數為執行函數內動作的 `組對像` ，下面本文將會以EP機器人舉例任務控制接口
的使用，教育飛機的使用方法類似：

    - 示例一：根據前面的教程現在已經獲得了三個機器人 `組對像` ，分別為包含 `0` 號機器人與 `1` 號機器人的 `robot_group1`, 包含 `2` 號
      機器人的 `robot_group2` ，以及包含 `1` `2` `3` 號三台機器人的 `robot_group_all` ，我們現在想控制 `robot_group1` 中
      的兩台機器人底盤向前移動1m，控制 `robot_group2` 中的 一台機器人向後移動1m， 在這兩個任務動作執行完畢後，控制三台機器人全部向左
      移動1m，可以利用如下方法實現

        - 首先定義上述三套動作的任務函數::

            def move_forward_task(robot_group):
                robot_group.chassis.move(x=1, y=0, z=0, xy_speed=0.7).wait_for_completed()


            def move_backward_task(robot_group):
                robot_group.chassis.move(x=-1, y=0, z=0, xy_speed=0.7).wait_for_completed()


            def move_left_task(robot_group):
                robot_group.chassis.move(x=0, y=-1, z=0, xy_speed=0.7).wait_for_completed()

        - 之後在利用多機對像 `multi_robots` 的 `run()` 方法指定 `組對像` 執行上述任務::

            # `0` 號與 `1` 號機器的底盤前進1m, `2` 號機器後退1m
            multi_robots.run([robot_group1, move_forward_task], [robot_group2, move_backward_task])

            # 三台機器的底盤同時左移1m
            multi_robots.run([robot_group_all, move_left_task])

.. note:: 用戶自定義的動作任務函數需要滿足固定的接口形式！