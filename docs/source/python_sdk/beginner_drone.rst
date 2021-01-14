.. _beginngerDrone:

##################################################################
Getting Started with the RoboMaster SDK - Education-series Drones
##################################################################

Initialize the robot
_____________________

Before performing robot-related operations, you must initialize the robot object according to the specified configuration.

- First, import the `robot` module from the installed `robomaster` package.::

    from robomaster import robot

- Specify the local IP address of the SDK (if you want to specify it manually). In this example, the retrieved local IP address is `192.168.2.20`.
  (For example, in the Windows operating system, press the `Win+R` shortcut command and then enter `cmd` in the window that appears.
  Enter `ipconfig` in the window to view the IP address of the device.)
  To specify the IP address, run the following statement::

    robomaster.config.LOCAL_IP_STR = "192.168.2.20"

.. tip:: In most cases, the SDK can automatically obtain the correct local IP address, and you do not need to manually specify it. However, when the SDK runs on a device with multiple network cards,
  the automatically obtained IP address may not be the one used to connect to the robot. In this case, you need to manually specify the IP address.

- Create a `tl_drone` instance object of the `Drone` class. Here, `tl_drone` is a robot object.::

    tl_drone = robot.Drone()

- Initialize the robot object. Currently, no input parameters are required for the initialization of education-series drones.::

    tl_drone.initialize()

Now, the initialization of the robot is completed. Then, you can use the robot for information query, motion control, and multimedia use through related interfaces.
Later, this document will introduce the use of several types of interfaces.

Obtain module objects
_______________________

Some SDK interfaces belong to the `Drone` object itself so they can be directly called through the `Drone` object.
However, certain interfaces belong to other modules in the `Drone` object. For example, the interface for obtaining information about the drone battery is in the `led` module object,
and the interface for controlling the drone is in the `flight` module object. To use these interfaces, you must first obtain the corresponding objects.
The following uses the `flight` module object as an example to explain how to obtain these objects.

- First, initialize the robot object as described in the `Initialize the robot`_ section.

- You can obtain the `flight` object in two ways.

  - Method 1: Directly use the `.` operator to obtain the `flight` object from the `Drone()` object.::

        tl_flight = tl_drone.flight

  - Method 2: Use the `get_module()` method of the `Drone` object to obtain the specified object.::

        tl_flight = tl_drone.get_module("flight")

After obtaining the object, you can call the SDK interfaces contained in it through the object.


Release robot resources
_________________________

At the end of the program, you need to manually release the resources related to the robot object, including releasing the network address, ending the corresponding background thread, and releasing the corresponding address space.
The `Drone` object provides the `close()` method for releasing these resources, which can be used as follows.::

    tl_drone.close()

.. tip:: To avoid unexpected errors, be sure to call the `close()` method at the end of the program.

Use the query interface
______________________________

The query interface is the data acquisition interface, through which you can obtain the status of the robot and the status of sensors.
The following two examples of querying the SDK firmware version and querying the robot SN can help you understand the usage of this interface.

Example 1: Query the firmware SDK version number of the robot
****************************************************************

- First, initialize the robot object as described in the `Initialize the robot`_ section.

- Use the `get_sdk_version()` method of the `Drone` object. The return value of the method is the version number string of the robot SDK firmware.
  Print the obtained version number.::

    drone_version = tl_drone.get_sdk_version()
    print("Drone sdk version: {0}".format(drone_version))

- Release relevant resources as described in the `Release robot resources`_ section.

For the full process, refer to the :file:`/examples/12_drone/02_get_version.py` sample file.

.. literalinclude:: ./../../../examples/12_drone/02_get_version.py
   :language: python
   :linenos:
   :lines: 17-

Example 2: Obtain the SN of the robot
*****************************************

- First, initialize the robot object as described in the `Initialize the robot`_ section.

- Use the `get_sn()` method of the `Drone` object. The return value of the method is the SN string of the robot.
  Print the obtained SN.::

    SN = tl_drone.get_sn()
    print("drone sn: {0}".format(SN))

- Release relevant resources as described in the `Release robot resources`_ section.

For the full process, refer to the :file:`/examples/12_drone/03_get_sn.py` sample file.

.. literalinclude:: ./../../../examples/12_drone/03_get_sn.py
   :language: python
   :linenos:
   :lines: 17-

