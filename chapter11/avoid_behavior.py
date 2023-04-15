from __future__ import print_function
from robot import Robot, NoDistanceRead
from time import sleep


class ObstacleAvoidingBehavior(object):
    """Better obstacle avoiding"""
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

    def get_speeds(self, nearest_distance):
        if nearest_distance > 100:
            nearest_speed = 100
            furthest_speed = 100
            delay = 100
        elif nearest_distance > 50:
            nearest_speed = 100
            furthest_speed = 80
            delay = 100
        elif nearest_distance > 20:
            nearest_speed = 100
            furthest_speed = 60
            delay = 100
        elif nearest_distance > 10:
            nearest_speed = -40
            furthest_speed = -100
            delay = 100
        else: # collison
            nearest_speed = -100
            furthest_speed = -100
            delay = 250
        return nearest_speed, furthest_speed, delay

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
            nearest_speed, furthest_speed, delay = self.get_speeds(min(left_distance, right_distance))
            print("Distances: l", left_distance, "r", right_distance, "Speeds: n", nearest_speed, "f", furthest_speed,
                "Delays: l", delay)

            # Send this to the motors
            if left_distance < right_distance:
                self.robot.set_left(nearest_speed)
                self.robot.set_right(furthest_speed)
            else:
                self.robot.set_right(nearest_speed)
                self.robot.set_left(furthest_speed)

            # Wait our delay time
            sleep(delay * 0.001)

bot = Robot()
behavior = ObstacleAvoidingBehavior(bot)
behavior.run()
