class PIController(object):
    def __init__(self, proportional_constant=0, integral_constant=0, windup_limit=None):
        self.proportional_constant = proportional_constant
        self.integral_constant = integral_constant
        self.windup_limit = windup_limit
        # Running sums
        self.integral_sum = 0

    def reset(self):
        self.integral_sum = 0

    def handle_proportional(self, error):
        return self.proportional_constant * error

    def handle_integral(self, error):
        """Integral will change if
            * There is no windup limit
            * We are below the windup limit
            * or the sign of the error would reduce the sum"""
        if self.windup_limit is None or \
                (abs(self.integral_sum) < self.windup_limit) or \
                ((error > 0) != (self.integral_sum > 0)):
            self.integral_sum += error
        return self.integral_constant * self.integral_sum

    def get_value(self, error):
        p = self.handle_proportional(error)
        i = self.handle_integral(error)
        return p + i
