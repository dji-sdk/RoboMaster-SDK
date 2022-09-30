.. _beginngerEp:

####################################
RoboMaster SDK 新手入门 - EP 篇
####################################

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

- 创建 `Robot` 类的实例对象 `ep_robot`， `ep_robot` 即一个机器人的对象::

    ep_robot = robot.Robot()

- 初始化机器人，如果调用初始化方法时不传入任何参数，则使用config.py中配置的默认连接方式（WIFI直连模式）
  以及默认的通讯方式（udp通讯）对机器人进行初始化，在本示例中我们手动指定机器人的连接方式为组网模式,
  不指定通讯方式使用默认配置::

    ep_robot.initialize(conn_type="sta")

..

  可以通过以下语句设置默认的连接方式与通讯方式，本例中将默认的连接方式设置为 `sta` 模式，
  默认的通讯方式设置为 `tcp` 方式::


    config.DEFAULT_CONN_TYPE = "sta"
    config.DEFAULT_PROTO_TYPE = "tcp"


至此，机器人的初始化工作就完成了，接下来可以通过相关接口对机器人进行信息查询、动作控制、多媒体使用等操作，
本文档将在后面的部分对几类接口的使用分别进行介绍

获取模块对象
__________________

部分 SDK 接口属于 `Robot` 对象本身，因此可以通过 `Robot` 对象直接调用，
但是一些接口属于 `Robot` 对象包含的其他模块，比如装甲灯的设置接口在 `led` 模块对象中，
底盘的控制接口在 `chassis` 模块对象中，等等。如果想使用这些接口需要首先获得相应的对象，
这里以获取 `led` 模块对象举例，介绍如何获取这些对象

- 首先按照 `初始化机器人`_ 章节的介绍完成机器人对象的初始化操作

- 可以使用两种方法获取 `led` 对象

  - 方法一：直接使用 `.` 运算符从 `Robot()` 对象中获取 `led` 对象::

        ep_led = ep_robot.led


  - 方法二：利用 `Robot` 对象的 `get_module()` 方法获得指定的对象::

        ep_led = ep_robot.get_module("led")

获取了相关对象，便可以通过该对象调用其所包含的 SDK 接口


释放机器人资源
__________________

在程序的最后，应该手动释放机器人对象相关的资源，包括释放网络地址、结束相应后台线程、释放相应地址空间等，
在 `Robot` 对象中，提供了用来释放相关资源的方法 `close()`，使用方法如下::

    ep_robot.close()

.. tip:: 为了避免一些意外错误，记得在程序的最后调用 `close()` 方法哦！

查询类接口的使用
________________

查询类接口即数据获取类接口，用户可以通过该类接口获取机器人自身的状态信息以及传感器状态等信息，
接下来将从查询机器人版本信息与查询机器人SN号两个例子来帮助用户掌握该类型接口的用法

示例一：查询机器人版本
************************

- 首先按照 `初始化机器人`_ 章节的介绍完成机器人对象的初始化操作

- 使用`Robot` 对象的 `get_version()` 方法，方法的返回值即为代表机器人版本号的字符串，
  并且将获取到的版本号打印出来::

    ep_version = ep_robot.get_version()
    print("Robot Version: {0}".format(ep_version))

- 利用 `释放机器人资源`_ 章节的介绍释放相关资源

完整的程序参考示例文件 :file:`/examples/01_robot/01_get_version.py`

.. literalinclude:: ./../../../examples/01_robot/01_get_version.py
   :language: python
   :linenos:
   :lines: 17-

示例二：获取机器人SN号
************************

- 首先按照 `初始化机器人`_ 章节的介绍完成机器人对象的初始化操作

- 利用 `Robot` 对象使用 `get_sn()` 方法，方法的返回值即为代表机器人SN号的字符串，
  并且将获取到的SN号打印出来::

    SN = ep_robot.get_sn()
    print("Robot SN:", SN)

- 利用 `释放机器人资源`_ 章节的介绍释放相关资源

完整的程序参考示例文件 :file:`/examples/01_robot/02_get_sn.py`

.. literalinclude:: ./../../../examples/01_robot/02_get_sn.py
   :language: python
   :linenos:
   :lines: 17-

设置类接口的使用
_______________________

设置类接口可以完成对机器人的相关模块的设置，本文档接下来将通过设置机器人整机运动模式与设置机器人装甲灯两个例子讲解设置类接口的使用

