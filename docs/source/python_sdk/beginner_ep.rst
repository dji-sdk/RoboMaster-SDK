.. _beginnerEp:

################################################
Getting Started with the RoboMaster SDK - EP
################################################

Initialize the robot
______________________

Before performing robot-related operations, you must initialize the robot object according to the specified configuration.

- First, import the `robot` module from the installed `robomaster` package.::

    from robomaster import robot

- Specify the local IP address of the SDK (if you want to specify it manually). In this example, the retrieved local IP address is `192.168.2.20`.
  (For example, in the Windows operating system, press the `Win+R` shortcut command and then enter `cmd` in the window that appears.
  Enter `ipconfig` in the window to view the IP address of the device.)
  To specify the IP address, run the following statement::

    robomaster.config.LOCAL_IP_STR = "192.168.2.20"

.. tip:: In most cases, the SDK can automatically obtain the correct local IP address, so you do not need to manually specify it. However, when the SDK runs on a device with multiple network cards,
  the automatically obtained IP address may not be the one used to connect to the robot. In this case, you need to manually specify the IP address.

- Create an `ep_robot` instance object of the `Robot` class. Here, `ep_robot` is a robot object.::

    ep_robot = robot.Robot()

- Initialize the robot. If no input parameters are specified when you call the initialization method, the default connection mode configured in config.py (the Wi-Fi direct connection mode)
  and the default communication method (UDP communication) are used to initialize the robot. In this example, the connection mode of the robot is manually set to the networking mode.
  Do not specify the communication method to use the default one.::

    ep_robot.initialize(conn_type="sta")

..

  You can set the default connection mode and communication method by running the following statement. In this example, the default connection method is set to `sta`,
  and the default communication method is set to `tcp`.::


    config.DEFAULT_CONN_TYPE = "sta"
    config.DEFAULT_PROTO_TYPE = "tcp"


Now, the initialization of the robot is completed. Then, you can use the robot for information query, motion control, and multimedia use through related interfaces.
Later, this document will introduce the use of several types of interfaces.

Obtain module objects
_________________________

Some SDK interfaces belong to the `Robot` object itself so they can be directly called through the `Robot` object.
However, certain interfaces belong to other modules in the `Robot` object. For example, the interface for configuring the armored light is in the `led` module object,
and the interface for controlling the chassis is in the `chassis` module object. To use these interfaces, you must first obtain the corresponding objects.
The following uses the `led` module object as an example to explain how to obtain these objects.

- First, initialize the robot object as described in the `Initialize the robot`_ section.

- You can obtain the `led` object in two ways.

  - Method 1: Directly use the `.` operator to obtain the `led` object from the `Robot()` object.::

        ep_led = ep_robot.led


  - Method 2: Use the `get_module()` method of the `Robot` object to obtain the specified object.::

        ep_led = ep_robot.get_module("led")

After obtaining the object, you can call the SDK interfaces contained in it through the object.


Release robot resources
__________________________

At the end of the program, you need to manually release the resources related to the robot object, including releasing the network address, ending the corresponding background thread, and releasing the corresponding address space.
The `Robot` object provides the `close()` method for releasing these resources, which can be used as follows.::

    ep_robot.close()

.. tip:: To avoid unexpected errors, be sure to call the `close()` method at the end of the program.

Use the query interface
__________________________

The query interface is the data acquisition interface, through which you can obtain the status of the robot and the status of sensors.
The following two examples of querying the robot version and querying the robot SN can help you understand the usage of this interface.

Example 1: Query the version number of the robot
*****************************************************

- First, initialize the robot object as described in the `Initialize the robot`_ section.

- Use the `get_version()` method of the `Robot` object. The return value of the method is the version number string of the robot.
  Print the obtained version number.::

    ep_version = ep_robot.get_version()
    print("Robot Version: {0}".format(ep_version))

- Release relevant resources as described in the `Release robot resources`_ section.

For the full process, refer to the :file:`/examples/01_robot/01_get_version.py` sample file.

.. literalinclude:: ./../../../examples/01_robot/01_get_version.py
   :language: python
   :linenos:
   :lines: 17-

Example 2: Obtain the SN of the robot
*****************************************

- First, initialize the robot object as described in the `Initialize the robot`_ section.

- Use the `get_sn()` method of the `Robot` object. The return value of the method is the SN string of the robot.
  Print the obtained SN.::

    SN = ep_robot.get_sn()
    print("Robot SN:", SN)

- Release relevant resources as described in the `Release robot resources`_ section.

For the full process, refer to the :file:`/examples/01_robot/02_get_sn.py` sample file.

.. literalinclude:: ./../../../examples/01_robot/02_get_sn.py
   :language: python
   :linenos:
   :lines: 17-

Use the setup interface
_______________________

