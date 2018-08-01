from gpiozero import LineSensor
from time import sleep


lsensor = LineSensor(23)
rsensor = LineSensor(16)

while True:
    print "Left", lsensor.is_active, "Right", rsensor.is_active
    sleep(0.05)
