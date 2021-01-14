===================
Protocol Content
===================

*************************
SDK mode control
*************************

^^^^^^^^^^^^^^^^^^^^^^^^^
Enter SDK mode
^^^^^^^^^^^^^^^^^^^^^^^^^

IN：**command;**

    - Description
        - Instructs the robot to enter the SDK mode.
        - The robot will respond to other control commands only after it enters SDK mode.


^^^^^^^^^^^^^^^^^^^^^^^^^
Exit SDK mode.
^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **quit;**

    - Description
        - Instructs the robot to exit SDK mode and reset all settings.
        - In Wi-Fi/USB connection mode, the robot automatically exits SDK mode when the connection is disconnected.

*************************
Robot control
*************************

^^^^^^^^^^^^^^^^^^^^^^^^^
Robot movement mode control
^^^^^^^^^^^^^^^^^^^^^^^^^

IN：**robot mode <mode>**
  
    - Description
        - Sets the robot movement mode.
    - Parameters
        - *mode* (:data:`mode_enum`): The robot movement mode
    - Example
        - *robot mode chassis_lead;*: Set the robot movement mode to "gimbal follows chassis".

.. note:: Robot movement modes

    The robot movement mode describes the relationship and mutual movement between the gimbal and the chassis. Each robot mode corresponds to a specific interaction relationship.

    There are three robot movement modes:

    1. Gimbal follows chassis: In this mode, the yaw axis of the gimbal always follows the movement of the yaw axis of the chassis. In addition, the gimbal does not respond to the yaw axis control part of all control commands. The affected commands are `gimbal movement speed control`_, `gimbal relative position control`_, and `gimbal absolute position control`_.
    2. Chassis follows gimbal: In this mode, the yaw axis of the chassis always follows the movement of the yaw axis of the gimbal. In addition, the chassis does not respond to the yaw axis control part of all control commands. The affected commands are `chassis movement speed control`_, `chassis wheel speed control`_, and `chassis relative position control`_.
    3. Free: In this mode, the movement of the yaw axis of the gimbal does not affect the movement of the yaw axis of the chassis, and vice versa.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Obtain the robot movement mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **robot mode ?**

    - Description
        - Queries the current robot movement mode.
    - Return values
        - *mode* (:data:`mode_enum`): The robot movement mode
    - Example
        - IN: *robot mode ?;*: Query the current robot movement mode.
        - OUT: *chassis_lead;*: The robot returns the current movement mode, *gimbal follows chassis*.

.. warning:: *?* in the query command

    Note: There is a space between *?* in the query command and the prior part of the command.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Obtain the remaining battery capacity of the robot
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **robot battery ?**

    - Description
        - Queries the remaining battery level of the robot.
    - Return values
        - *battery_percentage* (int:[1-100]): The remaining battery level of the robot. This value is 100 when the robot is fully charged.
    - Example
        - IN: *robot battery ?;*: Query the remaining battery level of the robot.
        - OUT: *20;* : The robot returns the current battery level, *20*.

*************************
Chassis control
*************************

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Chassis movement speed control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **chassis speed x <speed_x>  y <speed_y> z <speed_z>**

    - Description
        - Controls the chassis movement speed.
    - Parameters
        - *speed_x* (float:[-3.5,3.5]): The x-axis movement speed in m/s
        - *speed_y* (float:[-3.5,3.5]): The y-axis movement speed in m/s
        - *speed_z* (float:[-600,600]): The z-axis rotation speed in °/s
    - Example
        - *chassis speed x 0.1 y 0.1 z 1;*: The x-axis speed of the chassis is 0.1 m/s, the y-axis speed is 0.1 m/s, and the z-axis rotation speed is 1°/s.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Chassis wheel speed control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **chassis wheel w1 <speed_w1> w2 <speed_w2> w3 <speed_w3> w4 <speed_w4>**
    
    - Description
        - Control the speed of the four wheels.
    - Parameters
        - *speed_w1* (int:[-1000, 1000]): The speed of the front-right mecanum wheel in rpm
        - *speed_w2* (int:[-1000, 1000]): The speed of the front-left mecanum wheel in rpm
        - *speed_w3* (int:[-1000, 1000]): The speed of the rear-right mecanum wheel in rpm
        - *speed_w4* (int:[-1000, 1000]): The speed of the rea-left mecanum wheel in rpm
    - Example
        - *chassis wheel w2 100 w1 12 w3 20 w4 11;*: The speed of the front-left mecanum wheel of the chassis is 100 rpm, that of the front-right mecanum wheel is 12 rpm, that of the rear-right mecanum wheel is 20 rpm, and that of the rear-left mecanum wheel is 11 rpm.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Chassis relative position control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **chassis move { [x <distance_x>] | [y <distance_y>] | [z <degree_z>] } [vxy <speed_xy>] [vz <speed_z>]**
    
    - Description
        - Controls the chassis to move to a specified position. The origin of the coordinate plane is the current position.
    - Parameters
        - *distance_x* (float:[-5, 5]): The x-axis movement distance in meters
        - *distance_y* (float:[-5, 5]): The y-axis movement distance in meters
        - *degree_z* (int:[-1800, 1800]): The z-axis rotation angle in degrees
        - *speed_xy* (float:(0, 3.5]): The xy-axes movement speed in m/s
        - *speed_z* (float:(0, 600]): The z-axis rotation speed in °/s
    - Example
        - *chassis move x 0.1 y 0.2;*: Taking the current position as the origin of the coordinate plane, move 0.1 m along the x-axis and 0.2 m along the y-axis.

