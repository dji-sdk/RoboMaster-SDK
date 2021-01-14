.. _beginnger:

#################################################################
Getting Started with the RoboMaster SDK - Multi-device Control
#################################################################

Introduction to multi-device control
__________________________________________

The RoboMaster SDK supports multi-device control. By calling corresponding multi-device interfaces, you can easily control multiple devices in order to perform complex multi-device formations and other tasks.

Multi-device control process
_______________________________

Multi-device control mainly consists of the following processes:

    - *Multi-device initialization*: Establish a connection with multiple devices in the LAN and initialize relevant robots.
    - *Multi-device numbering*: Number drones by their SNs to facilitate the selection and control of multiple devices.
    - *Multi-device grouping* and *Group control*: Group multiple devices to facilitate multi-device selection.
    - *Task control*: Control different groups to perform different actions simultaneously through task control.

The following sections describe each of those processes.

Multi-device initialization
_____________________________

Install the netifaces package for environment preparation.::

	pip install netifaces

.. tip:: If the following error occurs, download and install visualcppbuildtools_full.exe (`from the GitHub RoboMaster SDK repository <https://github.com/dji-sdk/robomaster-sdk>`_) instead.

	.. image:: ./../images/neti_err.jpg


1. First, set the robot to work in router networking mode. Then, connect all robots and the device running the RoboMaster SDK to the same LAN.
For details, refer to :ref:`EpConn` for RoboMaster EP and :ref:`TelloConn` for education-series drones.

2. Import the packages related to multi-device control.::

    from multi_robomaster import multi_robot

3. Generate multi-device objects

  - Example 1: Generate a multi-device object for EP robots::

      multi_robot = multi_robot.MultiEP()

  - Example 2: Generate a multi-device object for education-series robots::

      multi_drones = multi_robot.MultiDrone()


4. Call the multi-device initialization function to complete the multi-device scanning and initialization steps. The initialization function for EP multi-device control does not require any input parameters.
The multi-device initialization function for education-series drones requires you to specify the number of vehicles to be scanned for.

  - Example 1: Initialize the multi-device object for EP robots::

      multi_robots.initialize()

  - Example 2: Initialize the multi-device object for 2 education-series drones::

      multi_drones.initialize(2)

.. note:: Take note of the difference in multi-device initialization between EP robots and education-series robots.

Multi-device numbering
__________________________

Number the robots to facilitate multi-device control.
The currently supported numbering method is to bind a robot with a number based on the entered SN. The numbering methods for multi-device objects are described below.::

    number_id_by_sn([id1, SN1], [id2, SN2], [id2, SN3] ...)

The method parameter is an array of robot number information, with each element in the array consisting of two items: [id, SN].
The first item is the desired ID, and the other item is the robot SN string. The number of elements is the number of devices that the user needs to number.
The return value of this method is the number of successfully numbered devices.

The following example of EP multi-device numbering will help you understand how to use this function. The multi-device numbering process for education-series devices is similar to that for EP devices.

    - Example 1: Assume that two EP robots need to be numbered and the `multi_robots` multi-device object has been created and initialized.
      Now, you want to number the robot with the SN `3JKDH2T001ULTD` as robot `0`
      and the robot with the SN `3JKDH3B001NN0E` as robot `1`. To do this, execute the following statement:::

        multi_robots.number_id_by_sn([0, '3JKDH2T001ULTD'], [1, '3JKDH3B001NN0E'])

Multi-device grouping and group control
____________________________________________

By grouping robots, you can easily implement multi-device control. During control, the call method of the control interface for a `group object` is similar to that for a standalone device. In most control situations, you can think of a `group object` as a standalone object.

Generate a `group object`
###########################

You can use the array of robot number information pairs (see the previous section for multiple-device numbering) to generate a `group object` containing multiple robots.
In this way, operations on this `group object` act on each robot in the group. Multi-device objects support the following interface for creating `group objects`:::

    build_group(robot_id_list)

The input parameter of the method is a list of ID information of the robots that need to be grouped, and the return value of the method is the created `group object`. The following example explains how to group EP devices.
The grouping method for education-series robots is similar to this method.

    - Example 1: Assume that there are three EP robots and the previous steps have been completed. The numbers of these robots are `0`, `1`, and `2`.
      Now, you want to place robots `0` and `1` into a group, robot `2` into another group, and all three robots in a third group. To do this, execute the following statements:::

        robot_group1 = multi_robots.build_group([0, 1])
        robot_group2 = multi_robots.build_group([2])
        robot_group_all = multi_robots.build_group([0, 1, 2])

      After running the code above, the created `robot_group1` object is the `group object` containing robots `0` and `1`.
      The created `robot_group2` object is the `group object` containing robot `2`.
      The created `robot_group_all` object is the `group object` containing all three robots. Then, you can use these `group objects` to control the robots they contain to have them execute the same commands.


