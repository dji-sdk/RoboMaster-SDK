.. _beginngerDrone:

###########################################
RoboMaster SDK 新手入门 - 教育系列无人机篇
###########################################

初始化机器人
__________________

在进行与机器人相关的操作之前，需要根据指定的配置初始化机器人对象

- 首先从安装的 `robomaster` 包中导入 `robot` 模块::

    from robomaster import robot

- 指定 RoboMaster SDK 的本地ip地址（如需手动指定），在本示例中，查询得到本地的ip地址为 `192.168.2.20`
  （比如在Windows操作系统下，通过 快捷键 `Win` + `R` 调出的窗口中输入 `cmd`，
  然后在 CMD窗口中输入 `ipconfig` ， 即可以查看设备ip的信息），
  如需指定ip使用以下语句::

    robomaster.config.LOCAL_IP_STR = "192.168.2.20"

.. tip:: 大部分情况下SDK能够自动获取正确的本地ip，无需手动指定这一步骤，但是当SDK运行在多网卡同时使用的设备时，
  自动获取的ip可能不是与机器人进行连接的ip，此时需要手动指定ip

- 创建 `Drone` 类的实例对象 `tl_drone`， `tl_drone` 即一个机器人的对象::

    tl_drone = robot.Drone()

- 初始化机器人，目前教育系列无人机的初始化不需要传入任何参数::

    tl_drone.initialize()

至此，机器人的初始化工作就完成了，接下来可以通过相关接口对机器人进行信息查询、动作控制、多媒体使用等操作，
本文档将在后面的部分对几类接口的使用分别进行介绍

获取模块对象
__________________

部分 SDK 接口属于 `Drone` 对象本身，因此可以通过 `Drone` 对象直接调用，
但是一些接口属于 `Drone` 对象包含的其他模块，比如飞机电池的信息获取接口在 `led` 模块对象中，
飞行器的控制接口在 `flight` 模块对象中，等等。如果想使用这些接口需要首先获得相应的对象，
这里以获取 `flight` 模块对象举例，介绍如何获取这些对象

- 首先按照 `初始化机器人`_ 章节的介绍完成机器人对象的初始化操作

- 可以使用两种方法获取 `flight` 对象

  - 方法一：直接使用 `.` 运算符从 `Drone()` 对象中获取 `flight` 对象::

        tl_flight = tl_drone.flight

  - 方法二：利用 `Drone` 对象的 `get_module()` 方法获得指定的对象::

        tl_flight = tl_drone.get_module("flight")

获取了相关对象，便可以通过该对象调用其所包含的 SDK 接口


释放机器人资源
__________________

在程序的最后，应该手动释放机器人对象相关的资源，包括释放网络地址、结束相应后台线程、释放相应地址空间等，
在 `Drone` 对象中，提供了用来释放相关资源的方法 `close()`，使用方法如下::

    tl_drone.close()

.. tip:: 为了避免一些意外错误，记得在程序的最后调用 `close()` 方法哦！

查询类接口的使用
____________________

查询类接口即数据获取类接口，用户可以通过该类接口获取机器人自身的状态信息以及传感器状态等信息，
接下来将从查询机器人SDK固件版本信息与查询机器人SN号两个例子来帮助用户掌握该类型接口的用法

示例一：查询机器人固件SDK版本
********************************

- 首先按照 `初始化机器人`_ 章节的介绍完成机器人对象的初始化操作

- 使用 `Drone` 对象的 `get_sdk_version()` 方法，方法的返回值即为代表机器人SDK固件版本号的字符串，
  并且将获取到的版本号打印出来::

    drone_version = tl_drone.get_sdk_version()
    print("Drone sdk version: {0}".format(drone_version))

- 利用 `释放机器人资源`_ 章节的介绍释放相关资源

完整的程序参考示例文件 :file:`/examples/12_drone/02_get_version.py`

.. literalinclude:: ./../../../examples/12_drone/02_get_version.py
   :language: python
   :linenos:
   :lines: 17-

示例二：获取机器人SN号
************************

- 首先按照 `初始化机器人`_ 章节的介绍完成机器人对象的初始化操作

- 利用 `Drone` 对象使用 `get_sn()` 方法，方法的返回值即为代表机器人SN号的字符串，
  并且将获取到的SN号打印出来::

    SN = tl_drone.get_sn()
    print("drone sn: {0}".format(SN))

- 利用 `释放机器人资源`_ 章节的介绍释放相关资源

完整的程序参考示例文件 :file:`/examples/12_drone/03_get_sn.py`

.. literalinclude:: ./../../../examples/12_drone/03_get_sn.py
   :language: python
   :linenos:
   :lines: 17-

设置类接口的使用
_______________________

设置类接口可以完成对机器人的相关模块的设置，本文档接下来将通过设置扩展led模块讲解设置类接口的使用

.. tip:: 设置扩展led灯目前只有 Tello Talent 机器支持！

示例一：设置机器人扩展led模块
********************************

下面介绍如何通过 SDK 实现设置机器人机器人扩展led模块的操作

