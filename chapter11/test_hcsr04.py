from gpiozero import GPIODevice, InputDevice, OutputDevice, DigitalInputDevice, DigitalOutputDevice
import time

# Setup devices
print "Prepare GPIO pins"

trigger = DigitalOutputDevice(17)
echo = DigitalInputDevice(27)

trigger.value = False

print "Waiting For Sensor To Settle"

time.sleep(0.5)

def make_measurement(trig_device, echo_device):
    """Function to get the distance measurement"""
    # Timeout - we'll use this to stop it getting stuck
    time_out = time.time() + 2

    # This off-on-off pulse tells the device to make a measurement
    trig_device.value = True
    time.sleep(0.00001)
    trig_device.value = False

    # This pulse end can be used to detect we didn't get a reading
    pulse_end = None

    # Here, we wait for the pin state to stop being 0, that is, to go from low to high, or we run out of time.
    # When it rises, this is the real pulse start.
    while echo_device.pin.state == 0 and time.time() < time_out:
        pulse_start = time.time()

    # Now we wait for the echo_device pin to stop being 1, going from high, to low, the end of the pulse.
    while echo_device.pin.state == 1 and time.time() < time_out:
        pulse_end = time.time()

    # If we don't get a pulse end, we timed out. Return a maximum distance (we could have missed the pule if it was too close too)
    if pulse_end is None:
        print "timed out"
        return 100

    # The duration is the time between the start and end of pulse in seconds.
    pulse_duration = pulse_end - pulse_start
    # This number is the speed of sound in centimeters per second - 34300 cm/s. However, the pulse has travelled TWICE 
    # the distance, so we get half of this. (34300 / 2) = 17150.
    distance = pulse_duration * 17150
    # Round it to 2 decimal places, any finer doesn't really make sense.
    distance = round(distance, 2)
    return distance

while True:
    # Make our measurement and print it
    distance = make_measurement(trigger, echo)
    print "Distance: ",distance,"cm"
    # Sleep a bit before making another.
    time.sleep(0.5)
