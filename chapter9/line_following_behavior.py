from robot import Robot
from time import sleep
import colorsys

cross_line_color = (255, 0, 0)
off_line_color = (0, 0, 255)

class LineFollowingBehavior:
    # Note - this is the robot ON the line. 
    def __init__(self, the_robot, forward_speed=30, cornering=-30):
        self.robot = the_robot
        self.forward_speed = forward_speed
        self.cornering = cornering

        led_qtr = int(self.robot.leds.leds_count/4)
        self.right_indicator = range(0, led_qtr)
        self.left_indicator = range(self.robot.leds.leds_count - led_qtr, self.robot.leds.leds_count)

        led_half = int(self.robot.leds.leds_count/2)
        hue_step = 0.9 / led_half

        for n in range(led_half):
            led_index = led_qtr + n
            hue = 0.1 + (hue_step * n)
            print(hue)
            rgb = colorsys.hsv_to_rgb(hue, 1.0, 0.6)
            rgb = [int(c*255) for c in rgb]
            self.robot.leds.set_one(led_index, rgb)
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

