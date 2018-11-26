from robot import Robot
from time import sleep

cross_line_color = (255, 0, 0)
off_line_color = (0, 0, 255)

class LineFollowingBehavior:
    # Note - this is the robot ON the line. 
    def __init__(self, the_robot, forward_speed=30, cornering=-30):
        self.robot = the_robot
        self.forward_speed = forward_speed
        self.cornering = cornering

        led_qtr = int(self.robot.leds.count/4)
        self.right_indicator = list(range(0, led_qtr))
        self.left_indicator = list(range(self.robot.leds.count - led_qtr, self.robot.leds.count))

        self.robot.leds.show()

    def when_left_crosses_line(self):
        self.robot.set_left(self.cornering)
        self.robot.leds.set_range(self.left_indicator, cross_line_color)
        self.robot.leds.show()

    def when_right_crosses_line(self):
        self.robot.set_right(self.cornering)
        self.robot.leds.set_range(self.right_indicator, cross_line_color)
        self.robot.leds.show()

    def when_left_off_line(self):
        self.robot.set_left(self.forward_speed)
        self.robot.leds.set_range(self.left_indicator, off_line_color)
        self.robot.leds.show()

    def when_right_off_line(self):
        self.robot.set_right(self.forward_speed)
        self.robot.leds.set_range(self.right_indicator, off_line_color)
        self.robot.leds.show()

    def run(self):
        # Setup conditions
        self.robot.left_line_sensor.when_line = self.when_left_crosses_line
        self.robot.left_line_sensor.when_no_line = self.when_left_off_line
        self.robot.right_line_sensor.when_line = self.when_right_crosses_line
        self.robot.right_line_sensor.when_no_line = self.when_right_off_line
        # Start driving
        self.robot.set_left(self.forward_speed)
        self.robot.set_right(self.forward_speed)
        while True:
            sleep(0.02)


bot = Robot()
behavior = LineFollowingBehavior(bot)
behavior.run()