Use the setup interface
_______________________

The setup interface is used to configure the modules of the robot. This section uses the extended LED module as an example to explain how to use the setup interface.

.. tip:: Currently, configuring extended LED lights is only supported by Tello Talent devices.

Example 1: Configure the extended LED module of the robot
*************************************************************

The process of configuring the extended LED module of the robot through the SDK is as follows.

- First, initialize the robot object as described in the `Initialize the robot`_ section.

- You must obtain the `led` object first, because the armored light configuration interface of the robot belongs to the `led` module contained in the `Drone` object.
  Obtain the `led` object as described in the `Obtain module objects`_ section. In this example, method 1 is used to obtain module objects.::

    tl_led = tl_robot.led

- Use the `set_led()` method in the `led` object to configure the extended LED lighting effect of the robot.
  When using the `led` method, you can use the `r`, `g`, and `b` parameters to specify the LED color. In this example, the color is specified as red.::

    tl_led.set_led(r=255, g=0, b=0)

- Release relevant resources as described in the `Release robot resources`_ section.

For the full process of configuring the armored light, refer to the :file:`/examples/12_drone/20_led.py` sample program.
In this process, the for loop is used to implement 8 color changes of the LED light, each of which lasts for 0.5 seconds.

.. literalinclude:: ./../../../examples/12_drone/20_led.py
   :language: python
   :linenos:
   :lines: 17-


Use the action interface
_____________________________

The action interface is used to control the robot to perform certain specified actions. Based on the characteristics of actions,
the SDK provides two types of action interfaces: *instant action control* and *task action control*.
Due to their characteristic, drones must take off before they can be controlled.
Therefore, this document will first introduce the *task action control* interface. After you are familiar with the flight actions, we will introduce the usage of the *instant action control* interface.

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


Example 1: Control the drone to take off and fly back and forth
+++++++++++++++++++++++++++++++

In this example, you first need to control the drone to take off and then move it forward 50 cm.

- First, initialize the robot object as described in the `Initialize the robot`_ section.

- The flight control interface belongs to the `flight` module. Therefore, first obtain the `flight` object as described in the `Obtain module objects`_ section.
  In this example, you also need to obtain the `led` module because you will control the extended LED module as well.
  This example uses method 1 to obtain module objects.::

    tl_flight = tl_drone.flight
    tl_led = tl_drone.led

- Next, have the drone take off. During this process, call the `wait_for_completed()` method in the `action` object returned by the task action interface to block the program until takeoff is completed.::

    tl_flight.takeoff().wait_for_completed()

- Then, control the drone to move forward 50 cm. In this example, the extended LED lighting effect will be configured after the vehicle takes off to demonstrate the characteristics of task actions.
  Use the `forward()` method in the `flight` object to control the forward movement of the chassis. This method uses only one parameter (`distance`) to specify the flight distance.
  To configure the extended LED module, see `Example 1: Configure the extended LED module of the robot`_. Next, this document will explain how to use the task action interface in three ways.


  - Method 1: After performing the task action, call the `wait_for_completed()` method immediately.::

     tl_flight.forward(distance=50).wait_for_completed()
     tl_led.set_led(r=255, g=0, b=0)

  - Method 2: Call the `wait_for_completed()` method after executing other commands.::

     flight_action = tl_flight.forward(distance=50)
     tl_led.set_led(r=255, g=0, b=0)
     flight_action.wait_for_completed()

  - Method 3: Do not use the `wait_for_completed()` method, but use delay to ensure the completion of the action.::

     flight_action = tl_flight.forward(distance=50)
     tl_led.set_led(r=255, g=0, b=0)
     time.sleep(8)

  The calling mechanisms of the task action interface in the three methods correspond to different behaviors of the robot. In *method 1*, the robot moves forward to the specified position and then sets the LED color of the extended LED module to red.
  In *method 2* and *method 3*, the LED color of the extended LED module is set to red while the vehicle is moving forward.


.. note:: In *method 2* and *method 3*, be sure not to use other interfaces whose `ack` is `ok/error` during the flight. For information about the `ack` object of the robot, refer to "Tello SDK Instructions".


.. tip:: We recommend that you use *method 1* and *method 2*, because it is less risky to call `wait_for_completed()` at an appropriate time.


