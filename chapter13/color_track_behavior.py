from __future__ import print_function
import time
from multiprocessing import Process, Queue

from flask import Flask, render_template, Response
import cv2
import numpy as np

import pi_camera_stream
from pid_controller import PIController
from robot import Robot


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
        self.output_queue = Queue(maxsize=1)
        self.control_queue = Queue()
        # Current state
        self.running = False

    def process_stream(self, image_stream):
        for frame in image_stream:
            # Convert to HSV
            frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # Mask for a green object
            masked = cv2.inRange(frame_hsv, self.low_range, self.high_range)
            # Find the largest enclosing circle
            coordinates, radius = pi_camera_stream.get_largest_enclosing(masked)
            # Now back to 3 channels to render it
            processed = cv2.cvtColor(masked, cv2.COLOR_GRAY2BGR)
            # Draw our circle on the original frame to tag this object
            cv2.circle(frame, coordinates, radius, [255, 0, 0])
            # Then make the dualscreen view - two images of the same scale concatenated
            self.make_display(np.concatenate((frame, processed), axis=1))
            # BUt what we yield are the object details - coordinates and radius
            yield coordinates, radius

    def process_control(self):
        if self.control_queue.empty():
            # nothing
            return
        instruction = self.control_queue.get_nowait()
        if instruction == "START":
            self.running = True
        elif instruction == "STOP":
            self.running = False

    def run(self):
        # allow the camera to warmup and start the stream
        camera = pi_camera_stream.setup_camera()
        # Set up two PID controllers
        # speed is a proportional pid - based on the radius we get.
        speed_pid = PIController(proportional_constant=0.8, integral_constant=0.1, windup_limit=100)
        # we then have a direction pid - how far from the middle X is. Beware integral windup here
        direction_pid = PIController(proportional_constant=0.4, integral_constant=0.1,
            windup_limit=120)
        time.sleep(0.1)
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
                bot.set_left(speed_value - direction_value)
                bot.set_right(speed_value + direction_value)
            else:
                bot.stop_motors()
                if not self.running:
                    speed_pid.reset()
                    direction_pid.reset()

    def make_display(self, display_frame):
        """Create display output, and put it on the queue, if it is empty"""
        if self.output_queue.empty():
            # Get the jpg image for this
            encoded_bytes = pi_camera_stream.get_encoded_bytes_for_frame(display_frame)
            self.output_queue.put_nowait(encoded_bytes)


def flask_app(output_queue, control_queue):
    """The flask/webserver part is slightly independent of the behavior,
    allowing the user to "tune in" to see, but should not stop the
    robot running"""
    app = Flask(__name__)
    # app.debug = True
    # app.use_reloader = False

    def display_stream():
        while True:
            # at most 20 fps
            time.sleep(0.05)
            # Get (wait until we have data)
            encoded_bytes = output_queue.get()
            # Need to turn this into http multipart data.
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + encoded_bytes + b'\r\n')

    @app.route('/')
    def index():
        return render_template('color_track_server.html')

    @app.route('/start')
    def start():
        control_queue.put("START")
        return Response('queued')

    @app.route('/stop')
    def stop():
        control_queue.put("STOP")
        return Response('queued')

    @app.route('/video_feed')
    def video_feed():
        return Response(display_stream(),
            mimetype='multipart/x-mixed-replace; boundary=frame')

    app.run(host="0.0.0.0", port=5001)

print("Setting up")
bot = Robot()
# Set pan and tilt to middle, then clear it.
bot.set_pan(0)
bot.set_tilt(0)
time.sleep(0.1)
bot.servos.stop_all()

behavior = ColorTrackingBehavior(bot)
server = Process(target=flask_app, args=[behavior.output_queue, behavior.control_queue])
server.start()

try:
    behavior.run()
finally:
    server.terminate()
