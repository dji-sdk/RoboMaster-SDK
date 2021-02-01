cmake_minimum_required(VERSION 3.4.1)
project (robomaster_video_and_audio_decoder)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_BUILD_TYPE Release)
SET(LIBRARY_OUTPUT_PATH ${CMAKE_SOURCE_DIR}/../output)
list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")
find_package(Opus REQUIRED)

set(PYBIND11_PYTHON_VERSION 3)
set(PYBIND11_CPP_STANDARD -std=c++11)
add_subdirectory(pybind11)
#find_package(pybind11)

pybind11_add_module(opus_decoder opus_decoder/opus_decoder.cpp)
target_link_libraries(opus_decoder PRIVATE ${OPUS_LIBRARIES})
target_include_directories(opus_decoder PRIVATE ${OPUS_INCLUDE_DIRS})

pybind11_add_module(libh264decoder h264_decoder/h264decoder.cpp)
target_link_libraries(libh264decoder PRIVATE avcodec swscale avutil)
