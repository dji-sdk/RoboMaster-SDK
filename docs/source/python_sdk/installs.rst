.. _installs:

#############################
Install RoboMaster SDK
#############################




Install the SDK on the Windows platform
-----------------------------------------

Prepare the development environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip:: Before using the Python SDK, ensure that the corresponding Python environment has been installed on the programming platform. If the environment is not installed, install it by referring to :doc:`Install the Python Programming Environment<./../code_env_setup>`.

Install the required VC library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Download the (`GitHub RoboMaster SDK repository  <https://github.com/dji-sdk/robomaster-sdk>`_) (`Alternative download address: Gitee RoboMaster SDK repository  <https://gitee.com/xitinglin/RoboMaster-SDK>`_) and run the executable file of the VC library:

.. image:: ./../images/vc_exe.png

.. warning:: The following error occurs if you use the SDK without installing the VC library:

	.. image:: ./../images/libmedia_err.png

Install the RoboMaster Python SDK
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install the RoboMaster SDK, click the start menu on your PC, and enter ``cmd`` in the search box. In the search results, right-click the CLI program and select ``Run as Administrator''. Then, enter the following command:::

    pip install robomaster

.. tip:: If the following error occurs, install the Python environment by referring to :doc:`Install the Python Programming Environment<./../code_env_setup>`.

	.. image:: ./../images/pip_install_error.jpg

Upgrade the RoboMaster SDK
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To upgrade the RoboMaster SDK, run the following command on the CLI:::

    pip install --upgrade robomaster



Install the SDK on the Linux platform
----------------------


Ubuntu 16.04



Install the Python environment


The following example explains how to install the Python environment in Ubuntu 16.04.


Install the RoboMaster SDK


Install the RoboMaster SDK by running the following command:::

    pip install robomaster



Upgrade the RoboMaster SDK


To upgrade the RoboMaster SDK, run the following command on the CLI:::

    pip install --upgrade robomaster

.. tip:: For the process of installing the Python environment on Raspberry Pi, refer to `sdk install on Raspberry Pi.7z  <https://github.com/dji-sdk/robomaster-sdk>`_.

Install the SDK on the MacOS X platform
---------------------------------------------


Install the RoboMaster SDK


Install RoboMaster SDK by running the following command:::

    pip install robomaster


Upgrade the RoboMaster SDK


To upgrade the RoboMaster SDK, run the following command on the CLI:::

    pip install --upgrade robomaster

