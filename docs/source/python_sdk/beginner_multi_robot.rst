.. _beginnger:

###########################################
RoboMaster SDK 新手入门 - 多机控制篇
###########################################

多机控制简介
__________________

RobomasterSDK 支持多机控制，用户可以调用相应的多机接口，轻松控制多台机器，实现复杂的多机编队等任务

多机控制流程
__________________

多机控制主要分为以下方面：

    - *多机初始化* ，与局域网内的多台机器建立连接，并初始化相关机器人
    - *多机编号* ，通过飞机的SN号对飞机进行编号，便于后面进行多机的选中控制
    - *多机分组* & *群组控制* ，通过将多台机器进行分组，实现多机选中的效果
    - *任务控制* ，通过任务控制的方式可以同时控制不同组执行不同的动作

接下来本文档将对这几部分别进行介绍。

多机初始化
__________________

环境准备安装netifaces包::

	pip install netifaces

.. tip:: 如果出现以下问题，请下载安装visualcppbuildtools_full.exe(`下载地址：GitHub RoboMaster SDK repository <https://github.com/dji-sdk/robomaster-sdk>`_)

	.. image:: ./../images/neti_err.jpg


1. 首先将机器人设置为路由器组网模式，并将所有机器人与运行 RobomasterSDK 的设备连接至同一个局域网内。
关于本部分如何操作，RobomasterEP参考 :ref:`EpConn` ，教育飞机参考 :ref:`TelloConn`

2. 导入多机控制相关的包::

    from multi_robomaster import multi_robot

3. 生成多机对象

  - 示例一：生成EP机器人多机对象::

      multi_robot = multi_robot.MultiEP()

  - 示例二：生成教育机器人多机对象::

      multi_drones = multi_robot.MultiDrone()


4. 调用多机初始化函数，完成对多机器的扫描以及初始化步骤，EP多机的初始化函数不需要输入参数，
教育飞机的多机初始化函数需要指明需要扫描的飞机数量

  - 示例一：初始化EP机器人多机对象::

      multi_robots.initialize()

  - 示例二：初始化教育无人机对象，飞机的数量为2::

      multi_drones.initialize(2)

.. note:: 注意EP机器人与教育机器人在多机初始化时的区别！

多机编号
_________________

通过将机器人编号，可以方便用户进行多机控制。
目前支持的编号策略为根据输入的SN进行机器人与编号的绑定,多机对象包含以下编号方法::

    number_id_by_sn([id1, SN1], [id2, SN2], [id2, SN3] ...)

方法的参数为一系列包含机器人编号信息的列表，每一个列表包含两个元素:[id, SN]，
第一个元素为期望的编号数字，第二个元素为包含机器人SN信息的字符串, 列表的个数为用户需要编号的机器台数，
且该方法的返回值为成功编号的机器数目

本文档接下来会通过一个EP多机编号的例子带领大家熟悉如何使用该功能，教育无人机的多机编号与EP类似：

    - 示例一：假设我们有两台EP机器人需要编号，且经过之前的步骤创建了并初始化了多机对象 `multi_robots`，
      希望将SN号为 `3JKDH2T001ULTD` 的机器人编号为 `0` 号机器人，
      希望将SN号为 `3JKDH3B001NN0E` 的机器人编号为 `1` 号机器人，则可以使用如下代码完成该编号操作::

        multi_robots.number_id_by_sn([0, '3JKDH2T001ULTD'], [1, '3JKDH3B001NN0E'])

多机分组 & 群组控制
_________________________

通过将机器人分为不同组，可以更加简单的进行多机控制。在进行控制时， `组对象` 的控制接口调用形式与单机类似，在大多数控制情况下，用户可以将一个 `组对象` 想象成一个单机对象使用

生成 `组对象`
##################

用户可以利用包含不同机器人编号（多机编号参考上一小节）的列表，生成包含多个机器人的 `组对象` ，
在之后对该 `组对象` 的操作将作用于组内每个单体机器人上，多机对象支持一下创建 `组对象` 的接口::

    build_group(robot_id_list)

方法的输入参数为包含需要分组的机器人的id信息的列表，方法的返回值为创建的 `组对象` ，接下来本文档会以EP的分组操作举例，
教育机器人的分组方法与其类似：

    - 示例一：假设我们有三台EP机器人，且前面几步骤的操作都已经完成，三台机器人的编号分别为 `0` `1` `2` 号，接下来想将
      `0` 号机器人与 `1` 号机器人放到一组中，将 `2` 号机器人放到一组中，三台机器人同时又属于另一组，则::

        robot_group1 = multi_robots.build_group([0, 1])
        robot_group2 = multi_robots.build_group([2])
        robot_group_all = multi_robots.build_group([0, 1, 2])

      通过以上代码，创建的 `robot_group1` 对象是包含 `0` 号与 `1` 号机器人的 `组对象` ，
      创建的 `robot_group2` 对象是包含 `2` 号机器人的 `组对象` ，
      创建的 `robot_group_all` 对象是包含全部三台机器人的 `组对象` ，我们可以通过这些 `组对象` 控制组内机器人执行同样的命令


