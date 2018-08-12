import spidev

class Leds(object):
    def __init__(self):
        # MOSI - default output, (Master Out, Slave in) is 10. Clock is 11. 
        self.led_device = spidev.SpiDev()
        self.led_device.open(0, 0)
        self.led_device.max_speed_hz = 15000

        self.leds_count = 8
        self.led_colors = [(0,0,0)] * self.leds_count

    def set_one(self, led_number, color):
        assert(len(color) == 3)
        self.led_colors[led_number] = color

    def set_range(self, a_range, color):
        for led_number in a_range:
            self.led_colors[led_number] = color

    def set_all(self, color):
        self.led_colors = [color] * self.leds_count

    def clear(self):
        self.set_all((0, 0, 0))

    def show(self):
        # Create the wake up header
        data = [0] * 4
        for color in self.led_colors:
            data.append(0xe1)
            data.extend(color)
        data.extend([0]* 4)
        # send it
        self.led_device.xfer(data)
    