The setup interface is used to configure the modules of the robot. This section uses configuring the overall robot movement mode and configuring the robot armored light to explain how to use the setup interface.

Example 1: Configure the overall movement mode of the robot
**************************************************************

The robot has three movement modes: free mode (FREE), gimbal follows chassis (CHASSIS_LEAD), and chassis follows gimbal (GIMBAL_LEAD).
This document sets the movement mode of the robot to chassis follows gimbal (CHASSIS_LEAD) in order to illustrate the use of the setup interface.

- First, initialize the robot object as described in the `Initialize the robot`_ section.

- Use the `set_robot_mode()` method in the `Robot` object to set the overall movement mode of the robot.
  This mode is defined in :file:`/examples/01_robot/02_get_sn.py`.
  `FREE`, `GIMBAL_LEAD`, and `CHASSIS_LEAD` are the three options for this parameter.
  In this example, the overall movement mode of the robot is set to chassis follows gimbal (`GIMBAL_LEAD`).::

    ep_robot.set_robot_mode(mode=robot.GIMBAL_LEAD)

- Release relevant resources as described in the `Release robot resources`_ section.

For the full process, refer to the :file:`/examples/01_robot/09_set_mode.py` sample file.

.. literalinclude:: ./../../../examples/01_robot/09_set_mode.py
   :language: python
   :linenos:
   :lines: 17-

Example 2: Configure the armored light of the robot
*********************************************************

The process of configuring the armored light of the robot through the SDK is as follows.

- First, initialize the robot object as described in the `Initialize the robot`_ section.
  You also need to import the `led` module because some definitions for the armored light in this module will be used to configure the light effect.::

    from robomaster import led

- You must obtain the `led` object first, because the armored light configuration interface of the robot belongs to the `led` module contained in the `Robot` object.
  Obtain the `led` object as described in the `Obtain module objects`_ section. In this example, method 1 is used to obtain module objects.::

    ep_led = ep_robot.led

- Use the `set_led()` method in the `led` object to configure the armored light effect of the robot.
  When using the `led` method, use the `comp` parameter to select the armored light that you want to control, the `r`, `g`, and `b` parameters to specify the light color,
  and the `effect` parameter to specify the lighting effect of the LED light.
  In this example, all armored lights are selected for control by `comp`, `r`, `g`, and `b` are set to specify the color red,
  and solid on is selected as the lighting effect by `effect`.::

    ep_led.set_led(comp=led.COMP_ALL, r=255, g=0, b=0, effect=led.EFFECT_ON)

- Release relevant resources as described in the `Release robot resources`_ section.

For the full process of configuring the armored light, refer to the :file:`/examples/01_robot/09_set_mode.py` sample program.
In this process, the for loop is used to implement 8 color changes of the LED light, each of which lasts for 1 second.

.. literalinclude:: ./../../../examples/07_led/01_set_led.py
   :language: python
   :linenos:
   :lines: 17-


Use the action interface
_____________________________

The action interface is used to control the robot to perform certain specified actions. Based on the characteristics of actions,
the SDK provides two types of action interfaces: *instant action control* and *task action control*.

Instant action control
*************

Instant control actions are actions that are performed immediately after being configured. Such actions refer to actions that are "instantaneously" performed from an overall perspective.
Next, this document will explain how to control the firing of the blaster and control the speed of the chassis to help you understand this action interface.

Example 1: Control the firing of the blaster
++++++++++++++++++++++++++++++++++++++++++++++++

- First, initialize the robot object as described in the `Initialize the robot`_ section.
  You also need to import the `blaster` module because some definitions for the blaster in this module will be used to control the blaster.::

    from robomaster import blaster

- The interface for controlling the blaster belongs to the `blaster` module. Therefore, first obtain the `blaster` object as described in the `Obtain module objects`_ section.
  This example uses method 1 to obtain module objects.::

    ep_blaster = ep_robot.blaster

- Use the `fire()` method in the `blaster` object to control the firing of the blaster, the `fire_type` parameter of the method to specify the firing type
  (which can be water bomb or infrared bomb; water bomb is used in this example), and the `times` parameter to set the number of times to fire (1 in this example).::

    ep_blaster.fire(fire_type=blaster.WATER_FIRE, times=1)

- Release relevant resources as described in the `Release robot resources`_ section.

For the full process of controlling the firing of the blaster, refer to the :file:`examples/06_blaster/01_fire.py` sample program.

.. literalinclude:: ./../../../examples/06_blaster/01_fire.py
   :language: python
   :linenos:
   :lines: 17-

Example 2: Control the speed of the chassis
++++++++++++++++++++++++++++++++++++++++++++++++++

Controlling the speed of the chassis is a typical instant control practice. After a control command is issued, the robot immediately moves at the specified speed.

- First, initialize the robot object as described in the `Initialize the robot`_ section.

