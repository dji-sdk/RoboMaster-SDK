==================
Protocol Content
==================

*************************
SDK mode control
*************************

^^^^^^^^^^^^^^^^^^^^^^^^^
Enter SDK mode
^^^^^^^^^^^^^^^^^^^^^^^^^

IN：**command**

    - Description
        - Control the robot to enter SDK mode
        - Only after the robot successfully enters SDK mode can it respond to other control commands


^^^^^^^^^^^^^^^^^^^^^^^^^
Exit SDK mode
^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **quit**

    -Description
        - Control the robot to exit SDK mode and reset all settings
        - In Wi-Fi/USB connection mode, when the connection is broken, the robot exits SDK mode automatically

*************************
Robot control
*************************

^^^^^^^^^^^^^^^^^^^^^^^^^
Robot motion mode control
^^^^^^^^^^^^^^^^^^^^^^^^^

IN：**robot mode <mode>**
  
    - Description
        - Set the robot motion mode
    - Parameters
        - *mode* (:data:`mode_enum`): Robot motion mode
    - Example
        - *robot mode chassis_lead* : Set the robot motion mode to "Chassis lead mode"

.. note:: Robot motion mode

    The robot motion mode describes the interaction and interplay between the platform and the chassis, and each robot mode corresponds to a specific relationship.

    There are three modes of robot motion:

    1. Chassis lead mode: In this mode, the yaw axis of the gimbal goes into a state in which it continuously follows the movement of the yaw axis of the chassis. The gimbal does not respond to the yaw axis control parts in any control commands. The affected commands include `gimbal motion speed control`_, `gimbal relative position control`_, and `gimbal absolute position control`_
    2. Gimbal lead mode: In this mode, the yaw axis of the chassis goes into a state in which it continuously follows the movement of the yaw axis of the gimbal. The chassis does not respond to the yaw axis control parts in any control commands. The affected commands include `chassis motion speed control`_, `chassis wheel speed control`_, and `chassis relative position control`_
    3. Free mode: In this mode, the yaw axis of the gimbal and the yaw axis of the chassis do not affect each other's movement.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Obtaining the robot's motion mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **robot mode ?**

    - Description
        - Query the robot's current motion mode
    - Return value
        - *mode* (:data:`mode_enum`): Robot motion mode
    - Example
        - IN：*robot mode ?*: Query the robot's current motion mode
        - OUT: *chassis_lead*: The current motion mode returned by the robot is *chassis lead mode*

.. warning:: Obtain the *?* from commands

   Note: There is a space between *?* in the query command and the foregoing command section

*************************
Chassis control
*************************

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Chassis motion speed control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **chassis speed x <speed_x>  y <speed_y> z <speed_z>**

    - Description
        - Control the chassis motion speed
    - Parameters
        - *speed_x* (float:[-3.5,3.5]):x-axial velocity in m/s
        - *speed_y* (float:[-3.5,3.5]):y-axial velocity in m/s
        - *speed_z* (float:[-600,600]): z-axial rotation velocity in °/s
    - Example
        - *chassis speed x 0.1 y 0.1 z 1* : The chassis's x-axial velocity is 0.1 m/s, the y-axial velocity is 0.1 m/s, and the z-axial velocity is 1°/s 