- Land the drone::

    tl_flight.land().wait_for_completed()

- Release relevant resources as described in the `Release robot resources`_ section.

For the full process of controlling the chassis to move forward and backward 50 cm, refer to the :file:`examples/12_drone/07_forward_backward.py` sample program.

.. literalinclude:: ./../../../examples/12_drone/07_forward_backward.py
   :language: python
   :linenos:
   :lines: 17-


Instant action control
****************************

Instant control actions are actions that are performed immediately after being configured. Such actions refer to actions that are "instantaneously" performed from an overall perspective.
Next, this document will explain how to control the remote control stick to help you understand this action interface.

Example 1: Control the remote control stick movement
++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Controlling the remote control stick movement is a typical instant control practice. After a control command is issued, the robot immediately flies at the specified speed and direction.

- First, initialize the robot object as described in the `Initialize the robot`_ section.

- The flight control interface belongs to the `flight` module. Therefore, first obtain the `flight` object as described in the `Obtain module objects`_ section.
  This example uses method 1 to obtain module objects.::

    tl_flight = tl_drone.flight

- Next, have the drone take off. During this process, call the `wait_for_completed()` method in the `action` object returned by the task action interface to block the program until takeoff is completed.::

    tl_flight.takeoff().wait_for_completed()

- Then, control the drone to move leftward at the specified speed for three seconds and then stop.
  Use the `rc()` method in the `flight` object to control the forward movement of the chassis. This is done by controlling the four speed parameters: roll, pitch, accelerate, and yaw. For details about these parameters, refer to the API documentation.
  In this example, set the value of the `a` roll parameter to 20 in order to move the drone leftward. Then, set all speed parameters to 0 after 3 seconds to stop the flight.::

    tl_flight.rc(a=20, b=0, c=0, d=0)
    time.sleep(4)

- Land the drone::

    tl_flight.land().wait_for_completed()

- Release relevant resources as described in the `Release robot resources`_ section.

For the full process of controlling the flight of the vehicle by controlling remote control stick movements, refer to the :file:`examples/12_drone/13_rc.py` sample program.

.. literalinclude:: ./../../../examples/12_drone/13_rc.py
   :language: python
   :linenos:
   :lines: 17-

Use the multimedia interface
______________________________________

The primary multimedia application of education-series drones is obtaining video streams.

Example 1: Obtain video streams
**********************************

Obtaining video streams collected by the robot is very useful for implementing certain practical scenarios. The process of obtaining video streams through the SDK is as follows.

- First, initialize the robot object as described in the `Initialize the robot`_ section.
  You also need to import the `camera` module because the definition of the `camera` module will be used in the example.::

    from robomaster import camera

- The interface for obtaining video streams belongs to the `camera` module. Therefore, first obtain the `camera` object as described in the `Obtain module objects`_ section.
  In this example, the method described in the `Obtain module objects`_ section is used to obtain module objects.::

    tl_camera= tl_robot.camera

- The `start_video_stream` method of the `camera` module has two parameters. The `display` parameter specifies whether to display the obtained video streams. The following example describes two video stream acquisition methods.

  - Method 1: Obtain the video stream and play it directly for 10 seconds.::

        tl_camera.start_video_stream(display=True)
        time.sleep(10)
        tl_camera.stop_video_stream()

  - Method 2: Obtain the video stream and display 200 image frames by using the method provided by cv2.::

        tl_camera.start_video_stream(display=False)
        for i in range(0, 200):
            img = tl_camera.read_cv2_image()
            cv2.imshow("Drone", img)
            cv2.waitKey(1)
        cv2.destroyAllWindows()
        tl_camera.stop_video_stream()

  Method 1 directly uses the `start_video_tream()` method of the `camera` object to obtain and play the video stream collected by the robot through the SDK.
  Method 2 obtains the video stream by using the `start_video_stream` method of the `camera` object and then plays the obtained video stream by using `cv2.inshow()`.

- Release relevant resources as described in the `Release robot resources`_ section.

For the full process of obtaining the video stream and then displaying images by using the method provided by cv2, refer to the :file:`examples/04_camera/01_video_with_display.py` sample program.

.. literalinclude:: ./../../../examples/12_drone/16_video_stream.py
   :language: python
   :linenos:
   :lines: 17-

