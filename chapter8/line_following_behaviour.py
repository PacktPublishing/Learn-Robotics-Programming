from robot import Robot
from time import sleep

class LineFollowerBehavior:
    # Note - this is the robot ON the line. 
    # pip install --upgrade git+https://github.com/RPi-Distro/python-gpiozero.git@linesensor-inverted-652
    max_speed = 30
    cornering = -30

    def __init__(self, the_robot):
        self.robot = the_robot

    def when_left_line(self):
        self.robot.set_right(self.max_speed)
        sleep(0.1)

    def when_right_line(self):
        self.robot.set_left(self.max_speed)
        sleep(0.1)

    def when_left_no_line(self):
        self.robot.set_right(self.cornering)

    def when_right_no_line(self):
        self.robot.set_left(self.cornering)

    def run(self):
        # Setup conditions
        self.robot.left_line_sensor.when_line = self.when_left_line
        self.robot.left_line_sensor.when_no_line = self.when_left_no_line
        self.robot.right_line_sensor.when_line = self.when_right_line
        self.robot.right_line_sensor.when_no_line = self.when_right_no_line
        # Start driving
        self.robot.set_left(self.max_speed)
        self.robot.set_right(self.max_speed)
        while True:
            sleep(0.1)


bot = Robot()
behaviour = LineFollowerBehavior(bot)
behaviour.run()

