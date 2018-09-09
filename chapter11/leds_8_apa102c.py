import spidev

class Leds(object):
    def __init__(self):
        # MOSI - default output, (Master Out, Slave in) is 10. Clock is 11. 
        self.device = spidev.SpiDev()
        self.device.open(0, 0)
        self.device.max_speed_hz = 15000
        self.colors = [(0,0,0)] * self.count

    @property
    def count(self):
        return 8

    def set_one(self, led_number, color):
        assert(len(color) == 3)
        self.colors[led_number] = color

    def set_range(self, a_range, color):
        for led_number in a_range:
            self.colors[led_number] = color

    def set_all(self, color):
        self.colors = [color] * self.count

    def clear(self):
        self.set_all((0, 0, 0))

    def show(self):
        # Create the wake up header
        data = [0] * 4
        for color in self.colors:
            data.append(0xe1)
            data.extend(color)
        data.extend([0]* 4)
        # send it
        self.device.xfer(data)
