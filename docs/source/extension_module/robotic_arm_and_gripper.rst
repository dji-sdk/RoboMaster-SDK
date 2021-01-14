======================================
Mechanical Arm and Mechanical Gripper
======================================

Introduction
-------------------

The mechanical arm supports FPV precise remote control, and the mechanical gripper is used in conjunction with the mechanical arm to support clamping force control. In the app, you can control the mechanical arm and the mechanical gripper to complete tasks from the first-person perspective.

.. image:: ../images/arm&gripper.png
	:scale: 30%

Instructions for use
-------------------------

Users can control the movement range of the mechanical arm and the opening and closing distance of the mechanical gripper. Specifically, the horizontal movement range of the mechanical arm is 0 to 0.22 m, and the vertical movement range is 0 to 0.15 m. The opening and closing distance of the mechanical claw is about 10 cm.

.. warning::
	1. When the mechanical arm or mechanical gripper is working, avoid applying external force to it as far as possible.

	2. Do not collide or damage the mechanical arm or mechanical gripper to avoid performance degradation or abnormal operation of the servo.

	3. Do not touch the rotating or sharp parts of the mechanical arm or mechanical gripper to avoid injury.

	4. Promptly clean water droplets, crystal bomb residue, and other foreign objects to avoid corrosion of the structure surface.
	
Description of the mechanical gripper's PWM interface:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The mechanical gripper supports the torque control mode

.. image:: ../images/arm_pwm.png
	:scale: 20%

+----------+------------+  
|    No.    |    Pin    |   
+==========+============+
|    1    |    485A/PWM    |  
+----------+------------+
|    2    |    485B    |  
+----------+------------+  
|    3    |    VCC-12V    | 
+----------+------------+
|    4    |    GND    |  
+----------+------------+

The frequency of the PWM signal is 50Hz, and the duty cycle is between 2.5% and 12.5%.

1. A duty cycle between 2.5% and 7.5% corresponds to the [Maximum, 0] closing force.

2. A duty cycle between 7.5% and 12.5% corresponds to the [0, Maximum] opening force.

Python API
--------------------------

Refer to :doc:`Mechanical Arm<../python/robotic_arm>` and :doc:`Mechanical Gripper<../python/gripper>`.