`组对象` 的相关操作
#####################



更新成员
+++++++++++++++++

`组对象` 提供支持增添/删除指定成员的功能，对应的对象方法分别是::

    append(self, robots_id_list)
    remove(self, robots_id_list)

方法的输入参数为包含需要添加/删除的机器人的编号的列表，返回值为操作结果，接下来以EP举例，教育飞机类似：

    - 示例一：通过前面的步骤，我们得到了 `组对象` `robot_group_all` ，现在需要将其中的 `1` 号机器人
      与 `2` 号机器人从群组中移除::

        robot_group_all.remove([1, 2])

    - 示例二： 经过思考后，我们认为删除的 `1` 号机器人与 `2` 号机器人还是需要被添加回来::

        robot_group_all.append([1, 2])

群组控制
+++++++++++++++++

在大多数情况下，群组控制的 `动作类接口` 形式与单机控制的接口形式一致，因此用户基本上可以将前面生成的 `组对象` 当成单机对象使用,
一下分别举例EP与教育机器人的两个控制示例：

    - 示例一：假设前面的操作都已经完成，生成的EP `组对象` 为 `robot_group` ，本示例利用该 `组对象` 控制所有EP机器人进行
      底盘与机器人的移动::

        # 组内所有机器人前进1米，程序阻塞至所有机器人动作完成
        robot_group.chassis.move(1, 0, 0, 2, 180).wait_for_completed()

        # 组内所有机器人云台向向左旋转90度，程序阻塞至所有机器人动作完成
        robot_group.gimbal.move(0, 90).wait_for_completed()

目前群组控制支持的api接口列表参考 `多机API列表` ，
列表中的接口参数类别以及取值范围与单机部分相同，使用形式也相同

单机控制
++++++++++++++++

在某些多机控制的场景下，用户可能需要单独控制群组中的某一台机器，RobomasterSDK也支持从群组中获取单机对象，从而进行单机控制。

用户可以通过 `组对象` 的 `get_robot(robot_id)` 方法获取到单机对象，从而进行单机控制，该方法的输入参数为相应机器的编号数字，
返回值为该单机对象。另外用户可以通过"组对象"的 `robot_id_list` 属性获取组内所有机器人的编号列表，
下面本文档将会以教育飞机举例说明，EP机器人使用方法类似：

    - 示例一：假设前面的准备工作都已经完成，`drone_group` 为获取到的“组对象”，可以通过以下代码实现组内的教育飞机依次起飞::

        for drone_id in drone_group.robots_id_list:
            drone_obj = drone_group.get_robot(drone_id)
            drone_obj.flight.takeoff().wait_for_completed()

任务控制
__________________

上一节有介绍如何通过 `组对象` 进行简单的群组控制，但是如何同时让不同组同时做不同的动作？如何在实现不同组同时执行任务的时候保证同步？
本节课来介绍多机对象的 `任务控制` 方法的使用，接口如下::

    run([robot_group1, action_task1], [robot_group2, action_task2], [robot_group3, action_task3]...)

通过该接口，用户可以实现不同的组同时执行不同的动作，并且 `run` 方法会保证该语句执行结束时，方法输入的所有动作任务都执行完毕。
`run` 接口的输入参数为储存任务信息的列表，列表包含两个元素，第一个元素是期望执行任务的 `组对象` ，第二个元素为用户自己编写的的任务函数。
*用户定义的任务函数必须满足固定的接口形式* ，函数应只有一个参数，参数为执行函数内动作的 `组对象` ，下面本文将会以EP机器人举例任务控制接口
的使用，教育飞机的使用方法类似：

    - 示例一：根据前面的教程现在已经获得了三个机器人 `组对象` ，分别为包含 `0` 号机器人与 `1` 号机器人的 `robot_group1`, 包含 `2` 号
      机器人的 `robot_group2` ，以及包含 `1` `2` `3` 号三台机器人的 `robot_group_all` ，我们现在想控制 `robot_group1` 中
      的两台机器人底盘向前移动1m，控制 `robot_group2` 中的 一台机器人向后移动1m， 在这两个任务动作执行完毕后，控制三台机器人全部向左
      移动1m，可以利用如下方法实现

        - 首先定义上述三套动作的任务函数::

            def move_forward_task(robot_group):
                robot_group.chassis.move(x=1, y=0, z=0, xy_speed=0.7).wait_for_completed()


            def move_backward_task(robot_group):
                robot_group.chassis.move(x=-1, y=0, z=0, xy_speed=0.7).wait_for_completed()


            def move_left_task(robot_group):
                robot_group.chassis.move(x=0, y=-1, z=0, xy_speed=0.7).wait_for_completed()

        - 之后在利用多机对象 `multi_robots` 的 `run()` 方法指定 `组对象` 执行上述任务::

            # `0` 号与 `1` 号机器的底盘前进1m, `2` 号机器后退1m
            multi_robots.run([robot_group1, move_forward_task], [robot_group2, move_backward_task])

            # 三台机器的底盘同时左移1m
            multi_robots.run([robot_group_all, move_left_task])

.. note:: 用户自定义的动作任务函数需要满足固定的接口形式！