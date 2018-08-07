from robot import Robot
from time import sleep
import leds_8_apa102c
# import leds_led_shim

class LineFollowingBehavior:
    # Note - this is the robot ON the line. 
    def __init__(self, the_robot, forward_speed=30, cornering=-30):
        self.robot = the_robot
        self.forward_speed = forward_speed
        self.cornering = cornering

        led_qtr = int(self.robot.leds.leds_count/4)
        self.left_indicator = range(0, led_qtr)
        self.right_indicator = range(self.robot.leds.leds_count - led_qtr, self.robot.leds.leds_count)

    def when_left_crosses_line(self):
        self.robot.set_left(self.cornering)
        self.robot.leds.set_range(self.left_indicator, (255, 0, 0))
        self.robot.leds.show()

    def when_right_crosses_line(self):
        self.robot.set_right(self.cornering)
        self.robot.leds.set_range(self.right_indicator, (255, 0, 0))
        self.robot.leds.show()

    def when_left_off_line(self):
        self.robot.set_left(self.forward_speed)
        self.robot.leds.set_range(self.left_indicator, (0, 0, 255))
        self.robot.leds.show()

    def when_right_off_line(self):
        self.robot.set_right(self.forward_speed)
        self.robot.leds.set_range(self.right_indicator, (0, 0, 255))
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


bot = Robot(leds_8_apa102c.Leds())
behavior = LineFollowingBehavior(bot)
behavior.run()

