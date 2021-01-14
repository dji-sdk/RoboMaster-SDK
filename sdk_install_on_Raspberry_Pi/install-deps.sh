#!/usr/bin/env bash
set -ex

sudo apt-get purge -y libreoffice*
sudo apt-get clean
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get dist-upgrade -y
sudo apt-get autoremove -y
# For some reason I couldn't install libgtk2.0-dev or libgtk-3-dev without running the 
# following line
# See https://www.raspberrypi.org/forums/viewtopic.php?p=1254646#p1254665 for issue and resolution
sudo apt-get install -y devscripts debhelper cmake libldap2-dev libgtkmm-3.0-dev libarchive-dev \
                        libcurl4-openssl-dev intltool
sudo apt-get install -y build-essential cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev \
                        libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
                        libxvidcore-dev libx264-dev libgtk2.0-dev libgtk-3-dev \
                        libatlas-base-dev libblas-dev libeigen{2,3}-dev liblapack-dev \
                        gfortran \
                        python3-dev python3-pip python3
sudo pip3 install -U pip
sudo pip3 install numpy