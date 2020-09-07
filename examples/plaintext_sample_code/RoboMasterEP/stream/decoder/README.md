# Description:

h264 decoder and opus decoder source code， can be compiled into a library
that can be invoked by python 3.x

# Dir tree:
.
├── ubuntu									  # ubuntu decoder
│   ├── build.sh								# build decoder script
│   ├── output								  # decodet output
│   └── src										 # dedocer source code
│       ├── CMakeLists.txt
│       ├── h264_decoder				# video h264 decoder
│       ├── opus_decoder				# audio opus decoder
│       └── pybind11
└── windows									# windows decoder
    ├── libh264decoder					# video h264 decoder
    │   ├── libh264decoder-0.0.1-cp36-cp36m-win_amd64.whl	# video h264 decoder, win64 bit python 3.6
    │   ├── libh264decoder-0.0.1-cp37-cp37m-win_amd64.whl	# video h264 decoder, win64 bit python 3.7
    │   ├── libh264decoder-0.0.1-cp38-cp38-win_amd64.whl	    # video h264 decoder, win64 bit python 3.8
    │   └── libh264decoder-0.0.1.tar.gz											  # video h264 decoder source file
    └── opus_decoder						# audio opus decoder
        ├── opus_decoder-0.0.1-cp36-cp36m-win_amd64.whl		# audio opus decoder, win64 bit python 3.6
        ├── opus_decoder-0.0.1-cp37-cp37m-win_amd64.whl		# audio opus decoder, win64 bit python 3.7
        ├── opus_decoder-0.0.1-cp38-cp38-win_amd64.whl	    	# audio opus decoder, win64 bit python 3.8
        └── opus_decoder-0.0.1.tar.gz												  # audio opus decoder source file

# Ubuntu environment:

## Dependent toolchian and library:

- libopus-dev, libavcodec-dev, libswscale-dev
- cmake (>= 3.4.1)

## Installation ( ubuntu ):

1. $ sudo apt-get install libopus-dev libavcodec-dev libswscale-dev
2. $ sudo apt-get install cmake
3. $ chmod +x ./build.sh
4. $ ./build.sh

## Output:

Output h264 decoder and opus decoder in ./output

## NOTE:

If you want to use the library in python2.x, please modify the CMakeLists.txt
as follows:

    set(PYBIND11_PYTHON_VERSION 3)  --->  set(PYBIND11_PYTHON_VERSION 2)

And build.

# Windows environment:

## Requirement:

- Windows 64 bit compute
- Install python 3.6, 3.7 and 3.8 version

## Installation ( windows ):

python 3.6 for example
- pip install libh264decoder-0.0.1-cp36-cp36m-win_amd64.whl
- pip install opus_decoder-0.0.1-cp36-cp36m-win_amd64.whl