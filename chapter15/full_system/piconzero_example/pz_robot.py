import piconzero as pz

import atexit

class Robot(object):
    def __init__(self):
        pz.init()
        atexit.register(self.stop_motors)
        
    def stop_motors(self):
        pz.stop()

    def convert_speed(self, speed):
            return (speed * 127) // 100

    def set_left(self, speed):
        pz.setMotor(0, self.convert_speed(speed))

    def set_right(self, speed):
        pz.setMotor(1, self.convert_speed(speed))
