.. _log:


##################################
RoboMaster SDK 如何記錄日誌
##################################

配置日誌等級
____________

RoboMaster SDK 的日誌等級默認為ERROR，用戶可根據自己的需要進行修改。

- 設置日誌等級的語句為 :file:`/examples/01_robot/00_logger.py` 中該行代碼::

    logger.setLevel(logging.ERROR)

- 用戶可根據自己的需要將其修改為::

    logger.setLevel(logging.WARNING)

  或者::

    logger.setLevel(logging.INFO)


日誌文件的使用
____________________

如果用戶是使用過程中遇到問題，需要將日誌寫入文件中，並將日誌文件提供給技術支持人員。

**生成日誌文件方法**

- 用戶需要在程序最開始添加語句::

    robomaster.enable_logging_to_file()

- 運行程序

- SDK會自動生成對應的系統日誌文件，存放路徑為該程序同級目錄中，日誌文件命名格式為::

    RoboMasterSDK_YYYYMMDDHHMMSS_log.txt

- 將生成的系統日誌文件發送到郵箱 `developer@dji.com`，郵件模板如下::

    xxxxxxxx
    xxxxxxxx
    xxxxxxxx

**示例代碼**

- 參考sdk代碼 :file:`/examples/01_robot/00_logger.py` 目錄下的例程

.. literalinclude:: ./../../../examples/01_robot/00_logger.py
   :language: python
   :linenos:
   :lines: 16-

- 運行程序後SDK會在在程序的同級目錄下會自動生成系統日誌文件,如下圖所示

	.. image:: ./../images/log_file.png
            :scale: 100%
            :align: center
