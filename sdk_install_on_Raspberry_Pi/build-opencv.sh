#!/usr/bin/env bash
set -ex

OPENCV_VERSION=4.1.2
pushd ~/opencv/opencv-$OPENCV_VERSION
mkdir -p build
pushd build
MEM="$(free -m | awk /Mem:/'{print $2}')"  # Total memory in MB
# RPI 4 with 4GB RAM is actually 3906MB RAM after factoring in GPU RAM split.
# We're probably good to go with `-j $(nproc)` with 3GB or more RAM.
if [[ $MEM -ge 3000 ]]; then
  NUM_JOBS=$(nproc)
else
  NUM_JOBS=1 # Earlier versions of the Pi don't have sufficient RAM to support compiling with multiple jobs.
fi

# -D ENABLE_PRECOMPILED_HEADERS=OFF
# is a fix for https://github.com/opencv/opencv/issues/14868

# -D OPENCV_EXTRA_EXE_LINKER_FLAGS=-latomic
# is a fix for https://github.com/opencv/opencv/issues/15192

cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-$OPENCV_VERSION/modules \
      -D OPENCV_ENABLE_NONFREE=ON \
      -D BUILD_PERF_TESTS=OFF \
      -D BUILD_TESTS=OFF \
      -D BUILD_EXAMPLES=OFF \
      -D ENABLE_PRECOMPILED_HEADERS=OFF \
      -D WITH_TBB=OFF \
      -D ENABLE_NEON=ON \
      -D OPENCV_GENERATE_PKGCONFIG=YES \
      -D OPENCV_EXTRA_EXE_LINKER_FLAGS=-latomic \
      -D PYTHON3_EXECUTABLE=$(which python3) \
      ..
make -j "$NUM_JOBS"
popd; popd
