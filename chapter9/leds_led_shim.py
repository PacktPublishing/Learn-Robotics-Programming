import ledshim

class Leds(object):
    def __init__(self):
        self.leds_count = 24

    def set_one(self, led_number, (r, g, b)):
        ledshim.set_pixel(led_number, r, g, b)

    def set_range(self, a_range, (r, g, b)):
        ledshim.set_multiple_pixels(a_range, (r, g, b))

    def set_all(self, (r, g, b)):
        ledshim.set_all(r, g, b)

    def clear(self):
        ledshim.clear()

    def show(self):
        ledshim.show()