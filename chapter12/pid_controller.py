import math

class PIController(object):
    def __init__(self, proportional_constant=1.0, integral_constant=0.2):
        self.proportional_constant = proportional_constant
        self.integral_constant = integral_constant

        # Running sums
        self.integral_sum = 0

    def get_integral(self, error):
        self.integral_sum += error
        return self.integral_constant * self.integral_sum

    def get_proportional(self, error):
        return self.proportional_constant * error

    def get_value(self, error):
        return self.get_proportional(error) + self.get_integral(error)