示例一：设置机器人整机运动模式
********************************

机器人的运动模式有三种：自由模式（FREE）、云台跟随底盘（CHASSIS_LEAD）、底盘跟随云台（GIMBAL_LEAD），
本文档以设置机器人的运动模式为底盘跟随云台（CHASSIS_LEAD）为例带大家熟悉如何使用设置类接口

- 首先按照 `初始化机器人`_ 章节的介绍完成机器人对象的初始化操作

- 使用`Robot` 对象中的 `set_robot_mode()` 方法设置机器人的整机运动模式，
  机器人的模式定义在 :file:`/examples/01_robot/02_get_sn.py` 中，
  `FREE` ， `GIMBAL_LEAD` , `CHASSIS_LEAD` 是可选的三个参数，
  本示例中设置机器人的整机运动模式为底盘跟随云台模式（`GIMBAL_LEAD`）::

    ep_robot.set_robot_mode(mode=robot.GIMBAL_LEAD)

- 利用 `释放机器人资源`_ 章节的介绍释放相关资源

完整的程序参考示例文件 :file:`/examples/01_robot/09_set_mode.py`

.. literalinclude:: ./../../../examples/01_robot/09_set_mode.py
   :language: python
   :linenos:
   :lines: 17-

示例二：设置机器人装甲灯
********************************

下面介绍如何通过 SDK 实现设置机器人装甲灯的操作

- 首先按照 `初始化机器人`_ 章节的介绍完成机器人对象的初始化操作,
  另外由于设置灯效时要使用 `led` 模块中关于装甲灯的一些定义，因此需要额外导入 `led` 模块::

    from robomaster import led

- 机器人的装甲灯设置接口属于 `Robot`对象包含的 `led` 模块，因此首先需要获取 `led` 对象，
  按照 `获取模块对象`_ 章节的介绍获取 `led` 对象, 本示例中使用方法一获取模块对象::

    ep_led = ep_robot.led

- 使用 `led` 对象中的 `set_led()` 方法设置机器人的装甲灯效果，
  在使用 `led` 方法时，通过 `comp` 参数选定要控制的装甲灯， 通过 `r` `g` `b` 参数指定灯的颜色，
  通过 `effect` 参数指定led灯的显示效果。
  在本例中，控制的装甲灯对象通过 `comp` 选定为所有装甲灯， `r` `g` `b` 颜色指定为红色，
  `effect` 选定的灯效为常亮灯效::

    ep_led.set_led(comp=led.COMP_ALL, r=255, g=0, b=0, effect=led.EFFECT_ON)

- 利用 `释放机器人资源`_ 章节的介绍释放相关资源

示例程序中提供了一个完整的设置装甲灯的例程 :file:`/examples/01_robot/07_led.py`，
例程中利用了for循环，实现了led灯的8次颜色变换，每次维持1秒钟

.. literalinclude:: ./../../../examples/07_led/01_set_led.py
   :language: python
   :linenos:
   :lines: 17-


动作类接口的使用
_____________________________

动作类接口是用来控制机器人执行某些指定动作的接口，根据动作本身特性的不同，
SDK中包含 *即时动作控制* 与 *任务动作控制* 两类动作接口

即时动作控制
*************

即时控制类动作是指设置后马上生效的动作，特指宏观上是“瞬时”执行的动作，
接下来本文档将通过控制发射器射击与控制底盘速度两个例子带大家熟悉此类动作接口

示例一：控制发射器射击
++++++++++++++++++++++++++++

- 首先按照 `初始化机器人`_ 章节的介绍完成机器人对象的初始化操作,
  另外由于使用发射器接口时要使用 `blaster` 模块中关于发射器的一些定义，因此需要额外导入 `blaster` 模块::

    from robomaster import blaster

- 发射器的控制接口属于 `blaster` 模块，首先按照 `获取模块对象`_ 章节的介绍获取 `blaster` 对象,
  本示例中使用方法一获取模块对象::

    ep_blaster = ep_robot.blaster

- 使用 `blaster` 对象中的 `fire()` 方法控制发射器射击， 方法的参数 `fire_type` 可以指定发射的类型，
  可选水弹、红外弹，在本示例中我们使用水弹， 参数 `times` 设置发射的次数，本示例中指定发射的次数为1::

    ep_balseter.fire(fire_type=balseter.WATER_FIRE, times=1)

- 利用 `释放机器人资源`_ 章节的介绍释放相关资源