^^^^^^^^^^^^^^^^^^^^^^^^^^^
Chassis wheel speed control
^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **chassis wheel w1 <speed_w1> w2 <speed_w2> w3 <speed_w3> w4 <speed_w4>**
    
    - Description
        - Control the speed of the four wheels
    - Parameters
        - *speed_w1* (int:[-1000, 1000]): Right front Mecanum wheel speed in rpm
        - *speed_w2* (int:[-1000, 1000]): Left front Mecanum wheel speed in rpm
        - *speed_w3* (int:[-1000, 1000]): Right rear Mecanum wheel speed in rpm
        - *speed_w4* (int:[-1000, 1000]): Left rear Mecanum wheel speed in rpm
    - Example
        - *chassis wheel w2 100 w1 12 w3 20 w4 11* : The speed of the left front Mecanum wheel of the chassis is 100 rpm, the speed of the right front Mecanum wheel is 12 rpm, the speed of the right rear Mecanum wheel is 20 rpm, and the speed of the left rear Mecanum wheel is 11 rpm

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Chassis relative position control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **chassis move { [x <distance_x>] | [y <distance_y>] | [z <degree_z>] } [vxy <speed_xy>] [vz <speed_z>]**
    
    - Description
        - Control the chassis to move to a specified position. The origin of the coordinate axis is the current position
    - Parameters
        - *distance_x* (int:[-5, 5]): x-axial distance in m
        - *distance_y* (int:[-5, 5]): y-axial distance in m
        - *degree_z* (int:[-1800, 1800]):z-axial distance in °
        - *speed_xy* (int:(0, 3.5]): xy-axial distance in m/s
        - *speed_z* (int:(0, 600]): z-axial distance in m/s
    - Example
        - *chassiss move x 0.1 y 0.2* ：Using the current position as the origin of coordinates, move 0.1 m towards the x axis and 0.2 m towards the y axis

^^^^^^^^^^^^^^^^^^^^^^^^^^^
Obtaining the chassis speed
^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **chassis speed ?**

    - Description
        - Obtain the chassis speed information
    - Return value
        - *<x> <y> <z> <w1> <w2> <w3> <w4>* ：x axial velocity (m/s), y axial velocity (m/s), z axial rotation velocity (°/s), w1 right front Mecanum wheel speed (rpm), w2 left front Mecanum wheel speed (rpm), w3 right rear Mecanum wheel speed (rpm), w4 left rear Mecanum wheel speed (rpm)
    - Example
        - IN: *chassis speed ?* : Obtain the motion speed information of the chassis
        - OUT: *1 2 30 100 150 200 250* : The current x-axial velocity of the chassis is 1 m/s, y-axial velocity is 2 m/s, z-axial rotation velocity is 20°/s, the speed of wheel 1 is 100 rpm, the speed of wheel 2 is 100 rpm, the speed of wheel 3 is 100 rpm, and the speed of wheel 4 is 100 rpm


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Obtaining the chassis position
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **chassis position ?**

    - Description
        - Obtain the chassis position information
    - Return value
        - *<x> <y> <z>* ：x-axis position (m), y-axis position (m), yaw angle (°)
    - Example
        - IN: *chassis position ?* ：Obtain the chassis position information
        - OUT: *1 1.5 20* ：The current position of the chassis is 1 m along the x-axis, 1.5 m along the y-axis, and 20° from the position at the time of powering up

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Obtaining the chassis attitude
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **chasssis attitude ?**

    - Description
        - Obtain chassis attitude information
    - Return value
        - *<pitch> <roll> <yaw>* ：pitch axis angle (°), roll axis angle (°), yaw axis angle (°)
    - Example
        - *chassis attitude ?* ：Query chassis attitude information