^^^^^^^^^^^^^^^^^^^^^^^^^
Obtain the chassis speed
^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **chassis speed ?**

    - Description
        - Obtain chassis speed information.
    - Return values
        - *<x> <y> <z> <w1> <w2> <w3> <w4>*: The x-axis movement speed (m/s), the y-axis movement speed (m/s), the z-axis rotation speed (°/s), the speed of the w1 front-right mecanum wheel (rpm), the speed of the w2 front-left mecanum wheel (rpm), the speed of the w3 rear-right mecanum wheel (rpm), and the speed of the w4 rear-left mecanum wheel (rpm)
    - Example
        - IN: *chassis speed ?;*: - Obtain speed information of the chassis.
        - OUT: *1 2 30 100 150 200 250;* : The current x-axis movement speed of the chassis is 1 m/s, the y-axis movement speed is 2 m/s, the z-axis rotation speed is 20°/s, the speed of wheel 1 is 100 rpm, the speed of wheel 2 is 100 rpm, the speed of wheel 3 is 100 rpm, and the speed of wheel 4 is 100 rpm.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Obtain the chassis position
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **chassis position ?**

    - Description
        - Obtains chassis position information.
    - Return values
        - *<x> <y> <z>*: x-axis position (m), y-axis position (m), and yaw angle (°)
    - Example
        - IN: *chassis position ?;*: Obtain position information of the chassis.
        - OUT: *1 1.5 20;*: Compared with the position of the chassis when the vehicle was turned on, the current position of the chassis is 1 m along the x-axis and 1.5 m along the y-axis, with a rotation angle of 20°.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Obtain the chassis posture
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **chassis attitude ?**

    - Description
        - Obtains chassis posture information.
    - Return values
        - *<pitch> <roll> <yaw>*: pitch-axis angle (°), roll-axis angle (°), and yaw-axis angle (°)
    - Example
        - *chassis attitude ?;*: Query the posture information of the chassis.

^^^^^^^^^^^^^^^^^^^^^^^^^
Obtain the chassis status
^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **chassis status ?**

    - Description 
        - Obtains chassis status information.
    - Return values
        - *<static> <uphill> <downhill> <on_slope> <pick_up> <slip> <impact_x> <impact_y> <impact_z> <roll_over> <hill_static>* 
            - *static*: Whether the chassis is still
            - *uphill*: Whether the chassis is going uphill
            - *downhill*: Whether the chassis is going downhill
            - *on_slope*: Whether the chassis is on a slope
            - *pick_up*: Whether the chassis is picked up
            - *slip*: Whether the chassis is slipping
            - *impact_x*: Whether the x-axis senses an impact
            - *impact_y*: Whether the y-axis senses an impact
            - *impact_z*: Whether the z-axis senses an impact
            - *roll_over*: Whether the chassis is rolled over
            - *hill_static*: Whether the chassis is still on a slope
    - Example
        - IN: *chassis status ?;*: Query the status of the chassis.
        - OUT: *0 1 0 0 0 0 0 0 0 0 0;* : The chassis is going uphill.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Chassis information push control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN：**chassis push {[position <switch> pfreq <freq>][attitude <switch> afreq <freq>] | [status <switch> sfreq <switch>] [freq <freq_all>]}**

    - Description
        - Enables or disables information push for chassis attributes
        - Frequency configuration
            - Each function supports a separate frequency setting, for example:
                - *chassis push position on pfreq 1 attitude on;*: Enable position and posture push, the frequency of position push is 1Hz, and the posture push frequency is the default value of 5Hz.
            - Supports the unified configuration of the frequencies of all functions in the current module, for example:
                - chassis push freq 10; #Set all chassis push frequencies to 10Hz.
                - chassis push position pfreq 1 freq 5; #In this case, the freq parameter is specified, and the pfreq parameter is ignored.
            - The supported frequencies are 1, 5, 10, 20, 30, and 50.
        - For the push data format, see `Chassis push information data`_.
    - Parameters
        - *switch* (:data:`switch_enum`): When this parameter is set to *on*, pushing of the corresponding attribute is enabled. When this parameter is set to *off*, pushing of the corresponding attribute is disabled.
        - *freq* (int:(1,5,10,20,30,50)): The push frequency of the corresponding attribute
        - *freq_all* (int:(1,5,10,20,30,50)): The push frequencies of all relevant chassis information
    - Example
        - *chassis push attitude on;*: Enable chassis posture information push.
        - *chassis push attitude on status on;*: Enable chassis posture push and status information push.
        - *chassis push attitude on afreq 1 status on sfreq 5;*: Enable chassis posture information push, with a push frequency of once per second. At the same time, enable chassis status information push, with a push frequency of five times per second.
        - *chassis push freq 10;*: Set the push frequencies for all chassis information to 10 times per second.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Chassis push information data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