示例程序中提供了一个完整的控制发射器射击的例程 :file:`examples/06_blaster/01_fire.py`

.. literalinclude:: ./../../../examples/06_blaster/01_fire.py
   :language: python
   :linenos:
   :lines: 17-

示例二：控制底盘速度
++++++++++++++++++++++++++++

控制底盘速度是一种典型的即时控制，发出控制指令后机器人将会立即按照指定速度运动

- 首先按照 `初始化机器人`_ 章节的介绍完成机器人对象的初始化操作

- 底盘控制接口属于 `chassis` 模块，首先按照 `获取模块对象`_ 章节的介绍获取 `chassis` 对象,
  本示例中使用方法一获取模块对象::

    ep_chassis= ep_robot.chassis

- 使用 `chassis` 对象中的 `dirve_speed()` 方法控制底盘的速度，
  方法的参数 `x` `y` `z` 分别代表前进、横移、旋转速度， 本示例中指定 `x` 前进速度点为 0.5 m/s,
  `timeout` 参数可以指定一个时间，超过该时间未接收到控制速度指令，SDK 将会主动控制机器人停止，
  本示例中指定 `timeout` 为 5s, 在机器人按照指定速度运行3s后，将速度设置为 0 ::

    ep_chassis.drive_speed(x=0.5, y=0, z=0, timeout=5)
    time.sleep(3)
    ep_chassis.drive_speed(x=0, y=0, z=0, timeout=5)

- 利用 `释放机器人资源`_ 章节的介绍释放相关资源

示例程序中提供了一个完整的控制底盘速度的例程 :file:`examples/02_chassis/03_speed.py`，
例程中每次令机器人按照指定速度运动三秒钟，然后改变速度

.. literalinclude:: ./../../../examples/02_chassis/03_speed.py
   :language: python
   :linenos:
   :lines: 17-

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


示例一：控制底盘移动指定距离
+++++++++++++++++++++++++++++++

控制底盘移动指定距离是一种任务动作控制

- 首先按照 `初始化机器人`_ 章节的介绍完成机器人对象的初始化操作

- 底盘控制接口属于 `chassis` 模块，首先按照 `获取模块对象`_ 章节的介绍获取 `chassis` 对象,
  由于本示例中同时也会控制装甲灯，因此也需要获取 `led` 模块，
  本示例中使用方法一获取模块对象::

    ep_chassis = ep_robot.chassis
    ep_led = ep_robot.led

- 在本示例中为了说明任务类动作的特点，在控制底盘运动后会设置装甲灯灯效。
  使用 `chassis` 对象中的 `move()` 方法控制底盘的相对位置移动，
  方法的参数 `x` `y` 代表 `x` 轴 `y` 轴的运动距离， 参数 `z` 代表 `z` 轴的旋转速度，
  本示例中指定 `x` 轴的运动距离为 0.5 m, `y` `z` 两参数为 0，
  `xy_speed` 参数可以指定 `xy` 两轴的运动速度， `z_speed` 参数用来指定 `z` 轴的旋转速度，
  本示例中指定 `xy` 轴的运动速度为 0.7 m/s, `z` 轴的旋转速度设置为 0。
  设置装甲灯灯效可以参考 `示例二：设置机器人装甲灯`_ 。接下来本文档会使用三种方法控制底盘移动的任务动作：

  - 方法一：执行任务动作后，立即调用 `wait_for_completed()` 方法::

     ep_chassis.move(x=x_val, y=0, z=0, xy_speed=0.7).wait_for_completed()
     ep_led.set_led(comp=led.COMP_ALL, r=255, g=0, b=0, effect=led.EFFECT_ON)

  - 方法二：在执行其他命令后再调用 `wait_for_completed()` 方法::

     chassis_action = ep_chassis.move(x=x_val, y=0, z=0, xy_speed=0.7)
     ep_led.set_led(comp=led.COMP_ALL, r=255, g=0, b=0, effect=led.EFFECT_ON)
     chassis_action.wait_for_completed()

  - 方法三：不使用 `wait_for_completed()` 方法，利用延时来保证动作执行结束::

     ep_chassis.move(x=x_val, y=0, z=0, xy_speed=0.7)
     ep_led.set_led(comp=led.COMP_ALL, r=255, g=0, b=0, effect=led.EFFECT_ON)
     time.sleep(10)

  三种任务动作接口的调用形式对应机器人的行为不同，*方法一* 机器人会先移动到指定位置之后装甲灯再全亮红色，
  而 *方法二* 与 *方法三* 则会在移动的过程中装甲灯全亮红色。

