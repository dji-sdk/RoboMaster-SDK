#!/usr/bin/env bash
set -ex

OPENCV_VERSION=4.1.2
cd ~
mkdir -p opencv && pushd opencv

wget -O "opencv-${OPENCV_VERSION}.tar.gz" "https://github.com/opencv/opencv/archive/${OPENCV_VERSION}.tar.gz"
wget -O "opencv_contrib-${OPENCV_VERSION}.tar.gz" "https://github.com/opencv/opencv_contrib/archive/${OPENCV_VERSION}.tar.gz"
tar -xvf "opencv-${OPENCV_VERSION}.tar.gz"
tar -xvf "opencv_contrib-${OPENCV_VERSION}.tar.gz"
popd