^^^^^^^^^^^^^^^^^^^^^^^^^^^
Obtaining the chassis state
^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **chassis status ?**

    - Description 
        - Obtain chassis state information
    - Return value
        - *<static> <uphill> <downhill> <on_slope> <pick_up> <slip> <impact_x> <impact_y> <impact_z> <roll_over> <hill_static>* 
            - *static*：Whether it is still
            - *uphill*：Whether it is moving uphill
            - *downhill*：Whether it is moving downhill
            - *on_slope*：Whether it is on a slope
            - *pick_up*：Whether it is picked up
            - *slip*：Whether it is gliding
            - *impact_x*：Whether the x-axis senses impact
            - *impact_y*：Whether the y-axis senses impact
            - *impact_z*：Whether the z-axis senses impact
            - *roll_over*：Whether it has rolled over
            - *hill_static*：Whether is standing still on a slope
    - Example
        - IN: *chassis status ?* ：Query the status of the chassis
        - OUT: *0 1 0 0 0 0 0 0 0 0 0* : Chassis is currently in moving uphill

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Chassis information push control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN：**chassis push {[position <switch> pfreq <freq>][attitude <switch> afreq <freq>] | [status <switch> sfreq <switch>] [afreq <freq_all>]}**

    - Description
        - Enable/disable the information push of corresponding attributes in the chassis
        - Frequency setting
            - Each individual function supports a separate frequency setting, such as:
                - *chassis push position on pfreq 1 attitude on* : Enable the position and attitude push. The position push frequency is 1 Hz, and the default setting of 5 Hz is used as the attitude push frequency
            - Unified frequency setting is supported for all functions of the current module, such as:
                - chassis push freq 10 #The push frequency is unified to 10 Hz for the chassis
                - chassis push position pfreq 1 freq 5 #If there is a freq parameter, pfreq is ignored
            - Supported frequencies: 1, 5, 10, 20, 30, and 50
        - For push data formats, refer to `Chassis Push Information Data`_
    - Parameters
        - *switch* (:data:`switch_enum`) ：When *on* is used in the parameter here, the push of corresponding attributes is enabled; when *off* is used here, the push of corresponding attributes is disabled
        - *freq* (int:(1,5,10,20,30,50)) ：Push frequency of corresponding attributes
        - *freq_all* (int:(1,5,10,20,30,50)) : Push frequency of all relevant push information of the whole chassis
    - Example
        - *chassis push attitude on* : Enable the push of chassis attitude information
        - *chassis push attitude on status on* ：Enable the push of chassis attitude and status information
        - *chassis push attitude on afreq 1 status on sfreq 5* ：Enable the push of chassis attitude information, the frequency of which is once per second, and, at the same time, enable the push of chassis status information, the frequency of which is five times per second
        - *chassis push freq 10* ：The push frequency of all chassis information is ten times per second

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Chassis push information data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

OUT: **chassis push <attr> <data>**

    - Description
        - After the user enables chassis information push, the robot pushes the corresponding information to the user at the set frequency
    - Parameters
        - *attr* (:data:`chassis_push_attr_enum`) : The name of the subscribed attribute
        - *data* : The data of the subscribed attribute
            - When *attr* is the **position**, the content of the *data* is *<x> <y>*
            - When *attr* is the **attitude**, the content of the *data* is *<pitch> <roll> <yaw>*
            - When *attr* is the **status**, the content of the *data* is *<static> <uphill> <downhill> <on_slope> <pick_up> <slip> <impact_x> <impact_y> <impact_z> <roll_over> <hill_static>*
    - Example
        - *chassis push attitude 0.1 1 3* ：The pitch, roll, and yaw attitude information of the current chassis are 0.1, 1, and 3, respectively

*************************
Gimbal control
*************************

