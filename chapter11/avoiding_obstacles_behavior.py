from robot import Robot, NoDistanceRead
from time import sleep

class ObstacleAvoidingBehavior(object):
    def __init__(self, the_robot, forward_speed=60, cornering=-60):
        self.robot = the_robot
        self.forward_speed = forward_speed
        self.cornering = cornering

        led_half = int(self.robot.leds.leds_count/2)
        self.max_distance = 100
        self.leds_per_distance = led_half / float(self.max_distance)
        print("Leds per distance", self.leds_per_distance)
        self.sense_colour = (255, 0, 0)

        self.threshold = 15 # Turn at 15 cm

    def display_state(self, left_distance, right_distance):
        # Clear first
        self.robot.leds.clear()
        # Right side 
        # Invert so closer means more LED's. 
        inverted = self.max_distance - min(right_distance, self.max_distance)
        led_count = int(round(inverted * self.leds_per_distance))
        print("Left led count", led_count, inverted)
        self.robot.leds.set_range(range(led_count), self.sense_colour)
        # Left side
        # Invert again
        inverted = self.max_distance - min(left_distance, self.max_distance)
        led_count = int(round(inverted * self.leds_per_distance))
        print("Right led count", led_count, inverted)
        # Bit trickier - must go from below the leds count, to the leds count.
        start = self.robot.leds.leds_count - led_count
        self.robot.leds.set_range(range(start, self.robot.leds.leds_count), self.sense_colour)

        # Now show this display
        self.robot.leds.show()

    def run(self):
        # Drive forward
        self.robot.set_left(self.forward_speed)
        self.robot.set_right(self.forward_speed)
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
            print("Distances: l", left_distance, "r", right_distance)
            # Display this
            self.display_state(left_distance, right_distance)

            # Favour turning right, check the left sensor first
            if left_distance < self.threshold:
                self.robot.set_right(self.cornering)
            # Now turning left if the right sensor is under the threshold
            elif right_distance < self.threshold:
                self.robot.set_left(self.cornering)
            # Otherwise we go forward
            else:
                self.robot.set_left(self.forward_speed)
                self.robot.set_right(self.forward_speed)
            # Wait a little
            sleep(0.1)

bot = Robot()
behavior = ObstacleAvoidingBehavior(bot)
behavior.run()
