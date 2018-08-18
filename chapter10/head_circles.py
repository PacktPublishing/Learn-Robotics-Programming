from time import sleep
import math

from robot import Robot

class CirclePanTiltBehavior(object):
    def __init__(self, the_robot):
        self.robot = the_robot
        self.current_time = 0
        self.radians_per_frame = (2 * math.pi) / 50.0

    def run(self):
        while True:
            frame = self.current_time % 50
            frame_in_radians = frame * self.radians_per_frame
            self.robot.set_pan(30 * math.cos(frame_in_radians))
            self.robot.set_tilt(30 * math.sin(frame_in_radians))
            sleep(0.05)
            self.current_time += 1


bot = Robot()
behavior = CirclePanTiltBehavior(bot)
behavior.run()