- 首先按照 `初始化机器人`_ 章节的介绍完成机器人对象的初始化操作,

- 机器人的装甲灯设置接口属于 `Drone`对象包含的 `led` 模块，因此首先需要获取 `led` 对象，
  按照 `获取模块对象`_ 章节的介绍获取 `led` 对象, 本示例中使用方法一获取模块对象::

    tl_led = tl_robot.led

- 使用 `led` 对象中的 `set_led()` 方法设置机器人的扩展led灯效，
  在使用 `led` 方法时，通过 `r` `g` `b` 参数可以指定led的颜色，这了将其指定为红色::

    tl_led.set_led(r=255, g=0, b=0)

- 利用 `释放机器人资源`_ 章节的介绍释放相关资源

示例程序中提供了一个完整的设置装甲灯的例程 :file:`/examples/12_drone/20_led.py`，
例程中利用了for循环，实现了led灯的8次颜色变换，每次维持0.5秒钟

.. literalinclude:: ./../../../examples/12_drone/20_led.py
   :language: python
   :linenos:
   :lines: 17-


动作类接口的使用
_____________________________

动作类接口是用来控制机器人执行某些指定动作的接口，根据动作本身特性的不同，
SDK中包含 *即时动作控制* 与 *任务动作控制* 两类动作接口。
由于飞机类机器人本身的特性决定必须要起飞后才能进行控制，
因此本文档将首先会介绍 *任务动作控制*，带领大家熟悉了飞行类动作之后会再介绍 *即时动作控制* 类的接口使用

任务动作控制
**********************

任务动作是指需要持续一段时间才能完成的动作，比如控制底盘向前运动一米，
底盘对于该动作需要执行一段时间才能到达指定地点。通过 SDK 控制任务动作时，
SDK 将对应的任务发送给机器人，机器人收到任务后会选择执行/拒绝执行（存在机器人当前时刻无法执行对应任务的情况）并通知 SDK，
如果选择执行任务，会在任务完成时再次告知 SDK。在使用任务动作控制接口时，用户需要注意以下两点：

- 任务动作接口的返回值为 `action` 对象，`action` 对象提供 `wait_for_completed(timeout)` 方法，
  用户可以通过 `timeout` 参数指定动作的超时时长。当调用 `wait_for_completed(timeout)` 方法时，
  程序会阻塞在该语句，直至动作执行完毕或执行超时


- 同一模块同一时间只能执行一个动作， 因此同一模块的任务之间互斥；不同模块之间的相互独立，动作可以同时执行。
  比如在使用任务动作控制接口后不立即调用 `wait_for_completed()` 方法时，用户在控制云台移动到指定角度的同时可以控制底盘移动到指定位置，
  但是不支持在上次控制云台的任务动作还未完成时再次发送其他的控制云台的任务动作


.. tip:: 如果在使用任务动作控制接口时不马上调用 `wait_for_completed()` 方法，切记程序中要控制好逻辑，
  避免在该任务执行完毕前发送与其互斥的其他任务动作命令！

接下来本文档会通过控制底盘移动指定距离来帮助大家熟悉该类接口的使用


示例一：控制飞机起飞并前后飞行
+++++++++++++++++++++++++++++++

在本例程中，首先需要控制飞机起飞，之后控制飞机起飞并向前飞行50cm

- 首先按照 `初始化机器人`_ 章节的介绍完成机器人对象的初始化操作

- 飞行控制接口属于 `flight` 模块，首先按照 `获取模块对象`_ 章节的介绍获取 `flight` 对象,
  由于本示例中同时也会控制扩展led模块，因此也需要获取 `led` 模块，
  本示例中使用方法一获取模块对象::

    tl_flight = tl_drone.flight
    tl_led = tl_drone.led

- 之后控制飞机起飞升空，控制起飞时通过调用任务动作接口返回的 `action` 中的 `wait_for_completed()` 方法阻塞程序直至起飞完成::

    tl_flight.takeoff().wait_for_completed()

- 接下来会控制飞机向前飞行50cm，本示例为了说明任务类动作的特点，在控制飞机飞行后会设置扩展led灯效。
  使用 `flight` 对象中的 `forward()` 方法控制底盘向前飞行，该方法都只有一个参数 `distance` ， 用来指定飞行距离。
  设置扩展led模块可以参考 `示例一：设置机器人扩展led模块`_ 。接下来本文档会使用三种方法使用任务动作接口


  - 方法一：执行任务动作后，立即调用 `wait_for_completed()` 方法::

     tl_flight.forward(distance=50).wait_for_completed()
     tl_led.set_led(r=255, g=0, b=0)

  - 方法二：在执行其他命令后再调用 `wait_for_completed()` 方法::

     flight_action = tl_flight.forward(distance=50)
     tl_led.set_led(r=255, g=0, b=0)
     flight_action.wait_for_completed()

  - 方法三：不使用 `wait_for_completed()` 方法，利用延时来保证动作执行结束::

     flight_action = tl_flight.forward(distance=50)
     tl_led.set_led(r=255, g=0, b=0)
     time.sleep(8)

  三种任务动作接口的调用形式对应机器人的行为不同，*方法一* 机器人会向前飞行到达指定地点后再将扩展led模块设置为红色，
  而 *方法二* 与 *方法三* 向前飞行的过程中将扩展led模块设置为红色。


