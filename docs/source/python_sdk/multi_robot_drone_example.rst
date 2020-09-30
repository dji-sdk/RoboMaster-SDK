.. _beginngerDrone:

###############################
RoboMaster SDK 多机编队TT
###############################

初始化无人机
__________________

在进行与无人机相关的操作之前，需要根据指定的配置初始化无人机对象

- 首先从安装的 `multi_robomaster` 包中导入 `multi_robot` 模块::

    from multi_robomaster import multi_robot

- 创建 `MultiDrone` 类的实例对象 `multi_drone`， `multi_drone` 即一个多机控制器的对象::

    multi_drone = multi_robot.MultiDrone()

- 初始化无人机，目前教育系列无人机的初始化需要传入想要控制的飞机数量::

    multi_drone.initialize(drone_num)

至此，无人机的初始化工作就完成了。

对无人机进行编号编组
_____________________

在进行多机控制时我们希望能够简化对飞机控制的流程，需要对飞机进行组队操作，由于SN码是唯一识别一架飞机的信息，
所以在多机编队时需要根据sn码来对飞机进行编队，为了简化编队时的复杂度，SDK要求用户使用自定义的id来对飞机SN码
进行映射

- 在初始化后，使用已经实例化后的 `multi_drone` 对SN进行编号::

    multi_drone.number_id_by_sn([1, "0TQZH79ED00H56"], [2, "0TQZH79ED00H89"])

用户对飞机同一SN进行多个id的映射是被允许的，但是一个id只允许映射一个SN

- 使用已经实例化后的 `multi_drone` 对飞机进行编组::

    multi_drone_group1 = multi_drone.build_group([1, 2])

编组后的结果为 `multi_group` 对象为 `multi_drone_group1` ，用户可以对同一架飞机进行多次编组，如::

    multi_drone_group1 = multi_drone.build_group([1])
    multi_drone_group2 = multi_drone.build_group([1, 2])

- 若用户不期望对飞机进行编号，则可使用 `number_id_to_all_drone` API隐式的对飞机进行0~drone_num的随机编号::

    multi_drone.number_id_to_all_drone()

至此，无人机的编组工作就完成了，接下来可以通过相关接口对无人机进行信息查询、动作控制等操作

控制无人机执行命令
___________________

- 在完成动作编组后，使用已经实例化后的 `multi_drone` 执行动作::

    multi_drone.run([multi_drone_group1, base_action_1])

其中 `multi_drone_group1` 为编组后的 `multi_group` 对象， `base_action_1` 为用户自定义的命令函数，格式为::

    def base_action_1(robot_group):
        robot_group.get_sn()
        robot_group.get_battery()

若想多group同时执行多组动作，可通过如下方式进行，以两个group为例::

    multi_drone.run([multi_drone_group1, base_action_1],
                    [multi_drone_group2, base_action_2])

至此，无人机的执行命令就完成了

释放无人机资源
__________________

在程序的最后，应该手动释放无人机对象相关的资源，包括释放网络地址、结束相应后台线程、释放相应地址空间等，
在 `multi_drone.close` 对象中，提供了用来释放相关资源的方法 `close()`，使用方法如下::

    multi_drone.close()

.. tip:: 为了避免一些意外错误，记得在程序的最后调用 `close()` 方法哦！

查询类接口的使用
____________________

查询类接口即数据获取类接口，用户可以通过该类接口获取无人机自身的状态信息以及传感器状态等信息，
接下来将从查询无人机SN信息与查询无人机电量两个例子来帮助用户掌握该类型接口的用法

示例一：查询机器人SN信息和电量
********************************

- 首先按照 `控制无人机执行命令`_ 章节的介绍完成无人机对象的各项操作

- 对 `base_action_1` (此例中为 `base_task` )进行编写如下:

.. literalinclude:: ./../../../examples/15_multi_robot/multi_drone/02_basic.py
   :language: python
   :linenos:
   :lines: 19-21

飞机的SN号和电量会在控制台打印出来，打印格式为： "DRONE id: {}, reply: {}"

- 利用 `释放无人机资源`_ 章节的介绍释放相关资源

