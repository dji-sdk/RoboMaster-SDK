===========================
Infrared Distance Sensor
===========================

Introduction
-------------------

The infrared distance sensor is designed based on the time of flight (TOF) principle. That is, the sensor emits modulated near-infrared light, which is reflected when it strikes an object. The sensor then calculates the distance to the object by calculating the time difference or phase difference between light emission and reflection.

Product features
--------------------

The detection area of ​​the infrared distance sensor is shown in the figure below:

.. image:: ../images/tof.png

The sensor emits a conical light with an angle of 20°. The relationship between the spot (D) and the distance (Dist) is calculated as follows:

    **D=2×Dist×tan⁡(10)**

To achieve optimal test results, the size of the target must at least equal the size of the TOF spot.
 
.. tip:: If the size of the target is smaller than the spot size, ensure that the target is in the center of the spot as far as possible because the light intensity distribution in the spot is not uniform, but a Gauss-like distribution. Specifically, the light intensity is strong in the center and weaker around the edges. For this reason, to ensure sufficient reflected light energy, the target must be in the center of the light spot as far as possible.


Pin description
--------------------

.. image:: ../images/tof_module.png
	:scale: 40%

The following describes the UART port of the infrared distance sensor:

====== ======= ====== ===========
No.    Pin    Function    Corresponding Connection Item
====== ======= ====== ===========
1	VCC	Power supply	Positive terminal
2	GND	Power supply	Power ground
3	TX	Transmission	RX
4	RX	Reception	TX
====== ======= ====== ===========

Communication protocol and data format
-------------------------------------------------

========= ====== ====== ====== ==========
Communication interface    Baud rate    Data bit    Stop bit    Parity
========= ====== ====== ====== ==========
UART    115200    8    1    N/A
========= ====== ====== ====== ==========

Control command input:

.. data:: ir_distance_sensor_measure_on

	:description: Enables data output by the infrared distance sensor, at the output frequency of 20 Hz.
	

.. data:: ir_distance_sensor_measure_off

	:description: Disables data output by the infrared distance sensor.
	

Data output:

.. data:: ir distance:xxx

	:description: Data format of the infrared distance sensor
	
.. tip:: Commands are input and output in the form of strings.

Python API
--------------------------

Refer to :doc:`Infrared Distance Sensor<../python/ir_distance_sensor>`.
