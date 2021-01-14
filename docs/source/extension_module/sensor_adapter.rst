================
Sensor Adapter
================

Introduction
----------

The sensor adapter module is designed to help you to connect the temperature, pressure, ranging, and other sensors to RoboMaster EP. Sensor data information can be obtained in the Scratch programming environment. Each sensor adapter module has two sensor interfaces with identical functions.

.. image:: ../images/pinboard.png
	:scale: 30%

Pin description
----------

+----------+---------------+------------------------------------------------------------+   
|   Port   |    Pin        |           Function                                         |   
+==========+===============+============================================================+   
|   port1  |    VCC        | Positive terminal with an output voltage of 3.3V           |   
+          +---------------+------------------------------------------------------------+    
|          |    GND        |      The power ground                                      |   
+          +---------------+------------------------------------------------------------+   
|          |    I/O        |    The level input, with an input range of 0-3.3V          |   
+          +---------------+------------------------------------------------------------+ 
|          |     AD        |    The analog voltage input, with an input range of 0-3.3V |   
+----------+---------------+------------------------------------------------------------+ 
|  port2   | Same as port1 |    Same as port1                                           |   
+----------+---------------+------------------------------------------------------------+

Python API
--------------------------

Refer to :doc:`Sensor Adapter<../python/sensor_adapter>`.