^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Gimbal motion speed control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **gimbal speed p <speed> y <speed>**

    - Description
        - Control the gimbal motion speed
    - Parameters
        - *p* (float:[-450, 450]) ：pitch axis velocity in °/s
        - *y* (float:[-450, 450]) ：yaw axis velocity in °/s
    - Example
        - *gimbal speed p 1 y 1* ：The pitch axis velocity of the gimbal is 1°/s, and the yaw axis velocity is 1°/s

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Gimbal relative position control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **gimbal move { [p <degree>] [y <degree>] } [vp <speed>] [vy <speed>]**

    - Description
        - Control the gimbal to move to a specified position. The origin of the coordinate axis is the current position
    - Parameters 
        - *p* (float:[-55, 55]) ：pitch axis angle in °
        - *y* (float:[-55, 55]) ：yaw axis angle in °
        - *vp* (float:[0, 540]) ：pitch axis velocity in °/s
        - *vy* (float:[0, 540]) ：yaw axis velocity in °/s
    - Example
        - *gimbal move p 10* ：With the current position as the coordinate reference, control the gimbal to move to where the pitch axis angle is 10°

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Gimbal absolute position control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **gimbal moveto { [p <degree>] [y <degree>] } [vp <speed>] [vy <speed>]**

    - Description
        - Control the gimbal to move to a specified position. The origin of the coordinate axis is power-up position
    - Parameters
        - *p* (int:[-25, 30]) ：pitch axis angle (°)
        - *y* (int:[-250, 250]) ：yaw axis angle (°)
        - *vp* (int:[0, 540]) ：pitch axis velocity (°/s)
        - *vy* (int:[0, 540]) ：yaw axis velocity (°/s)
    - Example
        - *giimbal moveto p 10 y -20 vp 0.1* ：Taking the power-up position of the robot as the coordinate reference, control the gimbal to move to where the pitch axis angle is 10° and the yaw axis angle is -20°. As it moves, specify the pitch axis velocity as 0.1°/s

^^^^^^^^^^^^^^^^^^^^^^^^^
Gimbal sleep control
^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **gimbal suspend**

    - Description
        - Control the gimbal to sleep
    - Example
        - *gimbal suspend* ：Put the gimbal into sleep state

^^^^^^^^^^^^^^^^^^^^^^^^^
Gimbal recovery control
^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **gimbal resume**

    - Description
        - Control the gimbal to recover from sleep state
    - Parameters
        - *None*
    - Example
        - *gimbal resume* ：Take the gimbal out of sleep state

.. warning:: Sleep state
    When the gimbal goes into sleep state, the two-axis motor of the gimbal releases the control force, and the gimbal does not respond to any control command as a whole.

    To release the gimbal from sleep state, see `Gimbal recovery control`_

^^^^^^^^^^^^^^^^^^^^^^^^^
Gimbal recenter control
^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **gimbal recenter**

    - Description
        - Recenter the gimbal
    - Example
        - *gimbal recenter* ：Control the gimbal to return to the center

^^^^^^^^^^^^^^^^^^^^^^^^^
Obtaining gimbal attitude
^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **gimbal attitude ?**

    - Description
        - Obtain gimbal attitude information
    - Return values
        - *<pitch> <yaw>* ：Pitch axis angle (°), yaw axis angle (°)
    - Example
        - IN：*gimbal attitude ?* ：Query gimbal angle information
        - OUT: *-10 20* ：The current pitch axis angle of the gimbal is -10°, and the yaw axis angle is 20°

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Gimbal information push control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **gimbal push <attr> <switch> [afreq <freq_all>]**

    - Description
        - Enable/disable the information push of corresponding attributes in the gimbal
        - For push data formats, refer to `Gimbal push information data`_
    - Parameters
        - *attr* (:data:`gimbal_push_attr_enum`) : The name of the subscribed attribute
        - *switch* (:data:`switch_enum`) ：When *on* is used in the parameter here, the push of corresponding attributes is enabled; when *off* is used here, the push of corresponding attributes is disabled
        - *freq_all* : Push frequency of all relevant push information of the gimbal
    - Example
        - *gimbal push attitude on* ：Enable the push of gimbal information

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Gimbal push information data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

OUT: **gimabal push <attr> <data>**

    - Description
        - After the user enables gimbal information push, the robot pushes the corresponding information to the user at the set frequency
    - Parameters
        - *attr* (:data:`gimbal_push_attr_enum`) : The name of the subscribed attribute
        - *data*: The data of the subscribed attribute
            - When *attr* is the **attitude**, the content of the *data* is *<pitch> <yaw>*
    - Example
        - *gimbal push attitude 20 10* ：The pitch angle of the current gimbal is 20°, and the yaw angle is 10°

