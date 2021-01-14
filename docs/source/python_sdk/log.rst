.. _log:


##################################
Logging for the RoboMaster SDK
##################################

Configure the log level
___________________________

The default log level of the RoboMaster SDK is ERROR. Users can change it as needed.

- The statement for setting the log level in :file:`/examples/01_robot/00_logger.py` is as follows:::

    logger.setLevel(logging.ERROR)

- You can change it to this statement based on their needs:::

    logger.setLevel(logging.WARNING)

  You can also change the statement to the following:::

    logger.setLevel(logging.INFO)


Use log files
____________________

If users encounter a problem during use, they need to write the log to a file and provide the log file to technical support personnel.

**Generation method of log files**

- Add this statement at the beginning of the program:::

    robomaster.enable_logging_to_file()

- Run the program.

- The SDK will automatically generate a system log file and store it in a directory at the same level as the program. The name format of log files is as follows:::

    RoboMasterSDK_YYYYMMDDHHMMSS_log.txt

- Send the generated system log file to `developer@dji.com` by using this email template:::

    xxxxxxxx
    xxxxxxxx
    xxxxxxxx

**Sample code**

- Refer to the example in the :file:`/examples/01_robot/00_logger.py` directory of SDK code.

.. literalinclude:: ./../../../examples/01_robot/00_logger.py
   :language: python
   :linenos:
   :lines: 16-

- After running the program, the SDK will automatically generate a system log file in a directory at the same level as the program, as shown in the figure below:

	.. image:: ./../images/log_file.png
            :scale: 100%
            :align: center
