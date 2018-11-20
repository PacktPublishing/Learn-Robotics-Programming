from __future__ import print_function
from robot import Robot, EncoderCounter
from pid_controller import PIController
import time


def drive_distance(bot, distance, speed=80):
    # Use left as "primary"  motor, the right is keeping up
    set_primary        = bot.set_left
    primary_encoder    = bot.left_encoder
    set_secondary      = bot.set_right
    secondary_encoder  = bot.right_encoder
    
    controller = PIController(proportional_constant=5, integral_constant=0.2)

    # start the motors, and start the loop
    set_primary(speed)
    set_secondary(speed)
    while primary_encoder.pulse_count < distance or secondary_encoder.pulse_count < distance:
        # Sleep a bit before calculating
        time.sleep(0.05)
        # How far off are we?
        error = primary_encoder.pulse_count - secondary_encoder.pulse_count
        adjustment = controller.get_value(error)
        # How fast should the motor move to get there?
        set_secondary(speed + adjustment)
        # Some debug
        print("Primary c:{} ({} mm)\tSecondary c:{} ({} mm) e:{} adjustment: {:.2f}".format(
            primary_encoder.pulse_count, primary_encoder.distance_in_mm(),
            secondary_encoder.pulse_count, secondary_encoder.distance_in_mm(),
            error,
            adjustment
        ))


bot = Robot()
distance_to_drive = 1000 # in mm - this is a meter
distance_in_ticks = EncoderCounter.mm_to_ticks(distance_to_drive)
drive_distance(bot, distance_in_ticks, distance_in_ticks)
