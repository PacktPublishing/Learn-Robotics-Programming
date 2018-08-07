import spidev

class Leds(object):
    def __init__(self):
        self.leds_count = 8
        self.led_colors = [(0,0,0)] * self.leds_count
        # MOSI - default output, (Master Out, Slave in) is 10. Clock is 11. 
        self.led_device = spidev.SpiDev()
        self.led_device.open(0, 0)
        self.led_device.max_speed_hz = 15000

    def set_one(self, led_number, (r, g, b)):
        self.led_colors[led_number] = (r, g, b)

    def set_range(self, a_range, (r, g, b)):
        for led_number in a_range:
            print led_number
            self.led_colors[led_number] = (r, g, b)

    def set_all(self, (r, g, b)):
        self.led_colors = [(r, g ,b)] * self.leds_count

    def clear(self):
        self.set_all((0, 0, 0))

    def show(self):
        # Create the data frame
        # print("Colors:", self.led_colors)
        data = [0] * 4
        for color in self.led_colors:
            data.append(0xe1)
            data.extend(color)
        data.extend([0]* 4)
        # print("Data", data)
        # send it
        self.led_device.xfer(data)
    