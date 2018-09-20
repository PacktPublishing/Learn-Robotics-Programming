from gpiozero import DigitalInputDevice


class EncoderCounter(object):
    def __init__(self, pin_number):
        self.device = DigitalInputDevice(pin=pin_number)
        self.device.pin.when_changed = self.when_changed
        self.pulse_count = 0

    def when_changed(self):
        self.pulse_count += 1

    def reset(self):
        self.pulse_count = 0

    def stop(self):
        self.device.pin.when_changed = None
        self.device.close()