Operations related to `group objects`
######################################



Update members
+++++++++++++++++

You can add/remove specified members to/from `group objects`. The related object methods are as follows:::

    append(self, robots_id_list)
    remove(self, robots_id_list)

The input parameter of the method is a list of the numbers of robots to be added or deleted, and the return value is the execution result of the method. The following example is for EP robots. For education-series robots, the process is similar.

    - Example 1: Generate the `robot_group_all` `group object` by completing the previous steps. Then, delete robots `1` and
      `2` from the group.::

        robot_group_all.remove([1, 2])

    - Example 2: Add the deleted robots `1` and `2` back to the group.::

        robot_group_all.append([1, 2])

Group control
+++++++++++++++++

In most cases, the "action interface" for group control is used just as that for standalone control. Therefore, you can basically use the generated group object as a standalone object.
The following two examples explain how to control EP robots and education-series robots.

    - Example 1: Assume that the previous steps have been completed and the generated EP `group object` is `robot_group`. In this example, this `group object` is used to control all EP robots
      in order to move their chasses and the robots themselves.::

        # Move all robots in the group forward 1 meter and block the program until all the robot actions are completed.
        robot_group.chassis.move(1, 0, 0, 2, 180).wait_for_completed()

        # Rotate the gimbals of all robots in the group 90 degrees to the left and block the program until all the robot actions are completed.
        robot_group.gimbal.move(0, 90).wait_for_completed()

For the list of APIs currently supported for group control, refer to the `List of Multi-device APIs`.
The parameter categories and value ranges of APIs in the list are the same as those for standalone devices and they are used in the same way.

Standalone control
++++++++++++++++++++

In some multi-device control scenarios, you may want to control a certain device in the group. The RoboMaster SDK supports obtaining single-device objects from groups for single-device control.

You can obtain a standalone object by using the `get_robot(robot_id)` method of the `group object` for the purpose of standalone control. The input parameter of this method is the number of the target device,
and the return value is the standalone object. In addition, you can obtain the number list of all robots in the group by using the `robot_id_list` attribute of the `group object`.
The following example is for education-series robots. The process for EP robots is similar to the method in this example.

    - Example 1: Assume that the previous steps have been completed and `drone_group` is the obtained `group object`. Now, you can execute the following statements to perform take off for each education-series drone in the group in sequence.::

        for drone_id in drone_group.robots_id_list:
            drone_obj = drone_group.get_robot(drone_id)
            drone_obj.flight.takeoff().wait_for_completed()

Task control
__________________

The previous section explained how to perform simple group control with `group objects`. However, you may also want to make different groups perform different actions at the same time and ensure synchronization when different groups perform tasks simultaneously.
This section explains how to use the `task control` method for multi-device objects. In this case, the required interface is as follows:::

    run([robot_group1, action_task1], [robot_group2, action_task2], [robot_group3, action_task3]...)

Through this interface, you can make different groups perform different actions at the same time. The `run` method ensures that all action tasks input by the method are performed when the statement is fully executed.
The input parameter of the `run` interface is an array of task information. Each element in the array consists of two items: the `group object` that will perform the task and the task function written by the user.
*User-defined task functions must meet certain interface development conditions*. That is, each task function has only one parameter, which is the `group object` that executes the action in the function. The following example explains how to use the control interface for EP robots.
The process for education-series robots is similar to the process in this example.

    - Example 1: Assume that three robot `group objects` have been obtained by completing the previous steps. Specifically, these group objects are `robot_group1` containing robots `0` and `1`,
      `robot_group2` containing robot `2`, and `robot_group_all` containing robots `1`, `2`, and `3`. Now, you want to instruct the chasses of the two robots in `robot_group1`
      to move forward 1 meter, instruct the only robot in `robot_group2` to move backward 1 meter, and instruct the three robots to move
      leftward 1 meter after completing the prior two task actions. To do this, you can use the following method.

        - First, define task functions for the three actions.::

            def move_forward_task(robot_group):
                robot_group.chassis.move(x=1, y=0, z=0, xy_speed=0.7).wait_for_completed()


            def move_backward_task(robot_group):
                robot_group.chassis.move(x=-1, y=0, z=0, xy_speed=0.7).wait_for_completed()


            def move_left_task(robot_group):
                robot_group.chassis.move(x=0, y=-1, z=0, xy_speed=0.7).wait_for_completed()

        - Then, use the `run()` method of the `multi_robots` multi-device object to specify `group objects` to perform these tasks.::

            # Move the chasses of robots `0` and `1` forward 1 meter and move robot `2` backward 1 meter.
            multi_robots.run([robot_group1, move_forward_task], [robot_group2, move_backward_task])

            # Move the chasses of all three robots leftward 1 meter.
            multi_robots.run([robot_group_all, move_left_task])

.. note:: User-defined action task functions must meet the interface development conditions.