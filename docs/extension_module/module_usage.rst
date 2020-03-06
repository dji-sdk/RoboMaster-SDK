================================================
Instructions for Using Extension Modules
================================================

Infrared Distance Sensor (TOF)
--------------------------------
1. Introduction

The infrared distance sensor is designed based on the principle of TOF (Time of Flight). In other words, the sensor emits modulated near-infrared light, which is reflected when it encounters an object. The sensor calculates the distance from the object by calculating the time difference or phase difference between the emission and reflection of the light.

2. Product characteristics

The detected area of the TOF is shown in the figure below.

.. image:: ../images/tof.png

It emits a conical light with an angle of 20°. The relationship between the light spot D and the distance Dist is:

    **D=2×Dist×tan⁡(10)**

In order to achieve the best test results, the size of the target should at least equate to the size of the TOF light spot.
 
.. tip:: If the target is smaller than the light spot size, the target should be as much towards the center of the light spot as possible. This is because the light intensity distribution in the light spot is not uniform, but rather a Gaussian-like distribution, with strong light in the middle and weak light around. In order to ensure sufficient light energy is returned, the target should be at the center of the light spot as much as possible.


3. Pin description

====== ======= ============ =================================
No.    Pin     Function     Corresponding connection item
====== ======= ============ =================================
1      GND     Power supply	GND
2      VCC     Power supply	VCC
3      RX      Receive	    TX
4      TX      Transmit	    RX
====== ======= ============ =================================

4. Communication protocol and data formats

============= ========== ========= ========= ============
COM interface  Baud rate Data bits Stop bits Parity check
============= ========== ========= ========= ============
UART          115200     8         1         none
============= ========== ========= ========= ============

Control command input:

.. data:: ir_distance_sensor_measure_on

	:Description: Enable data output of the TOF
	

.. data:: ir_distance_sensor_measure_off

	:Description: Disable data output of the TOF
	

Data output:

.. data:: ir distance:xxx

	:Description: Data format of the TOF
	
.. tip:: Command formats are input and output as strings

Servo
--------
1. Introduction

In addition to supporting the 485 control, the throttle control mode of the servo can also carry out PWM control. PWM mode only supports angle control

2. Pin description

The 485 pin and PWM pin on the servo are multiplexed, as shown in the figure below

.. image:: ../images/servo.png


3. Control description

The corresponding input and output of the servo in PWM control mode

+--------------+----------------+------------------+----------------------+   
| Control mode | Pulse period   |  Throttle range  |    Servo output      |   
+==============+================+==================+======================+   
|  Angle mode  |      50Hz      |    2.5%~12.5%    |       0°~360°        |   
+--------------+----------------+------------------+----------------------+    
