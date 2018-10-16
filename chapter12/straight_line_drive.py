from __future__ import print_function
from robot import Robot
from pid_controller import PIController
import time

bot = Robot()
stop_at_time = time.time() + 5

speed = 80
bot.set_left(speed)
bot.set_right(speed)

pid = PIController(proportional_constant=4, integral_constant=0.2)
while time.time() < stop_at_time:
    time.sleep(0.02)
    # Calculate the error
    left = bot.left_encoder.pulse_count
    right = bot.right_encoder.pulse_count
    error = left - right
    # Get the speed
    adjustment = pid.get_value(error)
    right_speed = int(speed + adjustment)
    print("left", left,
        "right", right,
        "right_speed:", right_speed,
        "error:", error,
        "adjustment: %.2f" % adjustment)
    # Appy it to the right motor
    bot.set_right(right_speed)
