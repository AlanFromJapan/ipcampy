#!/bin/bash

#get python an pip
sudo apt-get install python3-setuptools python3-pip --yes

#are you on Raspberry Pi? if yes then install the below
#doc https://tutorials-raspberrypi.com/installing-opencv-on-the-raspberry-pi/
sudo apt-get install build-essential git cmake pkg-config libjpeg-dev libtiff-dev libjasper-dev  libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libgtk2.0-dev libatlas-base-dev gfortran --yes


#get flask
sudo python3 -m pip install Flask

#opencv for python
#on raspi this step will take TIME like easily 1h so don't wait
pip install opencv-python