*************************
Blaster control
*************************

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Blaster single emittance control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN：**blaster bead <num>**

    - Description
        - Set the blaster single emittance
    - Parameters
        - *num* (int:[1,5]) ：Emittance
    - Example
        - *blaster bead 2* : Control the blaster to emit two at a time

^^^^^^^^^^^^^^^^^^^^^^^^^
Blaster emission control
^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **blaster fire**

    - Description
        - Control the water gun to fire once
    - Example
        - *blaster fire* ：Control the water gun to fire once

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Obtaining blaster single emittance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **blaster bead ?**

    - Description
        - Obtain the number of water bombs fired by the water gun at a single time
    - Return values
        - *<num>* ：Number of water bombs fired by the water gun at a single time
    - Example
        - IN: *blaster bead ?* ：Query the number of water bombs fired by the water gun at a single time
        - OUT: *3* ：At present, the number of water bombs fired by the water gun at a single time is 3

*************************
Armor plate control
*************************

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Armor plate sensitivity control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **armor sensitivity <value>**
    
    - Description
        - Set the strike detection sensitivity of the armor plate
    - Parameters
        - *value* (int:[1,10]) ：Armor plate sensitivity. The greater the value, the easier a strike is detected. The default sensitivity value is 5
    - Example
        - *armor sensitivity 1* ：Set the strike detection sensitivity of the armor plate to 1

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Obtaining armor plate sensitivity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **armor sensitivity ?**

    - Description
        - Obtain the strike detection sensitivity of the armor plate
    - Parameters
        - *<value>* ：Armor plate sensitivity
    - Example
        - IN: *armor sensitivity ?* ：Query the strike detection sensitivity of the armor plate
        - OUT: *5* ：Query the strike detection sensitivity of the armor plate

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Armor plate event reporting control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **armor event <attr> <switch>**

    - Description
        - Control the armor plate detection event report
        - For event data formats, please refer to `Armor plate event reporting data`_
    - Parameters
        - *attr* (:data:`armor_event_attr_enum`) : Event attribute name
        - *switch* (:data:`switch_enum`) : Event attribute control switch
    - Example
        - *armor event hit on* ：Enable the armor plate detection event push

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Armor plate event reporting data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

OUT: **armor event hit <index> <type>**

    - Description
        - This message can be received from the event push port when an armor plate hit event occurs
    - Parameters
        - *index* (int:[1, 6]) ：Armor plate ID of the current hit event
            - ``1``
            - ``2``
            - ``3``
            - ``4``
            - ``5``
            - ``6``
        - *type* (int:[0, 2]) ：Types of current hit events
            - ``0`` water bomb attack
            - ``1`` impact
            - ``2`` hand knock
    - Example
        - *armor event hit 1 0* ：Water gun attack detected on armor plate 1

*************************
Sound recognition control
*************************

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Sound recognition event reporting control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **sound event <attr> <switch>**

    - Description
        - Sound recognition time reporting control. Once enabled, related events will be reported
        - For event reporting data formats, refer to `Sound recognition event reporting data`_
    - Parameters
        - *attr* (:data:`sound_event_attr_enum`) : Event attribute name
        - *switch* (:data:`switch_enum`) : Event attribute control switch
    - Example
        - *sound event applause on* ：Enable sound (applause) recognition

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Sound recognition event reporting data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

OUT: **sound event <attr> <data>**

    - Description
        - When a specific sound event occurs, this data can be received from the event push port
        - To enable the event, please refer to `Sound recognition event reporting control`_
    - Parameters
        - *attr* (:data:`sound_event_attr_enum`):  Event attribute name
        - *data* ：Event attribute data
            - When *attr* is ``applause``, the *data* is *<count>*, which indicates the number of applauses in a short time
    - Example
        - *sound event applause 2* ：Recognize 2 claps in a short time

