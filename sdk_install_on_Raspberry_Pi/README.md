Install OpenCV 4.1.2 on Raspbian Buster

```bash
$ chmod +x *.sh
$ ./download-opencv.sh
$ ./install-deps.sh
$ ./build-opencv.sh
$ cd ~/opencv/opencv-4.1.2/build
$ sudo make install
```

**WARNING: Users of boards with 1GB of memory**

Compiling is very memory intensive, you will likely need to increase your swap size. Assuming you have a reasonably large SD card (>16GB to be safe), follow the procedure below to increase your swap size from the default 100MB to 2GB

```bash
$ sudo dphys-swapfile swapoff
$ sudo sed -i 's:CONF_SWAPSIZE=.*:CONF_SWAPSIZE=2048:g' /etc/dphys-swapfile
$ sudo reboot
```