.. tip:: 建议使用 *方法一* 以及 *方法二* ，在合适的时机调用 `wait_for_completed()` 是比较安全的做法

- 利用 `释放机器人资源`_ 章节的介绍释放相关资源

示例程序中提供了一个完整的控制底盘移动指定距离的例程 :file:`examples/02_chassis/01_move.py`，

.. literalinclude:: ./../../../examples/02_chassis/01_move.py
   :language: python
   :linenos:
   :lines: 17-


多媒体接口的使用
______________________________________

多媒体接口主要包括视频流与音频流两部分，接下来将通过两个示例介绍该类型接口的使用

示例一：获取视频流
**********************

获取机器人采集到的视频流有助于实现一些非常实用的案例，下面本文档将介绍如何通过 SDK 获取视频流

- 首先按照 `初始化机器人`_ 章节的介绍完成机器人对象的初始化操作，
  由于示例中会用到 `camera` 模块的相关定义，因此还需要导入 `camera` 模块::

    from robomaster import camera

- 获取视频流相关的接口属于属于 `camera` 模块，首先按照 `获取模块对象`_ 章节的介绍获取 `camera` 对象,
  本示例中使用`获取模块对象`_ 章节介绍的方法一获取模块对象::

    ep_camera= ep_robot.camera

- `camera` 模块的 `start_video_stream` 方法有两个参数， `display` 参数指定是否显示获取到的视频流，
  `resolution` 参数指定视频的尺寸大小。在本示例中，向大家介绍两种获取视频流的方法，

  - 方法一：获取视频流并直接播放显示十秒::

        ep_camera.start_video_stream(display=True, resolution=camera.STREAM_360P)
        time.sleep(10)
        ep_camera.stop_video_stream()

  - 方法二：获取视频流，通过cv2提供的方法显示200帧图像::

        ep_camera.start_video_stream(display=False)
        for i in range(0, 200):
            img = ep_camera.read_cv2_image()
            cv2.imshow("Robot", img)
            cv2.waitKey(1)
        cv2.destroyAllWindows()
        ep_camera.stop_video_stream()

  第一种方法直接通过 `camera` 对象的 `start_video_tream()` 方法将机器人些采集到的视频流通过SDK获取并播放；
  第二种方法通过 `camera` 对象的 `start_video_stream` 方法获取到视频流，之后通过 `cv2.inshow()` 播放获取到的视频流

- 利用 `释放机器人资源`_ 章节的介绍释放相关资源

示例程序中提供了一个完整的获取并直接显示视频流的例程 :file:`examples/04_camera/01_video_with_display.py`

.. literalinclude:: ./../../../examples/04_camera/01_video_with_display.py
   :language: python
   :linenos:
   :lines: 17-

示例程序中同时提供了一个完整的获取视频流之后利用cv2提供的方法显示图像的例程 :file:`examples/04_camera/03_video_without_display.py`

.. literalinclude:: ./../../../examples/04_camera/03_video_without_display.py
   :language: python
   :linenos:
   :lines: 17-

示例二：获取音频流
**********************

本示例将会通过 SDK 获取机器人采集到的音频流， 并将获取到的音频信息以 `wav` 文件的形式保存在本地

- 首先按照 `初始化机器人`_ 章节的介绍完成机器人对象的初始化操作

- 获取视频流相关的接口属于属于 `camera` 模块，首先按照 `获取模块对象`_ 章节的介绍获取 `camera` 对象,
  本示例中使用`获取模块对象`_ 章节介绍的方法一获取模块对象::

    ep_camera= ep_robot.camera

- 通过调用 `camera` 模块的 `record_audio()` 方法，将获取到的音频流保存在本地，
  方法的 `save_file` 参数可以指定保存文件的名称， `seconds` 参数可以指定采集的音频时长，
  `sample_rate` 参数指定采集频率::

    ep_camera.record_audio(save_file="output.wav", seconds=5, sample_rate=16000)

- 利用 `释放机器人资源`_ 章节的介绍释放相关资源

示例程序中提供了一个完整的获取音频流并保存在本地的例程 :file:`examples/04_camera/05_record_audio.py`

.. literalinclude:: ./../../../examples/04_camera/05_record_audio.py
   :language: python
   :linenos:
   :lines: 17-
