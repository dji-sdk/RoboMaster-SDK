# Description:

h264 decoder and opus decoder source code， can be compiled into a library
that can be invoked by python 3.x

# Dir tree:
. 
├── build.sh                # build decoder script
├── output                  # decodet output
└── src                     # dedocer source code
    ├── cmake
    ├── CMakeLists.txt
    ├── h264_decoder        # video h264 decoder
    ├── opus_decoder        # audio opus decoder
    └── pybind11


# Dependent toolchian and library:
    
- libopus-dev, libavcodec-dev, libswscale-dev
- cmake (>= 3.4.1)

# Installation(ubuntu):
    
1. $ sudo apt-get install libopus-dev libavcodec-dev libswscale-dev
2. $ sudo apt-get install cmake
3. $ chmod +x ./build.sh
4. $ ./build.sh

# Output:
    
Output h264 decoder and opus decoder in ./output

# NOTE:
    
If you want to use the library in python2.x, please modify the CMakeLists.txt
as follows:

    set(PYBIND11_PYTHON_VERSION 3)  --->  set(PYBIND11_PYTHON_VERSION 2)

And build.