.. note:: *方法二* 与 *方法三* 中，要注意不能在飞行过程使用其他 `ack` 为 `ok/error` 的接口！机器人的 `ack` 参考 《 Tello SDK 使用说明》


.. tip:: 建议使用 *方法一* 以及 *方法二* ，在合适的时机调用 `wait_for_completed()` 是比较安全的做法


- 飞机降落::

    tl_flight.land().wait_for_completed()

- 利用 `释放机器人资源`_ 章节的介绍释放相关资源

示例程序中提供了一个完整的控制底盘前后各飞行50cm的例程 :file:`examples/12_drone/07_forward_backward.py`，

.. literalinclude:: ./../../../examples/12_drone/07_forward_backward.py
   :language: python
   :linenos:
   :lines: 17-


即时动作控制
*************

即时控制类动作是指设置后马上生效的动作，特指宏观上是“瞬时”执行的动作，
接下来本文档将通过控制遥控器杆量带大家熟悉此类动作接口

示例一：控制遥控器杆量
++++++++++++++++++++++++++++

控制遥控器杆量是一种典型的即时控制，发出控制指令后机器人将会立即按照指定速度与方向飞行

- 首先按照 `初始化机器人`_ 章节的介绍完成机器人对象的初始化操作

- 飞行控制接口属于 `flight` 模块，首先按照 `获取模块对象`_ 章节的介绍获取 `flight` 对象,
  本示例中使用方法一获取模块对象::

    tl_flight = tl_drone.flight

- 之后控制飞机起飞升空，控制起飞时通过调用任务动作接口返回的 `action` 中的 `wait_for_completed()` 方法阻塞程序直至起飞完成::

    tl_flight.takeoff().wait_for_completed()

- 接下来会控制飞机以指定的速度向左飞行三秒钟然后停止。
  使用 `flight` 对象中的 `rc()` 方法控制底盘向前飞行，方法有控制横滚、俯仰、油门、偏航四个速度的参数，可以通过api文档中的介绍详细了解，
  本示例中令横滚的控制参数 `a` 的值为 20， 来达到飞机左飞的目的, 在三秒后将飞机的所有速度全设为0，达到停止飞行的目的::

    tl_flight.rc(a=20, b=0, c=0, d=0)
    time.sleep(4)

- 飞机降落::

    tl_flight.land().wait_for_completed()

- 利用 `释放机器人资源`_ 章节的介绍释放相关资源

示例程序中提供了一个完整的通过遥控器杆量控制飞机飞行的例程 :file:`examples/12_drone/13_rc.py`，

.. literalinclude:: ./../../../examples/12_drone/13_rc.py
   :language: python
   :linenos:
   :lines: 17-

多媒体接口的使用
______________________________________

教育系列无人机的多媒体部分主要指获取视频流

示例一：获取视频流
**********************

获取机器人采集到的视频流有助于实现一些非常实用的案例，下面本文档将介绍如何通过 SDK 获取视频流

- 首先按照 `初始化机器人`_ 章节的介绍完成机器人对象的初始化操作，
  由于示例中会用到 `camera` 模块的相关定义，因此还需要导入 `camera` 模块::

    from robomaster import camera

- 获取视频流相关的接口属于属于 `camera` 模块，首先按照 `获取模块对象`_ 章节的介绍获取 `camera` 对象,
  本示例中使用`获取模块对象`_ 章节介绍的方法一获取模块对象::

    tl_camera= tl_robot.camera

- `camera` 模块的 `start_video_stream` 方法有两个参数， `display` 参数指定是否显示获取到的视频流，在本示例中，向大家介绍两种获取视频流的方法，

  - 方法一：获取视频流并直接播放显示十秒::

        tl_camera.start_video_stream(display=True)
        time.sleep(10)
        tl_camera.stop_video_stream()

  - 方法二：获取视频流，通过cv2提供的方法显示200帧图像::

        tl_camera.start_video_stream(display=False)
        for i in range(0, 200):
            img = tl_camera.read_cv2_image()
            cv2.imshow("Drone", img)
            cv2.waitKey(1)
        cv2.destroyAllWindows()
        tl_camera.stop_video_stream()

  第一种方法直接通过 `camera` 对象的 `start_video_tream()` 方法将机器人些采集到的视频流通过SDK获取并播放；
  第二种方法通过 `camera` 对象的 `start_video_stream` 方法获取到视频流，之后通过 `cv2.inshow()` 播放获取到的视频流

- 利用 `释放机器人资源`_ 章节的介绍释放相关资源

示例程序中同时提供了一个完整的获取视频流之后利用cv2提供的方法显示图像的例程 :file:`examples/04_camera/01_video_with_display.py`

.. literalinclude:: ./../../../examples/12_drone/16_video_stream.py
   :language: python
   :linenos:
   :lines: 17-

