import ledshim

class Leds(object):
    def __init__(self):
        self.count = 24

    def set_one(self, led_number, color):
        ledshim.set_pixel(led_number, *color)

    def set_range(self, a_range, color):
        ledshim.set_multiple_pixels(a_range, color)

    def set_all(self, color):
        ledshim.set_all(*color)

    def clear(self):
        ledshim.clear()

    def show(self):
        ledshim.show()