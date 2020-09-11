.. _log:


##################################
RoboMaster SDK 如何记录日志
##################################

配置日志等级
____________

RoboMaster SDK 的日志等级默认为ERROR，用户可根据自己的需要进行修改。

- 设置日志等级的语句为 :file:`/examples/01_robot/00_logger.py` 中该行代码::

    logger.setLevel(logging.ERROR)

- 用户可根据自己的需要将其修改为::

    logger.setLevel(logging.WARNING)

  或者::

    logger.setLevel(logging.INFO)


日志文件的使用
____________________

如果用户是使用过程中遇到问题，需要将日志写入文件中，并将日志文件提供给技术支持人员。

**生成日志文件方法**

- 用户需要在程序最开始添加语句::

    robomaster.enable_logging_to_file()

- 运行程序

- SDK会自动生成对应的系统日志文件，存放路径为该程序同级目录中，日志文件命名格式为::

    RoboMasterSDK_YYYYMMDDHHMMSS_log.txt

- 将生成的系统日志文件发送到邮箱 `developer@dji.com`，邮件模板如下::

    xxxxxxxx
    xxxxxxxx
    xxxxxxxx

**示例代码**

- 参考sdk代码 :file:`/examples/01_robot/00_logger.py` 目录下的例程

.. literalinclude:: ./../../../examples/01_robot/00_logger.py
   :language: python
   :linenos:
   :lines: 16-

- 运行程序后SDK会在在程序的同级目录下会自动生成系统日志文件,如下图所示

	.. image:: ./../images/log_file.png
            :scale: 100%
            :align: center
