from __future__ import print_function
from robot import Robot, EncoderCounter
from pid_controller import PIController
import time
import math


def drive_distances(bot, left_distance, right_distance, speed=80):
    # We always want the "primary" to be the longest distance, therefore the faster motor
    if abs(left_distance) >= abs(right_distance):
        print("Left is primary")
        set_primary        = bot.set_left
        primary_encoder    = bot.left_encoder
        set_secondary      = bot.set_right
        secondary_encoder  = bot.right_encoder
        primary_distance   = left_distance
        secondary_distance = right_distance
    else:
        print("right is primary")
        set_primary        = bot.set_right
        primary_encoder    = bot.right_encoder
        set_secondary      = bot.set_left
        secondary_encoder  = bot.left_encoder
        primary_distance   = right_distance
        secondary_distance = left_distance
    primary_to_secondary_ratio = secondary_distance / (primary_distance * 1.0)
    secondary_speed = speed * primary_to_secondary_ratio
    print("Targets - primary: %d, secondary: %d, ratio: %.2f" % (primary_distance, secondary_distance, primary_to_secondary_ratio))

    primary_encoder.reset()
    secondary_encoder.reset()
    
    controller = PIController(proportional_constant=5, integral_constant=0.2)

    # Ensure that the encoder knows which way it is going
    primary_encoder.set_direction(math.copysign(1, speed))
    secondary_encoder.set_direction(math.copysign(1, secondary_speed))

    # start the motors, and start the loop
    set_primary(speed)
    set_secondary(secondary_speed)
    while abs(primary_encoder.pulse_count) < abs(primary_distance) or abs(secondary_encoder.pulse_count) < abs(secondary_distance):
        # And sleep a bit before calculating
        time.sleep(0.05)

        # How far off are we?
        secondary_target = primary_encoder.pulse_count * primary_to_secondary_ratio
        error = secondary_target - secondary_encoder.pulse_count

        # How fast should the motor move to get there?
        adjustment = controller.get_value(error)

        set_secondary(secondary_speed + adjustment)
        secondary_encoder.set_direction(math.copysign(1, secondary_speed+adjustment))
        # Some debug
        print("Primary c:{:.2f} ({:.2f} mm)\tSecondary c:{:.2f} ({:.2f} mm) t:{:.2f} e:{:.2f} s:{:.2f} adjustment: {:.2f}".format(
            primary_encoder.pulse_count, 
            primary_encoder.distance_in_mm(),
            secondary_encoder.pulse_count,
            secondary_encoder.distance_in_mm(),
            secondary_target,
            error,
            secondary_speed,
            adjustment
        ))

        # Stop the primary if we need to
        if abs(primary_encoder.pulse_count) >= abs(primary_distance):
            print("primary stop")
            set_primary(0)
            secondary_speed = 0

def drive_arc(bot, turn_in_degrees, radius, speed=80):
    """ Turn is based on change in heading. """
    # Get the bot width in ticks
    half_width_ticks = EncoderCounter.mm_to_ticks(bot.wheel_distance_mm/2.0)
    if turn_in_degrees < 0:
        left_radius     = radius - half_width_ticks
        right_radius    = radius + half_width_ticks
    else:
        left_radius     = radius + half_width_ticks
        right_radius    = radius - half_width_ticks
    print("Arc left radius {:.2f}, right_radius {:.2f}".format(left_radius, right_radius))
    radians = math.radians(abs(turn_in_degrees))
    left_distance = int(left_radius * radians)
    right_distance = int(right_radius * radians)
    print("Arc left distance {}, right_distance {}".format(left_distance, right_distance))
    drive_distances(bot, left_distance, right_distance, speed=speed)

bot = Robot()

distance_to_drive = 300 # in mm
distance_in_ticks = EncoderCounter.mm_to_ticks(distance_to_drive)
radius = bot.wheel_distance_mm + 100 # in mm
radius_in_ticks = EncoderCounter.mm_to_ticks(radius)

for n in range(4):
    drive_distances(bot, distance_in_ticks, distance_in_ticks)
    drive_arc(bot, 90, radius_in_ticks, speed=50)