*************************
PWM control
*************************

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PWM output duty cycle control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **pwm value <port_mask> <value>**

    - Description
        - PWM output duty cycle setting
    - Parameters
        - *port_mask* (hex:0-0xffff) ：PWM expansion port mask combination. The corresponding mask of output port X is **1 << (X-1)**
        - *value* (float:0-100) ：PWM output duty cycle. The default output is 12.5
    - Example
        - *pwm value 1 50* : Control the duty cycle of PWM port 1 to 50%

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PWM output frequency control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **pwm freq <port_mask> <value>**

    - Description
        - PWM output frequency control
    - Parameters
        - *port_mask* (hex:0-0xffff) ：PWM expansion port mask combination. The corresponding mask of output port X is **1 << (X-1)**
        - *value* (int:XXX) ：PWM output frequency value
    - Example
        - *pwm freq 1 1000* : Control the frequency of PWM port 1 to 1,000 Hz

****************************
Sensor adaptor board control
****************************

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Obtaining the ADC value of the sensor adaptor board
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **sensor_adapter adc id <adapter_id> port <port_num> ?**

    - Description
        - Obtain the ADC value of the sensor adaptor board
    - Parameters
        - *adapter_id* (int:[1, 6]) ：Adaptor board ID
        - *port_num* (int:[1, 2]) ：Port No.
    - Return values
        - *adc_value* ：Measure the voltage value of the specified port on the corresponding adaptor board. The voltage has a value range of [0V, 3, 3V] 
    - Example
        - IN: *sensor_adapter adc id 1 port 1 ?* : Query the ADC value of port 1 on adaptor board 1
        - OUT: *1.1* ：The ADC value of the port currently queried is 1.1

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Obtaining the IO value of the sensor adaptor board
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **sensor_adapter io_level id <adapter_id> port <port_num> ?**

    - Description
        - Obtain the logic level of the IO port of the sensor adaptor board
    - Parameters
        - *adapter_id* (int:[1, 6]) ：Adaptor board ID
        - *port_num* (int:[1, 2]) ：Port No.
    - Return values
        - *io_level_value* ：Measure the logic level value of the specified port on the corresponding adaptor board. The value is 0 or 1
    - Example
        - IN: *sensor_adapter io_level id 1 port 1 ?* ：Query the IO logic level of port 1 on adaptor board 1
        - OUT: *1* ：The IO value of the currently queried port is 1 

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Obtaining the level jump time value of the IO pin of the sensor adaptor board
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **sensor_adapter pulse_period id <adapter_id> port <port_num>**

    - Description
        - Obtain the level jump duration of the IO port of the sensor adaptor board
    - Parameters
        - *adapter_id* (int:[1, 6])：Adaptor board ID
        - *port_num* (int:[1, 2])：Port No.
    - Return values
        - *pulse_period_value*: The value of the level jump duration of the specified port on the corresponding adaptor board, in ms
    - Example
        - *sensor_adapter pulse_period id 1 port 1* ：Query the level jump duration of port 1 on adaptor board 1

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Sensor adaptor board event reporting control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **sensor_adapter event io_level <switch>**

    - Description
        - Enable/disable the level transition event push of the sensor adaptor board. Once enabled, a message will be pushed when the level transition occurs on the IO. See [Level Transition Event Push of the Sensor Adaptor Board] (#sensor adaptor board level transition push) in the next chapter  
    - Parameters
        - *switch* (:data:`switch_enum`)：Control switch for level transition event reporting
    - Example
        - *sensor_adapter event io_level on* ：Enable the level transition event push for the sensor adaptor board

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Sensor adaptor board event reporting data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

OUT: *sensor_adapter event io_level (<id>, <port_num>, <io_level>)*

    - Description
        - Push a message when the level of the sensor adaptor board changes. You can receive this message from the event push port
        - Enabling the level transition push of the sensor adaptor board is required. See `Sensor adaptor board event reporting control`_
    - Parameters
        - *id*：Sensor adaptor board ID
        - *port_num*：IO ID
        - *io_level*：Current logic level value
    - Example
        - *sensor_adapter event io_level (1, 1, 0)* ：At present, the logic level of IO 1 of adaptor board 1 jumps to 0

*************************
TOF control
*************************

^^^^^^^^^^^^^^^^^^^^^^^^^
TOF switch control
^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **ir_distance_sensor measure <switch>**

    - Description
        - Turn all infrared sensor switches on/off
    - Parameters
        - *switch* (:data:`switch_enum`)：Infrared sensor switch
    - Example
        - *ir_distance_sensor meaure on* ：Turn on all TOFs

^^^^^^^^^^^^^^^^^^^^^^^^^^
Obtaining the TOF distance
^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **ir_distance_sensor distance <id> ?**

    - Description
        - Obtain the distance measured by the TOF with the specified ID
    - Parameters
        - *id* (int:[1, 4])：Infrared sensor ID
    - Return values
        - *distance_value*：Distance value measured by the TOF with the specified ID, in mm
    - Example
        - IN: *ir_distance_sensor distance 1* ：Query the distance value measured by TOF 1
        - OUT: *1000* ：The distance value of the currently queried TOF is 1,000 mm

*************************
Servo control
*************************

^^^^^^^^^^^^^^^^^^^^^^^^^
Servo angle control
^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **servo angle id <servo_id> angle <angle_value>**

    - Description
        - Set the servo angle
    - Parameters
        - *servo_id* (int:[1, 3])：Servo ID
        - *angle_value* (float:[-180, 180])：Specified angle in °
    - Example
        - *servo angle id 1 angle 20* ：Control the angle of servo 1 to 20°

^^^^^^^^^^^^^^^^^^^^^^^^^
Servo speed control
^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **servo speed id <servo_id> speed <speed_value>**

    - Description
        - Set the speed of the specified servo
    - Parameters
        - *servo_id* (int:[1, 3])：Servo ID
        - *speed_value* (float:[-1800, 1800])：Set speed value in °/s 
    - Example
        - *servo speed id 1 speed 20* ：The set speed of servo 1 is 10°/s

^^^^^^^^^^^^^^^^^^^^^^^^^
Servo stop control
^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **servo stop**

    - Description
        - Stop the servo
    - Example
        - *servo stop* ：Control the servo to stop moving

^^^^^^^^^^^^^^^^^^^^^^^^^
Servo angle query
^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **servo angle id <servo_id> ?**

    - Description
        - Obtain the angle of the specified servo
    - Parameters
        - *servo_id* (int:[1, 3])：Servo ID
    - Return values
        - *angle_value*  : Specify the angle value of the servo
    - Example
        - IN: *servo angle id 1 ?* ：Obtain the angle value of servo 1
        - OUT: *30* ：The angle value of the currently queried servo is 30°

*************************
Robotic arm control
*************************

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Robotic arm relative position motion control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **robotic_arm move x <x_dist> y <y_dist>**

    - Description
        - Control the robotic arm to move a certain distance. The current position is the origin of coordinates
    - Parameters
        - *x_dist* (float:[])：x-axis movement distance in cm
        - *y_dist* (float:[]) ：y-axis movement distance in cm
    - Example
        - *robotic_arm move x 5 y 5* ：Control the robotic arm to move 5 cm along the x-axis and 5 cm along the y-axis

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Robotic arm absolute position motion control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **robotic_arm moveto x <x_pos> y <y_pos>**

    - Description
        - Control the robotic arm to move to a certain position. The robot power-up position is the origin of coordinates
    - Parameters
        - *x_pos* (float:[])：x-axis move-to coordinate in cm
        - *y_pos* (float:[])：y-axis move-to coordinate in cm
    - Example
        - *robotic_arm moveto x 5 y 5* ：Control the x-axis of the robotic arm to move to the coordinate position of 5 cm, and the y-axis to move to the coordinate position of 5 cm

^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Robotic arm recenter control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **robotic_arm recenter**

    - Description
        - Control the robotic arm to go back to the center
    - Parameters
        - *None*
    - Example
        - *robotic_arm recenter* ：Control the robotic arm to go back to the center

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Robotic arm movement stop control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **robotic_arm stop**

    - Description
        - Stop robotic arm movement
    - Parameters
        - *None*
    - Example
        - *robotic_arm stop* ：Stop robotic arm movement

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Robotic arm absolute position query
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **robotic_arm position ?**

    - Description
        - Obtain the position of the robotic arm
    - Parameters
        - *None*
    - Return values
        - *<x_pos> <y_pos>*: The position coordinates of the robotic arm
            - *x_pos*：x-axis coordinate in cm
            - *y_pos*：y-axis coordinate in cm
    - Example
        - IN: *robotic_arm position ?* ：Query the position of the robotic arm
        - OUT：*50 60* ：The distance between the position of the currently queried robotic arm and the calibration point is 50 cm in the x-axis direction and 60 cm in the y-axis direction

*************************
Gripper control
*************************

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Gripper opening motion control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **robotic_gripper open [leve <level_num>]**

    - Description
        - Open the gripper
    - Parameters
        - *level_num* (int:[1,4])：The force of the gripper opening. The value range is [1,4]
    - Example
        - *robotic_gripper open 1* ：Control the robotic arm to open with a force of 1

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Gripper closing motion control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **robotic_gripper close [leve <level_num>]**

    - Description
        - Close the gripper
    - Parameters
        - *level_num* (int:[1,4])：The force of the gripper closing. The value range is [1,4]
    - Example
        - *robotic_gripper close 1* ：Control the robotic arm to close with a force of 1

.. note:: Gripper control force

    **The gripper control force** describes the movement speed of the gripper during the movement and the maximum clamping force in the locked rotor state

    The greater the force, the faster the movement speed, and the greater the clamping force; vice versa.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Robotic arm relative position motion control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **robotic_gripper status ?**

    - Description
        - Obtain the opening and closing state of the gripper
    - Parameters
        - *None*
    - Return values
        - *status*  : Current opening and closing state of the gripper
            > ``0`` Gripper fully closed
            > ``1`` Gripper neither fully closed nor fully opened
            > ``2`` Gripper fully opened
    - Example
        - IN: *robotic_gripper status ?* ：Obtain the opening and closing state of the gripper
        - OUT: *2* ：The currently queried gripper is open

*************************
Video streaming control
*************************

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Video streaming enabling control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **stream on**

    - Description
        - Enable video streaming
        - Once enabled, the H.264 encoded bitstream data can be received from the video streaming port
    - Example
        - *stream on* ：Enable video streaming

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Video streaming disabling control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **stream off**

    - Description
        - Disable video streaming
        - Once video streaming is disabled, the H.264 encoded bitstream data stops being output
    - Example
        - *stream off* ：Disable video streaming

*************************
Audio streaming control
*************************

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Audio streaming enabling control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **audio on**

    - Description
        - Enable audio streaming
        - Once audio streaming is disabled, the Opus encoded audio streaming data can be received from the audio streaming port
    - Example
        - *audio on* ：Enable audio streaming

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Audio streaming disabling control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **audio off**

    - Description
        - Disable audio streaming
        - Once audio streaming is disabled, the Opus encoded audio stream data stops being output
    - Example
        - *audio off* ：Disable audio streaming

*************************
IP broadcasting
*************************

OUT: **robot ip <ip_addr>**

    - Description
        - When there is no connection with the robot, you can receive this message from the IP broadcast port. Once the connection is successful, the message stops broadcasting
        - The IP address of the current robot is provided. It is applicable to situations where the robot is in the same LAN with the robot, but the IP information of the robot is unknown
    - Parameters
        - *ip_addr* : The robot's current IP address
    - Example
        - *robot ip 192.168.1.102* : The robot's current IP address is 192.168.1.102