OUT: **chassis push <attr> <data>**

    - Description
        - After the user enables chassis information push, the robot will push corresponding information to the user at the set frequency.
    - Parameters
        - *attr* (:data:`chassis_push_attr_enum`): The name of the subscribed attribute
        - *data*: The data of the subscribed attribute
            - When *attr* is set to **position**, the content of *data* is *<x> <y>*.
            - When *attr* is set to **attitude**, the content of *data* is *<pitch> <roll> <yaw>*.
            - When *attr* is set to **status**, the content of *data* is *<static> <uphill> <downhill> <on_slope> <pick_up> <slip> <impact_x> <impact_y> <impact_z> <roll_over> <hill_static>*.
    - Example
        - *chassis push attitude 0.1 1 3;*: The pitch, roll, and yaw posture information of the current chassis are 0.1, 1, and 3 respectively.

*************************
Gimbal control
*************************

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Gimbal movement speed control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **gimbal speed p <speed> y <speed>**

    - Description
        - Controls the gimbal movement speed.
    - Parameters
        - *p* (float:[-450, 450]): The pitch-axis speed in °/s
        - *y* (float:[-450, 450]): The yaw-axis speed in °/s
    - Example
        - *gimbal speed p 1 y 1;*: The pitch-axis speed of the gimbal is 1°/s, and the yaw-axis speed is 1°/s.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Gimbal relative position control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **gimbal move { [p <degree>] [y <degree>] } [vp <speed>] [vy <speed>]**

    - Description
        - Controls the gimbal to move to a specified position. The origin of the coordinate plane is the current position.
    - Parameters 
        - *p* (float:[-55, 55]): The pitch-axis angle in degrees
        - *y* (float:[-55, 55]): The yaw-axis angle in degrees
        - *vp* (float:[0, 540]): The pitch-axis movement speed in °/s
        - *vy* (float:[0, 540]): The yaw-axis movement speed in °/s
    - Example
        - *gimbal move p 10;*: Taking the current position as the origin, move the gimbal to the position where the pitch-axis angle is 10°.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Gimbal absolute position control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **gimbal moveto { [p <degree>] [y <degree>] } [vp <speed>] [vy <speed>]**

    - Description
        - Controls the gimbal to move to a specified position. The origin of the coordinate plane is the startup position.
    - Parameters
        - *p* (int:[-25, 30]): The pitch-axis angle (°)
        - *y* (int:[-250, 250]): The yaw-axis angle (°)
        - *vp* (int:[0, 540]): The pitch-axis movement speed (°)
        - *vy* (int:[0, 540]): The yaw-axis movement speed (°)
    - Example
        - *gimbal moveto p 10 y -20 vp 0.1;*: Taking the robot startup position as the origin, move the gimbal to the position where the pitch-axis angle is 10° and the yaw-axis angle is -20°. At the same time, set the speed of the pitch axis to 0.1 °/s during the movement.

^^^^^^^^^^^^^^^^^^^^^^^^^
Gimbal sleep control
^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **gimbal suspend**

    - Description
        - Puts the gimbal to sleep.
    - Example
        - *gimbal suspend;*: Puts the gimbal in the sleeping state.

^^^^^^^^^^^^^^^^^^^^^^^^^
Gimbal wakeup control
^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **gimbal resume**

    - Description
        - Wakes up the gimbal from the sleeping state.
    - Parameters
        - *None*
    - Example
        - *gimbal resume;*: Wake up the gimbal from the sleeping state.

.. warning:: The sleeping state
    When the gimbal is in the sleeping state, the motors of the gimbal axes will no longer exercise control, and the gimbal will not respond to any control commands.

    To wake up the gimbal from the sleeping state, see `Gimbal wakeup control`_.

^^^^^^^^^^^^^^^^^^^^^^^^^
Gimbal recenter control
^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **gimbal recenter**

    - Description
        - Recenters the gimbal.
    - Example
        - *gimbal recenter;*: Recenter the gimbal.

^^^^^^^^^^^^^^^^^^^^^^^^^
Obtain the gimbal posture
^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **gimbal attitude ?**

    - Description
        - Obtains gimbal posture information.
    - Return values
        - *<pitch> <yaw>*: pitch-axis angle (°) and yaw-axis angle (°)
    - Example
        - IN: *gimbal attitude ?;*: Query the angle information of the gimbal.
        - OUT: *-10 20;*: Set the pitch-axis angle of the gimbal to -10° and the yaw-axis angle to 20°.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Gimbal information push control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **gimbal push <attr> <switch> [afreq <freq_all>]**

    - Description
        - Enables or disables information push for gimbal attributes.
        - For the push data format, see `Gimbal push information data`_.
    - Parameters
        - *attr* (:data:`gimbal_push_attr_enum`): The name of the subscribed attribute
        - *switch* (:data:`switch_enum`): When this parameter is set to *on*, pushing of the corresponding attribute is enabled. When this parameter is set to *off*, pushing of the corresponding attribute is disabled.
        - *freq_all*: The push frequencies of all relevant gimbal information
    - Example
        - *gimbal push attitude on;*: Enable gimbal information push.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Gimbal push information data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

