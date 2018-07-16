from Raspi_MotorHAT import Raspi_MotorHAT

import time
import atexit

mh = Raspi_MotorHAT(addr=0x6f)
lm = mh.getMotor(1)
rm = mh.getMotor(2)

def turn_off_motors():
        lm.run(Raspi_MotorHAT.RELEASE)
        rm.run(Raspi_MotorHAT.RELEASE)
atexit.register(turn_off_motors)

lm.setSpeed(150)
rm.setSpeed(150)

lm.run(Raspi_MotorHAT.BACKWARD)
rm.run(Raspi_MotorHAT.FORWARD)
time.sleep(1)
