.. _beginnger:

##########################################################
Getting Started with RoboMaster SDK - Basics
##########################################################

What can the SDK do?
_______________________

RoboMaster SDK (hereinafter referred to as the SDK) is a set of development kits for DJI RoboMaster series products.
It currently supports products including RoboMaster EP, RoboMaster EP Core, Tello EDU, and Tello Talent.
By using the SDK, users can control robot movement on the PC and obtain information from the robot sensors. (To be supplemented?)

Your first SDK program
_______________________

This document explains how to obtain the version number of the SDK to write your first SDK program.

- First, import the modules that you need from the installed `robomaster` package. Here, we will import the `version` module that contains SDK version information.::

    from robomaster import version

- Next, obtain the SDK version number from the `__version__` attribute in the `version` module and print the version number.::

    sdk_version = version.__version__
    print("sdk version:", sdk_version)

- Run the program. You will see the printed result::

    sdk version: 0.1.1.29

The :file:`/examples/00_general/01_sdk_version.py` sample document describes the process of obtaining the SDK version number.

.. literalinclude:: ./../../../examples/00_general/01_sdk_version.py
   :language: python
   :linenos:
   :lines: 17-
