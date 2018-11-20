from Raspi_MotorHAT import Raspi_MotorHAT
from gpiozero import LineSensor
import RPi.GPIO as GPIO

import atexit

#import leds_led_shim
import leds_8_apa102c
from servos import Servos
from distance_sensor_hcsr04 import DistanceSensor, NoDistanceRead
from encoder_counter import EncoderCounter

class Robot(object):
    wheel_diameter_mm = 69.0
    ticks_per_revolution = 40.0
    wheel_distance_mm =  131.0

    def __init__(self, motorhat_addr=0x6f, drive_enabled=True):
        # Setup the motorhat with the passed in address
        self._mh = Raspi_MotorHAT(addr=motorhat_addr)

        # get local variable for each motor
        self.left_motor = self._mh.getMotor(1)
        self.right_motor = self._mh.getMotor(2)
        self.drive_enabled = drive_enabled

        # ensure the motors get stopped when the code exits
        atexit.register(self.stop_all)

        # Setup the line sensors
        self.left_line_sensor = LineSensor(23, queue_len=3, pull_up=True)
        self.right_line_sensor = LineSensor(16, queue_len=3, pull_up=True)

        # Setup The Distance Sensors
        self.left_distance_sensor = DistanceSensor(17, 27)
        self.right_distance_sensor = DistanceSensor(5, 6)

        # Setup the Encoders
        EncoderCounter.set_constants(self.wheel_diameter_mm, self.ticks_per_revolution)
        self.left_encoder = EncoderCounter(4)
        self.right_encoder = EncoderCounter(26)

        # Setup the Leds
        self.leds = leds_8_apa102c.Leds()

        # Set up servo motors for pan and tilt.
        self.servos = Servos(addr=motorhat_addr)
    
    def stop_all(self):
        self.stop_motors()

        # Clear any sensor handlers
        self.left_line_sensor.when_line = None
        self.left_line_sensor.when_no_line = None
        self.right_line_sensor.when_line = None
        self.right_line_sensor.when_no_line = None

        # Clear the display
        self.leds.clear()
        self.leds.show()

        # Reset the servos
        self.servos.stop_all()

    def convert_speed(self, speed):
        mode = Raspi_MotorHAT.RELEASE
        if speed > 0:
            mode = Raspi_MotorHAT.FORWARD
        elif speed < 0:
            mode = Raspi_MotorHAT.BACKWARD
        output_speed = (abs(speed) * 255) / 100
        return mode, int(output_speed)

    def set_left(self, speed):
        if not self.drive_enabled:
            return
        mode, output_speed = self.convert_speed(speed)
        self.left_motor.setSpeed(int(output_speed))
        self.left_motor.run(mode)

    def set_right(self, speed):
        if not self.drive_enabled:
            return
        mode, output_speed = self.convert_speed(speed)
        self.right_motor.setSpeed(int(output_speed))
        self.right_motor.run(mode)
        
    def stop_motors(self):
        self.left_motor.run(Raspi_MotorHAT.RELEASE)
        self.right_motor.run(Raspi_MotorHAT.RELEASE)

    def set_pan(self, angle):
        self.servos.set_servo_angle(1, angle)
    
    def set_tilt(self, angle):
        self.servos.set_servo_angle(0, angle)
