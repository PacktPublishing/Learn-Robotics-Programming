from Raspi_MotorHAT.Raspi_PWM_Servo_Driver import PWM
from robot import Robot
import atexit
import time

r = Robot()
pwm = PWM(0x6f)

servo_min = 150         # Servo minimum position.
servo_max = 600         # Maximum position
servo_mid = 225 + 150   # Middle position

def stop():
    pwm.setPWM(0, 0, 0)

atexit.register(stop)
pwm.setPWMFreq(60)      # Set frequency to 60 Hz

while (True):
    r.set_left(255)
    r.set_right(255)
    print("min")
    pwm.setPWM(0, 0, servo_min)
    time.sleep(1)
    print("max")
    pwm.setPWM(0, 0, servo_max)
    time.sleep(1)
    r.stop_motors()
    print("mid")
    pwm.setPWM(0, 0, servo_mid)
    time.sleep(1)