# Overview

This code is intended to run on a Raspberry Pi on A robot running Raspbian (currently stretch).

# Setup

Start by performing:
    
    pi@myrobot:~ $ sudo apt-get update && sudo apt-get upgrade -y

The following Raspbian packages should be present:

    pi@myrobot:~ $ sudo apt-get install -y git python-pip python-smbus i2ctools

* python-opencv
* opencv-data
* picamera

In Raspi Config enable:

* I2c
* SPI
* Camera

For python the following packages should be installed with pip

    pi@myrobot:~ $ pip install
git+https://github.com/orionrobots/Raspi_MotorHAT
    pi@myrobot:~ $ pip install flask gpiozero spidev
