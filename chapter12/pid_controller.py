class PIController(object):
    def __init__(self, proportional_constant=0, integral_constant=0):
        self.proportional_constant = proportional_constant
        self.integral_constant = integral_constant

        # Running sums
        self.integral_sum = 0

    def handle_proportional(self, error):
        return self.proportional_constant * error

    def handle_integral(self, error):
        self.integral_sum += error
        return self.integral_constant * self.integral_sum

    def get_value(self, error):
        p = self.handle_proportional(error)
        i = self.handle_integral(error)
        return p + i
