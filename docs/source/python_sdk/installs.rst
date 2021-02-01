.. _installs:

#############################
RoboMaster SDK 安裝
#############################




安裝 SDK 到 Windows平台
-------------------------

開發環境準備
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip:: 在使用python sdk前，需要確保編程平台端安裝對應的python環境，如果沒有，請參考以下鏈接進行安裝： :doc:`python編程環境安裝 <./../code_env_setup>`

安裝必要的VC庫環境
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

下載（`下載地址：GitHub RoboMaster SDK repository <https://github.com/dji-sdk/robomaster-sdk>`_ , `備用地址：Gitee RoboMaster SDK repository <https://gitee.com/xitinglin/RoboMaster-SDK>`_）安裝VC庫的exe可執行文件：

.. image:: ./../images/vc_exe.png

.. warning:: 不安裝VC庫，使用SDK，會引起以下問題:

	.. image:: ./../images/libmedia_err.png

安裝robomaster python sdk
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

安裝RoboMaster SDK，點開開始菜單，在搜索框中輸入 ``cmd`` ，在搜索結果中，對著命令提示符程序，單擊鼠標右鍵，菜單中點擊選擇 ``以管理員身份運行`` ,並輸入以下指令::

    pip install robomaster

.. tip:: 如果出現下列情況，請參考以下鏈接進行python環境安裝：:doc:`python編程環境安裝 <./../code_env_setup>`

	.. image:: ./../images/pip_install_error.jpg

升級 RoboMaster SDK
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

當需要升級 RoboMaster SDK時，可在命令行中輸入以下指令::

    pip install --upgrade robomaster



安裝 SDK 到 Linux平台
----------------------


Ubuntu 16.04



Python 環境安裝


介紹 Ubuntu 16.04 的Python環境安裝。


安裝 RoboMaster SDK


安裝 RoboMaster SDK，可輸入以下指令::

    pip install robomaster



升級 RoboMaster SDK


當需要升級 RoboMaster SDK時，可在命令行中輸入以下指令::

    pip install --upgrade robomaster

.. tip:: 樹莓派下的python sdk安裝教程可參考 `sdk install on Raspberry Pi.7z <https://github.com/dji-sdk/robomaster-sdk>`_

安裝 SDK 到 macOS X平台
---------------------------


安裝 RoboMaster SDK


安裝RoboMaster SDK，可輸入以下指令::

    pip install robomaster


升級 RoboMaster SDK


當需要升級 RoboMaster SDK時，可在命令行中輸入以下指令::

    pip install --upgrade robomaster

