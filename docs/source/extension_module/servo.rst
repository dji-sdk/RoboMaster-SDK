================
Servo
================

Introduction
---------------

In addition to supporting 485 control, the throttle control mode of the servo can also be controlled by PWM. The control modes are the speed mode and the angle mode.

.. note:: Control modes of the servo

    The control mode of the servo is switched through the official programming interface (Scratch/Python). This mode is recorded in the servo and will not be reset when the servo is powered off. Before using PWM control, confirm the current control mode of the servo.

Pin description
-----------------

The 485 and PWM pins on the servo are multiplexed, as shown in the figure below:

.. image:: ../images/arm_pwm.png
    :scale: 20%

+----------+------------+
|    No.   |    Pin     |
+==========+============+
|    1     |  485A/PWM  |
+----------+------------+
|    2     |    485B    |
+----------+------------+
|    3     |  VCC-12V   |
+----------+------------+
|    4     |    GND     |
+----------+------------+

Control description
-------------------------

In PWM control mode, the input and output of the servo are described as follows.

+--------------------+--------------------+----------------------+--------------------------------+   
|    Control mode    |    Pulse period    |    Throttle range    |         Servo output           |   
+====================+====================+======================+================================+   
|      Angle mode    |    50Hz            |      2.5%-12.5%      |           0°-360°              |   
+--------------------+--------------------+----------------------+--------------------------------+    
|                    |                    |       2.5%-7.5%      |        49-0 rpm (clockwise)    |   
|    Speed mode      |        50Hz        +----------------------+--------------------------------+   
|                    |                    |      7.5%-12.5%      |   0-49 rpm (counterclockwise)  |   
+--------------------+--------------------+----------------------+--------------------------------+ 

Python API
--------------------------

Refer to :doc:`Servo<./python/servo>`.
