# Overview

This code is intended to run on a Raspberry Pi on A robot running Raspbian (currently stretch).

# Setup

Start by performing:
    
    sudo apt-get update && sudo apt-get upgrade -y

The following Raspbian packages should be present:

    sudo apt-get install -y git python-pip python-smbus i2ctools

* python-opencv
* opencv-data
* picamera

In Raspi Config enable:

* I2c
* SPI
* Camera

For python the following packages should be installed with pip

    pip install
git+https://github.com/orionrobots/Raspi_MotorHAT
    pip install flask gpiozero spidev