- The interface for controlling the chassis belongs to the `chassis` module. Therefore, first obtain the `chassis` object as described in the `Obtain module objects`_ section.
  This example uses method 1 to obtain module objects.::

    ep_chassis = ep_robot.chassis

- Use the `drive_speed()` method in the `chassis` object to control the speed of the chassis.
  The `x`, `y`, and `z` parameters of the method represent the forward, lateral, and rotational speeds respectively. In this example, the `x` forward speed is set to 0.5 m/s.
  The `timeout` parameter is used to specify a timeout period. If no speed control command is received after this period elapses, the SDK instructs the robot to stop.
  In this example, `timeout` is set to 5 seconds, and the speed is set to 0 after the robot moves at the specified speed for 3 seconds.::

    ep_chassis.drive_speed(x=0.5, y=0, z=0, timeout=5)
    time.sleep(3)
    ep_chassis.drive_speed(x=0, y=0, z=0, timeout=5)

- Release relevant resources as described in the `Release robot resources`_ section.

For the full process of controlling the speed of the chassis, refer to the :file:`examples/02_chassis/03_speed.py` sample program.
In this program, the speed of the robot changes every time the robot moves at the specified speed for three seconds.

.. literalinclude:: ./../../../examples/02_chassis/03_speed.py
   :language: python
   :linenos:
   :lines: 17-

Task action control
**********************

Task actions are actions that take a period of time to complete, such as controlling the chassis to move forward by 1 m.
In this case, the chassis needs to perform this action for a period of time to reach the specified position. When you use the SDK to control task actions,
the SDK sends the task to the robot. After the robot receives the task, it will choose to execute or reject the task (the robot may not be able to execute the task instantly) and notify the SDK.
If the robot chooses to execute the task, the SDK will be notified again when the task is completed. When using the task action control interface, pay attention to the following two items:

- The return value of the task action interface is the `action` object, which provides the `wait_for_completed(timeout)` method.
  You can specify the timeout period of the action by using the `timeout` parameter. When calling the `wait_for_completed(timeout)` method,
  the program will be blocked at the statement until the action is completed or the execution times out.

- A single module can perform only one action at a time, so tasks of the same module are mutually exclusive. Different modules are independent of each other, so their actions can be performed simultaneously.
  For example, if you do not call the `wait_for_completed()` method immediately after using the task action control interface, you can control the chassis to move to the specified position while controlling the gimbal to rotate to the specified angle.
  However, you cannot send another task action to control the gimbal until the previous task action for the gimbal is completed.

.. tip:: If you do not call the `wait_for_completed()` method immediately after using the task action control interface, be sure to control the logic in the program
  to avoid sending other task action commands that are mutually exclusive with the ongoing task.

Next, this document will explain how to control the chassis to move a specified distance to show you how to use this interface.


Example 1: Control the chassis to move a specified distance
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Controlling the chassis to move a specified distance is a task action control scenario.

- First, initialize the robot object as described in the `Initialize the robot`_ section.

- The interface for controlling the chassis belongs to the `chassis` module. Therefore, first obtain the `chassis` object as described in the `Obtain module objects`_ section.
  In this example, you also need to obtain the `led` module because you will also control the armored light.
  This example uses method 1 to obtain module objects.::

    ep_chassis = ep_robot.chassis
    ep_led = ep_robot.led

- In this example, in order to demonstrate the characteristics of task actions, the armored light effect will be configured after you control the movement of the chassis.
  Use the `move()` method in the `chassis` object to control the relative movement of the chassis.
  The `x` and `y` parameters of the method represent the movement distance of the x-axis and that of the y-axis, respectively. The `z` parameter indicates the rotation speed of the z-axis.
  In this example, the movement distance of the x-axis is set to 0.5 m, and the `y` and `z` parameters are set to 0.
  You can use the `xy_speed` parameter to specify the movement speed along the x- and y-axes, and use the `z_speed` parameter to specify the rotation speed of the z-axis.
  In this example, the movement speeds of the x- and y-axes are both set to 0.7 m/s, and the rotation speed of the z-axis is set to 0.
  To set the armored light effect, refer to `Example 2: Configure the armored light of the robot`_. Next, we will use three methods to control the task actions for chassis movement.:

  - Method 1: After performing the task action, call the `wait_for_completed()` method immediately.::

     ep_chassis.move(x=x_val, y=0, z=0, xy_speed=0.7).wait_for_completed()
     ep_led.set_led(comp=led.COMP_ALL, r=255, g=0, b=0, effect=led.EFFECT_ON)

  - Method 2: Call the `wait_for_completed()` method after executing other commands.::

     chassis_action = ep_chassis.move(x=x_val, y=0, z=0, xy_speed=0.7)
     ep_led.set_led(comp=led.COMP_ALL, r=255, g=0, b=0, effect=led.EFFECT_ON)
     chassis_action.wait_for_completed()

  - Method 3: Do not use the `wait_for_completed()` method, but use delay to ensure the completion of the action.::

     ep_chassis.move(x=x_val, y=0, z=0, xy_speed=0.7)
     ep_led.set_led(comp=led.COMP_ALL, r=255, g=0, b=0, effect=led.EFFECT_ON)
     time.sleep(10)

  The three calling mechanisms of the task action interface correspond to different behaviors of the robot. In *method 1*, the robot moves to the specified position and then sets the armored light to solid red.
  In *method 2* and *method 3*, the armored light will be solid red during the movement.

