from Raspi_MotorHAT import Raspi_MotorHAT

import atexit

class Robot(object):
    def __init__(self, motorhat_addr=0x6f):
        self._mh = Raspi_MotorHAT(addr=motorhat_addr)

        self._lm = self._mh.getMotor(1)
        self._rm = self._mh.getMotor(2)
        atexit.register(self.stop_motors)

    def convert_speed(self, speed):
        return (abs(speed) * 255) / 100

    def set_left(self, speed):
        mode = Raspi_MotorHAT.RELEASE
        if speed > 0:
            mode = Raspi_MotorHAT.FORWARD
        elif speed < 0:
            mode = Raspi_MotorHAT.BACKWARD
        self._lm.setSpeed(self.convert_speed(speed))
        self._lm.run(mode)

    def set_right(self, speed):
        mode = Raspi_MotorHAT.RELEASE
        if speed > 0:
            mode = Raspi_MotorHAT.FORWARD
        elif speed < 0:
            mode = Raspi_MotorHAT.BACKWARD
        self._rm.setSpeed(self.convert_speed(speed))
        self._rm.run(mode)
        
    def stop_motors(self):
        self._lm.run(Raspi_MotorHAT.RELEASE)
        self._rm.run(Raspi_MotorHAT.RELEASE)
