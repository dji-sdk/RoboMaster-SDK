========================
User-defined UI System
========================

A custom UI system allows users to generate custom UI controls by using their own programs to expand the input and output of the programs.

Processing input and output is an important part of our programming work. For our robot, the program output can be actions of the chassis, gimbal, blaster, or other modules, or lighting effects, sound effects, and other effects. The input can be initial variables, visual recognition by the robot, applause recognition, detection of armor plate strikes, and mobile phone gyroscope signals. Now, we can interact with the generated UI controls through a custom UI system to implement input. We can also use the processing results of the program to output information through the UI controls.

We can write Python programs in the RoboMaster app, call related interfaces of the custom UI system to generate UI controls, and bind event callbacks of the controls. After programming and debugging the program in the lab, we can assemble the program into custom skills and release them for single-device driving or multiplayer competition.

For information on the Python API, refer to :doc:`Custom UI System<./custom_ui>`.