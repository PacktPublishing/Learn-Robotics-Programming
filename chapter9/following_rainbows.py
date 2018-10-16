from robot import Robot
import colorsys
from time import sleep

class FollowingRainbows:
    # Note - this is the robot ON the line. 
    def __init__(self, the_robot, forward_speed=40, cornering=0):
        self.robot = the_robot
        self.forward_speed = forward_speed
        self.cornering = cornering
        self.left_index = 0
        self.left_brightness = 0
        self.right_index = 0
        self.right_brightness = 0
        self.main_index = 0

        led_qtr = int(self.robot.leds.count/4)
        self.right_indicator = list(range(0, led_qtr))
        self.left_indicator = list(range(self.robot.leds.count - led_qtr, self.robot.leds.count))


    def when_left_crosses_line(self):
        self.robot.set_left(self.cornering)
        self.left_brightness = 1.0

    def when_right_crosses_line(self):
        self.robot.set_right(self.cornering)
        self.right_brightness = 1.0

    def when_left_off_line(self):
        self.robot.set_left(self.forward_speed)

    def when_right_off_line(self):
        self.robot.set_right(self.forward_speed)

    def hsv_to_rgb(self, h, s, v):
        return [int(component*255) for component in colorsys.hsv_to_rgb(h, s, v)]

    def make_display(self):
        # main rainbow
        half_leds = int(self.robot.leds.count/2)
        qtr_leds = int(self.robot.leds.count/4)
        for n in range(0, half_leds):
            offset = (240/half_leds) * n
            ih = (self.main_index + offset) % 360
            ch = self.hsv_to_rgb(ih / 360.0, 1.0, 0.6)
            rgb = [int(c*255) for c in ch]
            self.robot.leds.set_one(qtr_leds + n, rgb)
        self.main_index += 5
        # LEft and right
        for n in range(0, qtr_leds):
            offset = (60/7.0) * n
            lh = (self.left_index + offset) % 360
            ch = self.hsv_to_rgb(lh / 360.0, 1.0, self.left_brightness)
            rgb = [int(c*255) for c in ch]
            self.robot.leds.set_one(n, rgb)
            rh = (self.right_index + offset) % 360
            ch = self.hsv_to_rgb(rh / 360.0, 1.0, self.right_brightness)
            rgb = [int(c*255) for c in ch]
            self.robot.leds.set_one(self.robot.leds.count-1-n, rgb)
        self.left_index += 5
        self.right_index -= 5
        if self.left_brightness >= 0.1:
            self.left_brightness -= 0.1
        if self.right_brightness >= 0.1:
            self.right_brightness -= 0.1
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
            sleep(0.01)
            self.make_display()


bot = Robot()
behavior = FollowingRainbows(bot)
behavior.run()