OUT: **gimabal push <attr> <data>**

    - Description
        - After the user enables gimbal information push, the robot will push corresponding information to the user at the set frequency.
    - Parameters
        - *attr* (:data:`gimbal_push_attr_enum`): The name of the subscribed attribute
        - *data*: The data of the subscribed attribute
            - When *attr* is set to **attitude**, the content of *data* is *<pitch> <yaw>*.
    - Example
        - *gimbal push attitude 20 10;*: Set the pitch-axis angle of the gimbal to 20° and the yaw-axis angle to 10°.

*************************
Blaster control
*************************

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Single blaster shot amount
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN：**blaster bead <num>**

    - Description
        - Sets the single blaster shot amount.
    - Parameters
        - *num* (int:[1,5]): The shot amount
    - Example
        - *blaster bead 2;*: Instruct the blaster to fire two shots at a time.

^^^^^^^^^^^^^^^^^^^^^^^^^
Blaster firing control
^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **blaster fire**

    - Description
        - Instructs the water gun to fire once.
    - Example
        - *blaster fire;*: Instruct the water gun to fire once.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Obtain the amount of a single blaster shot
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **blaster bead ?**

    - Description
        - Obtains the number of water bombs fired by the water gun at a time.
    - Return values
        - *<num>*: The number of water bombs fired by the water gun at a time
    - Example
        - IN: *blaster bead ?;*: Query the number of water bombs fired by the water gun at a time.
        - OUT: *3;*: The current number of water bombs fired by the water gun at a time is 3.

*************************
Armored plate control
*************************

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Armored plate sensitivity control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **armor sensitivity <value>**
    
    - Description
        - Sets the strike detection sensitivity of the armored plate.
    - Parameters
        - *value* (int:[1,10]): The greater the sensitivity of the armored plate, the easier it is to detect a strike. The default sensitivity value is 5.
    - Example
        - *armor sensitivity 1;*: Set the strike detection sensitivity of the armored plate to 1.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Obtain the armored plate sensitivity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **armor sensitivity ?**

    - Description
        - Obtains the strike detection sensitivity of the armored plate.
    - Parameters
        - *<value>*: Sensitivity of the armored plate
    - Example
        - IN: *armor sensitivity ?;*: Query the strike detection sensitivity of the armored plate.
        - OUT: *5;*: Query the strike detection sensitivity of the armored plate.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Armored-plate event reporting control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **armor event <attr> <switch>**

    - Description
        - Controls armored-plate detected event reporting.
        - For the format of event reporting data, see `Armored-plate event reporting data`_.
    - Parameters
        - *attr* (:data:`armor_event_attr_enum`): The name of the event attribute
        - *switch* (:data:`switch_enum`): The event attribute control switch
    - Example
        - *armor event hit on;*: Enable armored-plate detected event push.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Armored-plate event reporting data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

OUT: **armor event hit <index> <type>**

    - Description
        - When an armored-plate hit event occurs, this message can be received from the event push port.
    - Parameters
        - *index* (int:[1, 6]): The ID of the armored plate where a hit event occurs
            - ``1``: At the rear end the chassis
            - ``2``: At the front end of the chassis
            - ``3``: On the left side of the chassis
            - ``4``: On the right side of the chassis
            - ``5``: On the left side of the gimbal
            - ``6``: On the right side of the gimbal
        - *type* (int:[0, 2]): The type of the current tap event
            - ``0``: A water-bomb attack
            - ``1``: A strike
            - ``2``: A hand hit
    - Example
        - *armor event hit 1 0;*: Armored plate 1 detects a water-gun attack.

*************************
Voice recognition control
*************************

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Voice recognition event reporting control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **sound event <attr> <switch>**

    - Description
        - Controls voice recognition event reporting. Once enabled, relevant events will be reported.
        - For the format of reporting data, see `Voice recognition event reporting data`_.
    - Parameters
        - *attr* (:data:`sound_event_attr_enum`): The name of the event attribute
        - *switch* (:data:`switch_enum`): The event attribute control switch
    - Example
        - *sound event applause on;*: Enables voice (applause) recognition.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Voice recognition event reporting data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

