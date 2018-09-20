from robot import Robot
import time

bot = Robot()
stop_at_time = time.time() + 1

bot.set_left(90)
bot.set_right(90)

while time.time() < stop_at_time:
    print "Left:", bot.left_encoder.pulse_count, "Right:", bot.right_encoder.pulse_count
    time.sleep(0.05)
