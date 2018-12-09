# Move and Turn

The code in this directory is the starting point for making a moving robot.
It is designed to work with the "Full Function Stepper Motor Hat", a robotics board with support for DC motors, Stepper Motors, Servo motors which also has long passthrough header pins for easy access to all GPIO pins on the Raspberry Pi.

First you will require the following installation on your Pi:

    pi@myrobot:~ $ sudo apt-get install -y git python-pip python-smbus i2ctools
    pi@myrobot:~ $ pip install git+https://github.com/orionrobots/Raspi_MotorHAT

You will need to use Raspi Config to enable i2c and SPI.

Run the test_ or behavior_ files to demonstrate your robot moving.