OUT: **sound event <attr> <data>**

    - Description
        - When a certain voice event occurs, this message can be received from the event push port.
        - For information about enabling this event, refer to `Voice recognition event reporting control`_.
    - Parameters
        - *attr* (:data:`sound_event_attr_enum`):  The name of the event attribute
        - *data*: The data of the event attribute
            - When *attr* is set to ``applause``, *data* is *<count>*, indicating the number of hand claps within a short time.
    - Example
        - *sound event applause 2;*: Two hand claps were recognized in a short time.

*************************
PWM control
*************************

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Control the PWM output duty cycle
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **pwm value <port_mask> <value>**

    - Description
        - Sets the PWM output duty cycle.
    - Parameters
        - *port_mask* (hex:0-0xffff): The PWM extended port mask combination. The mask for output port X is **1 << (X-1)**.
        - *value* (float:0-100): The PWM output duty cycle, which defaults to 12.5.
    - Example
        - *pwm value 1 50;*: Set the duty cycle of PWM port 1 to 50%.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PWM output frequency control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **pwm freq <port_mask> <value>**

    - Description
        - Sets the PWM output frequency.
    - Parameters
        - *port_mask* (hex:0-0xffff): The PWM extended port mask combination. The mask for output port X is **1 << (X-1)**.
        - *value* (int:XXX): The PWM output frequency
    - Example
        - *pwm freq 1 1000;*: Set the frequency of PWM port 1 to 1,000Hz.

*************************
LED control
*************************

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
LED lighting effect control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN：**led control comp <comp_str> r <r_value> g <g_value> b <value> effect <effect_str>**

    - Description
        - This interface controls the robot's LED lighting effect. Multiple effects can be configured.
        - The marquee effect is available only to the LED lights on both sides of the gimbal.
    - Parameters
        - *comp_str* (:data:`led_comp_enum`): The LED light number
        - *r_value* (int:[0, 255]): The red component value of RGB
        - *g_value* (int:[0, 255]): The green component value of RGB
        - *b_value* (int:[0, 255]): The blue component value of RGB
        - *effect_str* (:data:`led_effect_enum`): The type of the LED lighting effect

    - Example
        - *led control comp all r 255 g 0 b 0 effect solid;* : Set all LED lights of the robot to solid red.

