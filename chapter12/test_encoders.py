from robot import Robot
import time

from gpiozero import DigitalInputDevice


class EncoderCounter(object):
    def __init__(self, pin_number):
        self.pulse_count = 0
        self.device = DigitalInputDevice(pin=pin_number)
        self.device.pin.when_changed = self.when_changed

    def when_changed(self):
        self.pulse_count += 1


bot = Robot()
left_encoder = EncoderCounter(4)
right_encoder = EncoderCounter(26)
stop_at_time = time.time() + 1

bot.set_left(90)
bot.set_right(90)

while time.time() < stop_at_time:
    print("Left:", left_encoder.pulse_count, "Right:", right_encoder.pulse_count)
    time.sleep(0.05)
