from __future__ import print_function
from robot import Robot, NoDistanceRead
from time import sleep


class ObstacleAvoidingBehavior(object):
    """Simple obstacle avoiding"""
    def __init__(self, the_robot):
        self.robot = the_robot
        
        # Calculations for the LEDs
        led_half = int(self.robot.leds.count/2)
        self.max_distance = 100
        self.leds_per_distance = led_half / float(self.max_distance)
        # print("Leds per distance", self.leds_per_distance)
        self.sense_colour = (255, 0, 0)

    def distance_to_led_bar(self, distance):
        # Invert so closer means more LED's. 
        inverted = self.max_distance - min(distance, self.max_distance)
        led_bar = int(round(inverted * self.leds_per_distance))
        return led_bar

    def display_state(self, left_distance, right_distance):
        # Clear first
        self.robot.leds.clear()
        # Right side
        led_bar = self.distance_to_led_bar(right_distance)
        self.robot.leds.set_range(range(led_bar), self.sense_colour)
        # Left side
        led_bar = self.distance_to_led_bar(left_distance)
        # Bit trickier - must go from below the leds count, to the leds count.
        start = self.robot.leds.count - led_bar
        self.robot.leds.set_range(range(start, self.robot.leds.count), self.sense_colour)

        # Now show this display
        self.robot.leds.show()

    def get_motor_speed(self, distance):
        """This method chooses a speed for a motor based on the distance from it's sensor"""
        if distance < 20:
            return -100
        else:
            return 100

    def run(self):
        self.robot.set_pan(0)
        self.robot.set_tilt(0)
        while True:
            # Get the sensor readings
            try:
                left_distance = self.robot.left_distance_sensor.get_distance()
            except NoDistanceRead:
                left_distance = 100
            try:
                right_distance = self.robot.right_distance_sensor.get_distance()
            except NoDistanceRead:
                right_distance = 100
            # Display this
            self.display_state(left_distance, right_distance)

            # Get speeds for motors from distances
            print("Distances: l", left_distance, "r", right_distance)
            self.robot.set_left(self.get_motor_speed(left_distance))
            self.robot.set_right(self.get_motor_speed(right_distance))

            # Wait a little
            sleep(0.1)

bot = Robot()
behavior = ObstacleAvoidingBehavior(bot)
behavior.run()
