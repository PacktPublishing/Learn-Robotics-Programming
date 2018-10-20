from __future__ import print_function
import time

from image_app_core import start_server_process, get_control_instruction, put_output_image

import cv2
import numpy as np

import pi_camera_stream
from pid_controller import PIController
from robot import Robot


def get_largest_enclosing(masked_image):
    """Find the largest enclosing circle for all contours in a masked image"""
    # Find the contours of the image (outline points)
    contour_image = np.copy(masked_image)
    contours, _ = cv2.findContours(contour_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # Find enclosing circles
    circles = [cv2.minEnclosingCircle(cnt) for cnt in contours]
    # Filter for the largest one
    largest = (0, 0), 0
    for (x, y), radius in circles:
        if radius > largest[1]:
            largest = (int(x), int(y)), int(radius)
    return largest

class ColorTrackingBehavior(object):
    """This will identify a colored objects.
    It takes a video stream and produces:
    * A video feed of images - frames showing the original and transformed next to it.
    * x,y coordinates of the largest object.
    * radius of the enclosing circle of the largest object.
    It will draw the circle, and show the numbers in the image frame if prompted.
    """
    def __init__(self, robot):
        self.low_range = (25, 70, 25)
        self.high_range = (80, 255, 255)
        self.correct_radius = 120
        self.center = 160
        self.robot = robot
        # Current state
        self.running = False

    def process_stream(self, image_stream):
        for frame in image_stream:
            # Convert to HSV
            frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # Mask for a green object
            masked = cv2.inRange(frame_hsv, self.low_range, self.high_range)
            # Find the largest enclosing circle
            coordinates, radius = get_largest_enclosing(masked)
            # Now back to 3 channels to render it
            processed = cv2.cvtColor(masked, cv2.COLOR_GRAY2BGR)
            # Draw our circle on the original frame to tag this object
            cv2.circle(frame, coordinates, radius, [255, 0, 0])
            # Then make the dualscreen view - two images of the same scale concatenated
            self.make_display(np.concatenate((frame, processed), axis=1))
            # But what we yield are the object details - coordinates and radius
            yield coordinates, radius

    def process_control(self):
        instruction = get_control_instruction()
        if instruction == "start":
            self.running = True
        elif instruction == "stop":
            self.running = False
        if instruction == "exit":
            print("Stopping")
            exit()

    def run(self):
        # Set pan and tilt to middle, then clear it.
        self.robot.set_pan(0)
        self.robot.set_tilt(0)
        # allow the camera to warmup and start the stream
        camera = pi_camera_stream.setup_camera()
        # Set up two PID controllers
        # speed is a proportional pid - based on the radius we get.
        speed_pid = PIController(proportional_constant=0.8, integral_constant=0.1, windup_limit=100)
        # we then have a direction pid - how far from the middle X is. Beware integral windup here
        direction_pid = PIController(proportional_constant=0.6, integral_constant=0.1,
            windup_limit=400)
        time.sleep(0.1)
        # Servo's will be in place - stop them for now.
        self.robot.servos.stop_all()
        
        print("Setup Complete")
        input_stream = pi_camera_stream.start_stream(camera)
        # Start actually tracking the object
        data_stream = self.process_stream(input_stream)
        # left is X - value, right is x + value
        # add the base speed to the directional outputs for the two motors
        for (x, y), radius in data_stream:
            self.process_control()
            if self.running and radius > 20:
                # calculate the first error
                radius_error = max(-80, min(self.correct_radius - radius, 80)) # up to +-80% speed
                speed_value = speed_pid.get_value(radius_error)
                # And the second error is the based on the center coordinate.
                direction_error = max(-40, min(self.center - x, 40)) # up to +-40 degree deflection
                # direction_error = self.center - x
                direction_value = direction_pid.get_value(direction_error)
                print("radius: %d, radius_error: %d, speed_value: %.2f, direction_error: %d, direction_value: %.2f" %
                    (radius, radius_error, speed_value, direction_error, direction_value))
                # Now produce left and right motor speeds
                self.robot.set_left(speed_value - direction_value)
                self.robot.set_right(speed_value + direction_value)
            else:
                self.robot.stop_motors()
                if not self.running:
                    speed_pid.reset()
                    direction_pid.reset()

    def make_display(self, display_frame):
        """Create display output, and put it on the queue, if it is empty"""
        encoded_bytes = pi_camera_stream.get_encoded_bytes_for_frame(display_frame)
        put_output_image(encoded_bytes)

print("Setting up")
behavior = ColorTrackingBehavior(Robot())
process = start_server_process('color_track_server.html')
try:
    behavior.run()
finally:
    process.terminate()
