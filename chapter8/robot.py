from Raspi_MotorHAT import Raspi_MotorHAT
from gpiozero import LineSensor

import atexit

class Robot(object):
    def __init__(self, motorhat_addr=0x6f):
        # Setup the motorhat with the passed in address
        self._mh = Raspi_MotorHAT(addr=motorhat_addr)

        # get local variable for each motor
        self.left_motor = self._mh.getMotor(1)
        self.right_motor = self._mh.getMotor(2)

        # ensure the motors get stopped when the code exits
        atexit.register(self.stop_all)

        # Setup the line sensors
        self.left_line_sensor = LineSensor(23, queue_len=3, pull_up=True)
        self.right_line_sensor = LineSensor(16, queue_len=3, pull_up=True)

    def stop_all(self):
        self.stop_motors()
        
        # Clear any sensor handlers
        self.left_line_sensor.when_line = None
        self.left_line_sensor.when_no_line = None
        self.right_line_sensor.when_line = None
        self.right_line_sensor.when_no_line = None

    def convert_speed(self, speed):
        mode = Raspi_MotorHAT.RELEASE
        if speed > 0:
            mode = Raspi_MotorHAT.FORWARD
        elif speed < 0:
            mode = Raspi_MotorHAT.BACKWARD
        output_speed = (abs(speed) * 255) / 100
        return mode, int(output_speed)

    def set_left(self, speed):
        mode, output_speed = self.convert_speed(speed)
        self.left_motor.setSpeed(int(output_speed))
        self.left_motor.run(mode)

    def set_right(self, speed):
        mode, output_speed = self.convert_speed(speed)
        self.right_motor.setSpeed(int(output_speed))
        self.right_motor.run(mode)
        
    def stop_motors(self):
        self.left_motor.run(Raspi_MotorHAT.RELEASE)
        self.right_motor.run(Raspi_MotorHAT.RELEASE)
