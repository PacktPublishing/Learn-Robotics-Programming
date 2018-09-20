from robot import Robot
import time

bot = Robot()
stop_at_time = time.time() + 60

speed = 80
bot.set_left(speed)
bot.set_right(speed)

proportional_constant = 4
integral_constant = 0.2
integral_sum = 0

while time.time() < stop_at_time:
    # Calculate the error
    left = bot.left_encoder.pulse_count
    right = bot.right_encoder.pulse_count
    error = left - right
    # Calculate the PI components
    proportional = (error * proportional_constant)
    integral_sum += error
    integral = integral_sum * integral_constant
    # Get the speed
    right_speed = int(speed + proportional + integral)
    print "left", left, \
        "right", right, \
        "right_speed:", right_speed, \
        "error:", error, \
        "p", proportional,\
        "i", "%.2f" % integral
    # Appy it to the right motor
    bot.set_right(right_speed)
    time.sleep(0.02)