*************************
Sensor adapter control
*************************

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Obtain the ADC value of the sensor adapter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **sensor_adapter adc id <adapter_id> port <port_num> ?**

    - Description
        - Obtains the ADC value of the sensor adapter.
    - Parameters
        - *adapter_id* (int:[1, 6]): The adapter ID
        - *port_num* (int:[1, 2]): The port number
    - Return values
        - *adc_value*: Measure the voltage of the specified port on the corresponding adapter, whose range is [0V, 3,3V]. 
    - Example
        - IN: *sensor_adapter adc id 1 port 1 ?;*: Query the ADC value of port 1 on adapter 1
        - OUT: *1.1;*: The retrieved ADC value of the port is 1.1.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Obtain the I/O value of the sensor adapter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **sensor_adapter io_level id <adapter_id> port <port_num> ?**

    - Description
        - Obtain the logic level of the I/O port on the sensor adapter.
    - Parameters
        - *adapter_id* (int:[1, 6]): The adapter ID
        - *port_num* (int:[1, 2]): The port number
    - Return values
        - *io_level_value*: Measure the logical level of the specified port on the corresponding adapter, which is 0 or 1.
    - Example
        - IN: *sensor_adapter io_level id 1 port 1 ?;*: Query the I/O logic level of port 1 on adapter 1.
        - OUT: *1;*: The retrieved I/O value of the port is 1.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Obtain the I/O pin level transition time of the sensor adapter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **sensor_adapter pulse_period id <adapter_id> port <port_num>**

    - Description
        - Obtains the level transition duration of the I/O port on the sensor adapter.
    - Parameters
        - *adapter_id* (int:[1, 6]): The adapter ID
        - *port_num* (int:[1, 2]): The port number
    - Return values
        - *pulse_period_value*: Measure the level transition duration of the specified port on the corresponding adapter, in milliseconds.
    - Example
        - *sensor_adapter pulse_period id 1 port 1;*: Query the level transition duration of port 1 on adapter 1.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Sensor adapter event reporting control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **sensor_adapter event io_level <switch>**

    - Description
        - Enables or disables the push of level transition events of the sensor adapter. When enabled, messages are pushed when the I/O level transits. For details, see the next section [Push sensor adapter level transition events](#Push sensor adapter level transition).  
    - Parameters
        - *switch* (:data:`switch_enum`): The control switch for level transition event reporting
    - Example
        - *sensor_adapter event io_level on;*: Enable the pushing of sensor adapter level transition events.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Sensor adapter event reporting data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

OUT: *sensor_adapter event io_level (<id>, <port_num>, <io_level>)*

    - Description
        - Pushes a message when the sensor adapter encounters a level transition. This message can be received from the event push port.
        - You need to enable push for sensor adapter level transition. For details, see `Sensor adapter event reporting data`_.
    - Parameters
        - *id*: The sensor adapter ID
        - *port_num*: The I/O port ID
        - *io_level*: The current logic level
    - Example
        - *sensor_adapter event io_level (1, 1, 0);*: The logic level of I/O port 1 on adapter 1 transits to 0.

***********************************
Infrared distance sensor control
***********************************

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Switch control for the infrared distance sensor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **ir_distance_sensor measure <switch>**

    - Description
        - Enables or disables all infrared sensor switches.
    - Parameters
        - *switch* (:data:`switch_enum`): The switch of the infrared sensor
    - Example
        - *ir_distance_sensor measure on;*: Enables all infrared distance sensors.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Obtain the distance measured by the infrared distance sensor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **ir_distance_sensor distance <id> ?**

    - Description
        - Obtains the distance measured by the infrared distance sensor of the specified ID.
    - Parameters
        - *id* (int:[1, 4]): Infrared sensor ID
    - Return values
        - *distance_value*: The distance measured by the infrared sensor of the specified ID, in millimeters.
    - Example
        - IN: *ir_distance_sensor distance 1 ?;*: Query the distance measured by infrared distance sensor 1.
        - OUT: *1000;*: The current distance measured by the infrared distance sensor is 1,000 mm.

*************************
Servo control
*************************

^^^^^^^^^^^^^^^^^^^^^^^^^
Servo angle control
^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **servo angle id <servo_id> angle <angle_value>**

    - Description
        - Set the servo angle.
    - Parameters
        - *servo_id* (int:[1, 3]): The servo ID
        - *angle_value* (float:[-180, 180]): The specified angle in degrees
    - Example
        - *servo angle id 1 angle 20;*: Set the angle of servo 1 to 20°.

^^^^^^^^^^^^^^^^^^^^^^^^^
Servo speed control
^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **servo speed id <servo_id> speed <speed_value>**

    - Description
        - Sets the speed of the specified servo.
    - Parameters
        - *servo_id* (int:[1, 3]): The servo ID
        - *speed_value* (float:[-1800, 1800]): The set speed in °/s 
    - Example
        - *servo speed id 1 speed 20;*: Set the speed of servo 1 to 10°/s.

^^^^^^^^^^^^^^^^^^^^^^^^^
Servo stop control
^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **servo stop**

    - Description
        - Stops the servo.
    - Example
        - *servo stop;*: Stop the servo.

^^^^^^^^^^^^^^^^^^^^^^^^^
Servo angle query
^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **servo angle id <servo_id> ?**

    - Description
        - Obtains the angle of the specified servo.
    - Parameters
        - *servo_id* (int:[1, 3]): The servo ID
    - Return values
        - *angle_value*: The angle of the specified servo
    - Example
        - IN: *servo angle id 1 ?;*: Obtain the angle of servo 1.
        - OUT: *30;*: The current angle of the servo is 30°.

*************************
Mechanical arm control
*************************

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Control the relative position of the mechanical arm
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **robotic_arm move x <x_dist> y <y_dist>**

    - Description
        - Controls the mechanical arm to move a certain distance. The current position is the origin of the coordinates plane.
    - Parameters
        - *x_dist* (float:[]): The x-axis movement distance in centimeters
        - *y_dist* (float:[]): The y-axis movement distance in centimeters
    - Example
        - *robotic_arm move x 5 y 5;*: Move the mechanical arm 5 cm along the x-axis and 5 cm along the y-axis.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Control the absolute position of the mechanical arm
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **robotic_arm moveto x <x_pos> y <y_pos>**

    - Description
        - Controls the mechanical arm to move to a certain position. The startup position of the robot is the origin of the coordinate plane.
    - Parameters
        - *x_pos* (float:[]): The target x-axis coordinate in centimeters
        - *y_pos* (float:[]): The target y-axis coordinate in centimeters
    - Example
        - *robotic_arm moveto x 5 y 5;*: Move the mechanical arm to the 5 cm coordinate position on the x-axis and the 5 cm coordinate position on the y-axis.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Mechanical arm recenter control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **robotic_arm recenter**

    - Description
        - Recenters the mechanical arm.
    - Parameters
        - *None*
    - Example
        - *robotic_arm recenter;*: Recenter the mechanical arm.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Mechanical arm stop control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **robotic_arm stop**

    - Description
        - Stops the mechanical arm.
    - Parameters
        - *None*
    - Example
        - *robotic_arm stop;*: Stop the mechanical arm.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Query the absolute position of the mechanical arm
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **robotic_arm position ?**

    - Description
        - Obtains the position of the mechanical arm.
    - Parameters
        - *None*
    - Return values
        - *<x_pos> <y_pos>*: The coordinates of the mechanical arm
            - *x_pos*: The x-axis coordinate in centimeters
            - *y_pos*: The y-axis coordinate in centimeters
    - Example
        - IN: *robotic_arm position ?;*: Query the position of the mechanical arm.
        - OUT: *50 60;*: The mechanical arm is 50 cm from the calibration point on the x-axis and 60 cm on the y-axis.

****************************
Mechanical gripper control
****************************

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Mechanical gripper opening control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **robotic_gripper open [leve <level_num>]**

    - Description
        - Opens the mechanical gripper.
    - Parameters
        - *level_num* (int:[1,4]): The opening force level of the mechanical gripper, whose range is [1,4]
    - Example
        - *robotic_gripper open 1;*: Opens the mechanical arm with a force of 1.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Mechanical gripper closing control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **robotic_gripper close [leve <level_num>]**

    - Description
        - Closes the mechanical gripper.
    - Parameters
        - *level_num* (int:[1,4]): The closing force level of the mechanical gripper, whose range is [1,4]
    - Example
        - *robotic_gripper close 1;*: Closes the mechanical arm with a force of 1.

.. note:: The mechanical gripper control force

    The **mechanical gripper control force** describes the speed of the mechanical gripper during the movement and the maximum clamping force in the locked-rotor state.

    The greater the force, the faster the movement speed and the greater the clamping force.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Query the open/close status of the mechanical gripper
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **robotic_gripper status ?**

    - Description
        - Obtains the open/close status of the mechanical gripper
    - Parameters
        - *None*
    - Return values
        - *status*: The current open/close status of the mechanical gripper
            - ``0``: The mechanical gripper is fully closed.
            - ``1``: The mechanical gripper is neither fully closed nor fully opened.
            - ``2``: The mechanical gripper is fully opened.
    - Example
        - IN: *robotic_gripper status ?;*: Obtain the open/close status of the mechanical gripper.
        - OUT: *2;*: The mechanical gripper is opened.

*****************************************
Intelligent recognition function control
*****************************************

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Control intelligent recognition function attributes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **AI attribute { [line_color <line_color>] [marker_color <marker_color>] [marker_dist <dist>] }**

    - Description
        - Controls intelligent recognition function attributes.
    - Parameters
        - *line_color* (:data:`line_color_enum`): The line identification color
        - *marker_color* (:data:`marker_color_enum`): The visual label color
        - *marker_dist* (float:[0.5, 3]): The minimum effective distance of visual labels in meters
    - Example
        - IN: *AI attribute line_color red;*: Set the line identification color to red.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Control intelligent recognition function push
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **AI push <attr> <switch>**

    - Description
        - Controls intelligent recognition function push.
        - Different intelligent recognition functions are mutually exclusive and cannot be enabled at the same time. If mutually exclusive functions exist in the set of functions to enable, all functions will fail to be enabled. For the mutual exclusion relationships, refer to :ref:`Mutual exclusion relationships between intelligent recognition functions<Mutual exclusion relationships between intelligent recognition functions>`.
        - You cannot currently set the frequency.
        - For the data submission format, see `Intelligent recognition function push data`_.
    - Parameters
        - *attr* (:data:`AI_push_attr_enum`): Enumerated intelligent recognition functions, which cannot be enabled at the same time for certain parameters.
        - *switch* (:data:`switch_enum`): When this parameter is set to *on*, pushing of the corresponding attribute is enabled. When this parameter is set to *off*, pushing of the corresponding attribute is disabled.
    - Example
        - IN: *AI push marker on line on;*: Enable the push for line and visual label recognition data.

.. - Mutual exclusion relationships between intelligent recognition functions:

.. note:: Mutual exclusion relationships between intelligent recognition functions

    Due to the limited computing resources of the robot, mutual exclusion relationships exist between intelligent recognition functions. Mutually exclusive intelligent functions cannot be turned on at the same time.
    Intelligent recognition functions are divided into groups A and B:

        +--+-------+-----+------+-----+
        |A |people |pose |marker|robot|
        +--+-------+-----+------+-----+
        |B | line                     |
        +--+--------------------------+

    For the preceding two groups, only one function can be turned on for each group at a time, and any function combinations between the two groups are allowed.

^^^^^^^^^^^^^^^^^^^^^^^^^
Intelligent recognition function push data
^^^^^^^^^^^^^^^^^^^^^^^^^

OUT: **AI push <attr> <data>**

    - Description
        - After you enable intelligent recognition function push, the robot will push corresponding information to you at the set frequency.
    - Parameters
        - *attr* (:data:`AIi_push_attr_enum`): The subscribed function name
        - *data*: The subscribed attribute data
            - When *attr* is set to **person**, the content is <n> <x1> <y1> <w1> <h1> <x2> <y2>... <wn> <hn>
            - When *attr* is set to **gesture**, the content is <n> <info1> <x1> <y1> <w1> <h1> <x2> <y2>... <wn> <hn>. For the meaning of info, refer to :data:`AI_pose_id_enum`.
            - When *attr* is set to **marker**, the content is <n> <info1> <x1> <y1> <w1> <h1> <x2> <y2>... <wn> <hn>. For the meaning of info, refer to :data:`AI_marker_id_enum`.
            - When *attr* is set to **line**, the content is <n> <x1> <y1> <θ1> <c1> <x2> <y2>... <θ10n> <c10n>
            - When *attr* is set to **robot**, the content is <n> <x1> <y1> <w1> <h1> <x2> <y2>... <wn> <hn>

    - Example
        - OUT: *AI push person 1 0.5 0.5 0.3 0.7;*: A pedestrian is currently recognized, the coordinates are (0.5, 0.5), the target width is 0.3, and the height is 0.7.

.. note:: Intelligent function push data

    In intelligent recognition function push data, n, x, y, w, and h are all general data, which are described as follows:

        *n*: The number of recognized targets

        *x*: The center of the recognized target on the x-axis of the field of view

        *y*: The center of the recognized target on the y-axis of the field of view

        *w*: The width of the recognized target

        *h*: The height of the recognized target

    n, x, y, θ, and c in line recognition push data are described as follows:

        *n*: The number of recognized lines. Each line has 10 points. For detailed point data, see below.

        *x*: The line point is on the x-axis of the field of view.

        *y*: The line point is on the y-axis of the field of view.

        *θ*: The tangent angle of the line point

        *c*: The curvature of the curve corresponding to the line point, whose range is [0, 10]. The value 0 indicates a straight line.

    The preceding x, y, w, and h values are all normalized values, whose ranges are all [0, 1]. The origin of the coordinate plane is at the upper-left of the field of view.

*************************
Camera control
*************************

^^^^^^^^^^^^^^^^^^^^^^^^^
Camera exposure configuration
^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **camera exposure <ev_level>**

    - Description
        - Sets the camera exposure value.
    - Parameters
        - *ev_level* (:data:`camera_ev_enum`): Enumerated camera exposure values
    - Example
        - *camera exposure small;*: Set the camera exposure value to low.

*************************
Video stream control
*************************

^^^^^^^^^^^^^^^^^^^^^^^^^
Video stream on control
^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **stream on**

    - Description
        - Turns on the video stream.
        - When turned on, you can receive H.264-encoded stream data from the video stream port.
    - Example
        - *stream on;*: Turn on the video stream.

^^^^^^^^^^^^^^^^^^^^^^^^^
Video stream off control
^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **stream off**

    - Description
        - Turns off the video stream.
        - When turned off, H.264-encoded stream data output stops.
    - Example
        - *stream off;*: Turn off the video stream.

*************************
Audio stream control
*************************

^^^^^^^^^^^^^^^^^^^^^^^^^
Audio stream on control
^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **audio on**

    - Description
        - Turns on the audio stream.
        - When turned on, you can receive Opus-encoded audio stream data from the audio stream port.
    - Example
        - *audio on;*: Turn on the audio stream.

^^^^^^^^^^^^^^^^^^^^^^^^^
Audio stream off control
^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **audio off**

    - Description
        - Turns off the audio stream.
        - When turned off, Opus-encoded audio stream data output stops.
    - Example
        - *audio off;*: Turn off the audio stream.

*************************
IP broadcasting
*************************

OUT: **robot ip <ip_addr>**

    - Description
        - When no connection is established with the robot, this message can be received from the IP broadcasting port. After a connection is established, this message stops being broadcast.
        - Displays the IP address of the current robot, which is applicable to situations where the robot is in the same LAN but the IP information of the robot is unknown.
    - Parameters
        - *ip_addr*: The current IP address of the robot
    - Example
        - *robot ip 192.168.1.102;*: The current IP address of the robot is 192.168.1.102.

*************************
Event data acquisition
*************************

^^^^^^^^^^^^^^^^^^^^^^^^^^^
Turn on keyboard data push
^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **game_msg on**

    - Description
        - Turns on keyboard and mouse data push for youth competition systems.
    - Parameters
        - *None*
    - Example
        - *game_msg on;*: Turn on keyboard and mouse data push.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Turn off keyboard data push
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IN: **game_msg off**

    - Description
        - Turns off keyboard and mouse data push for youth competition systems.
    - Parameters
        - *None*
    - Example
        - *game_msg off;*: Turn off keyboard and mouse data push.
 
^^^^^^^^^^^^^^^^^^^^^^^^^
Keyboard data push data
^^^^^^^^^^^^^^^^^^^^^^^^^

OUT: **game msg push <data>**

    - Description
        - After you enable event data push, the robot will push the corresponding information as a string to you at a fixed frequency.
    - Parameters
        - *data*: The subscribed attribute data
            - The content is [cmd_id, len, mouse_press, mouse_x, mouse_y, seq, key_num, key_1, key2,...].
            - mouse_press: 1 for the right mouse button, 2 for the left mouse button, and 4 for the central mouse button
            - mouse_x: The mouse movement distance, whose range is -100 to 100
            - mouse_y: The mouse movement distance, whose range is -100 to 100
            - seq: The serial number, whose range is 0 to 255
            - key_num: The number of recognized buttons, which cannot exceed three
            - key1: The key value

    - Example
        - OUT: *game msg push [0, 6, 1, 0, 0, 255, 1, 199];* : cmd_id is 0, the data length is 6, the right mouse button is recognized, the w button is pressed, and the packet serial number is 255.