.. tip:: We recommend that you use *method 1* and *method 2*, because it is less risky to call `wait_for_completed()` at an appropriate time.

- Release relevant resources as described in the `Release robot resources`_ section.

For the full process of controlling the chassis to move a specified distance, refer to the :file:`examples/02_chassis/01_move.py` sample program.

.. literalinclude:: ./../../../examples/02_chassis/01_move.py
   :language: python
   :linenos:
   :lines: 17-


Use the multimedia interface
______________________________________

The multimedia interface is mainly used to obtain video streams and audio streams. The following two examples demonstrate how to use this interface.

Example 1: Obtain video streams
************************************

Obtaining video streams collected by the robot is very useful for implementing certain practical scenarios. The process of obtaining video streams through the SDK is as follows.

- First, initialize the robot object as described in the `Initialize the robot`_ section.
  You also need to import the `camera` module because the definition of the `camera` module will be used in the example.::

    from robomaster import camera

- The interface for obtaining video streams belongs to the `camera` module. Therefore, first obtain the `camera` object as described in the `Obtain module objects`_ section.
  In this example, the method described in the `Obtain module objects`_ section is used to obtain module objects.::

    ep_camera = ep_robot.camera

- The `start_video_stream` method of the `camera` module has two parameters. The `display` parameter specifies whether to display the obtained video streams.
  The `resolution` parameter specifies the size of the video. This example describes two ways to obtain the video stream.

  - Method 1: Obtain the video stream and play it directly for 10 seconds.::

        ep_camera.start_video_stream(display=True, resolution=camera.STREAM_360P)
        time.sleep(10)
        ep_camera.stop_video_stream()

  - Method 2: Obtain the video stream and display 200 image frames by using the method provided by cv2.::

        ep_camera.start_video_stream(display=False)
        for i in range(0, 200):
            img = ep_camera.read_cv2_image()
            cv2.imshow("Robot", img)
            cv2.waitKey(1)
        cv2.destroyAllWindows()
        ep_camera.stop_video_stream()

  Method 1 directly uses the `start_video_stream()` method of the `camera` object to obtain and play the video stream collected by the robot through the SDK.
  Method 2 obtains the video stream by using the `start_video_stream` method of the `camera` object and then plays the obtained video stream by using `cv2.inshow()`.

- Release relevant resources as described in the `Release robot resources`_ section.

For the full process of obtaining and then directly displaying the video scream, refer to the :file:`examples/04_camera/01_video_with_display.py` sample program.

.. literalinclude:: ./../../../examples/04_camera/01_video_with_display.py
   :language: python
   :linenos:
   :lines: 17-

For the full process of obtaining the video stream and then displaying images by using the method provided by cv2, refer to the :file:`examples/04_camera/03_video_without_display.py` sample program.

.. literalinclude:: ./../../../examples/04_camera/03_video_without_display.py
   :language: python
   :linenos:
   :lines: 17-

Example 2: Obtain the audio stream
*****************************************

This example shows how to obtain the audio stream collected by the robot through the SDK, and then locally save the obtained audio stream as a `wav` file.

- First, initialize the robot object as described in the `Initialize the robot`_ section.

- The interface for obtaining video streams belongs to the `camera` module. Therefore, first obtain the `camera` object as described in the `Obtain module objects`_ section.
  In this example, the method described in the `Obtain module objects`_ section is used to obtain module objects.::

    ep_camera = ep_robot.camera

- Save the obtained audio stream locally by calling the `record_audio()` method of the `camera` module.
  The `save_file` parameter of the method specifies the name of the saved file, the `seconds` parameter specifies the duration of the collected audio stream,
  and the `sample_rate` parameter specifies the collection frequency.::

    ep_camera.record_audio(save_file="output.wav", seconds=5, sample_rate=16000)

- Release relevant resources as described in the `Release robot resources`_ section.

For the full process of obtaining and then locally saving the audio stream, refer to the :file:`examples/04_camera/05_record_audio.py` sample program.

.. literalinclude:: ./../../../examples/04_camera/05_record_audio.py
   :language: python
   :linenos:
   :lines: 17-
