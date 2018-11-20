"""Object for the HC-SR04 distance sensor type."""
import time # import the whole thing, we need more than just sleep
from gpiozero import DigitalInputDevice, DigitalOutputDevice

# This is an exception, we will send this when get distance fails to make a measurement
class NoDistanceRead(Exception):
    """The system was unable to make a measurement"""
    pass # We aren't doing anything special, but python syntax demands us to be explicit about this.

class DistanceSensor(DigitalInputDevice):
    """Represents a distance sensor."""
    def __init__(self, trigger_pin, echo_pin):
        # Setup devices, an input device and an output device, with pin numbers for the sensor.
        super(DistanceSensor, self).__init__(echo_pin)
        self._trigger = DigitalOutputDevice(trigger_pin)
        self._trigger.value = False

    def get_distance(self):
        """Method to get the distance measurement"""
        # Timeout - we'll use this to stop it getting stuck
        time_out = time.time() + 2

        # This off-on-off pulse tells the device to make a measurement
        self._trigger.value = True
        time.sleep(0.00001) # This is the 10 microseconds
        self._trigger.value = False

        # Wait for the pin state to stop being 0, going from low to high
        # When it rises, this is the real pulse start. Assign it once - it may already have changed!
        pulse_start = time.time()
        while self.pin.state == 0:
            pulse_start = time.time()
            # We ran out of time
            if pulse_start > time_out:
                raise NoDistanceRead("Timed Out")

        # Wait for the echo pin to stop being 1, going from high, to low, the end of the pulse.
        pulse_end = time.time()
        while self.pin.state == 1:
            pulse_end = time.time()
            # Pulse end not received
            if pulse_end > time_out:
                raise NoDistanceRead("Timed Out")

        # The duration is the time between the start and end of pulse in seconds.
        pulse_duration = pulse_end - pulse_start
        # Speed of sound in centimeters per second - 34300 cm/s. However, the pulse has travelled TWICE 
        # the distance, so we get half of this. (34300 / 2) = 17150.
        distance = pulse_duration * 17150
        # Round it to 2 decimal places, any finer doesn't really make sense.
        distance = round(distance, 2)
        return distance
