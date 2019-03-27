# Setup

Currently GPIOZero release 1.4.1 does not have the pull_up=True option for the LineSensor object.
When 1.5 is available, this will be present.
Until then the master branch can be used, on the Pi type:

    pi@myrobot:~ $ pip install git+https://github.com/RPi-Distro/python-gpiozero.git

If you use gpiozero 1.4.1, you are likely to see errors about the pull_up argument not existing.