完整的程序参考示例文件 :file:`/examples/15_multi_robot/multi_drone/02_basic.py`

.. literalinclude:: ./../../../examples/15_multi_robot/multi_drone/02_basic.py
   :language: python
   :linenos:
   :lines: 16-

设置类接口的使用
_______________________

设置类接口可以完成对无人机的相关模块的设置，本文档接下来将通过设置扩展led模块讲解设置类接口的使用

.. tip:: 设置扩展led灯目前只有 Tello Talent 机器支持！

示例一：设置无人机扩展led模块
********************************

下面介绍如何通过 SDK 实现设置无人机扩展led模块的操作

- 首先按照 `控制无人机执行命令`_ 章节的介绍完成无人机对象的各项操作

- 对 `base_action_1` 进行编写如下:

.. literalinclude:: ./../../../examples/15_multi_robot/multi_drone/06_led.py
   :language: python
   :linenos:
   :lines: 19-22

使用 `set_led(255, 255, 255)` 接口可以令当前group中所有飞机亮白灯，若想实现不同飞机分别亮不同颜色的灯，
可以使用 `command_dict` 关键字，当使用了 `command_dict` 且其参数类型为dict时，将实现当前group下
不同飞机分别亮灯，如上例所示，1号飞机亮红灯，2号飞机亮绿灯。

值得注意的是，当使用了 `command_dict` 关键字且其参数类型为dict时以后，其他参数将被自动忽略，字典中的飞机数
必须等于当前group中的飞机数，不支持默认设置。

- 利用 `释放无人机资源`_ 章节的介绍释放相关资源

完整的程序参考示例文件 :file:`/examples/15_multi_robot/multi_drone/06_led.py`

.. literalinclude:: ./../../../examples/15_multi_robot/multi_drone/06_led.py
   :language: python
   :linenos:
   :lines: 15-

动作类接口的使用
_____________________________

动作类接口是用来控制无人机执行飞行动作的接口，本文档接下来将讲解飞行类接口的使用

.. warning:: 飞机固件版本v2.5.1.4 和 wifi模块版本v1.0.0.33 以下的用户，请升级后再使用动作类接口，否则会导致执行飞行动作异常，查询方式请参考单机接口文档

示例一：控制飞机起飞并前后飞行
********************************

在本例程中，首先需要控制两组共两架飞机起飞，之后控制飞机起飞并向前向后各飞行100cm

- 首先按照 `控制无人机执行命令`_ 章节的介绍完成无人机对象的各项操作,随后编写如下程序:

.. literalinclude:: ./../../../examples/15_multi_robot/multi_drone/03_takeoff_land.py
   :language: python
   :linenos:
   :lines: 16-

- 利用 `释放无人机资源`_ 章节的介绍释放相关资源

.. warning:: 不同于单机，多机执行飞行动作时，wait_for_completed()接口为必写项，如忘记书写则可能导致当前动作的下一动作无法运行，在等待一段时间后会执行当前动作之后的第二个动作

示例二：控制飞机移动到目标坐标点
********************************

在本例程中，首先需要控制两架飞机起飞，之后控制飞机起飞并以大地毯中点为圆心，
以50cm为边长，在100cm高度上以100cm/s的速度按正方形轨迹运动

- 首先按照 `控制无人机执行命令`_ 章节的介绍完成无人机对象的各项操作

- 对 `base_action_1` 进行编写如下:

.. literalinclude:: ./../../../examples/15_multi_robot/multi_drone/05_go.py
   :language: python
   :linenos:
   :lines: 19-29

值得注意的是，多机编队的go指令强制用户使用地毯坐标进行运动，为了编程安全不支持飞机自身坐标系移动，
字典中的飞机数必须等于当前group中的飞机数，不支持默认设置。

- 利用 `释放无人机资源`_ 章节的介绍释放相关资源

完整的程序参考示例文件 :file:`/examples/15_multi_robot/multi_drone/05_go.py`

.. literalinclude:: ./../../../examples/15_multi_robot/multi_drone/05_go.py
   :language: python
   :linenos:
   :lines: 16-