from robot import Robot
from time import sleep
from gpiozero import LineSensor

r = Robot()

lsensor = LineSensor(23, pull_up=True)
rsensor = LineSensor(16, pull_up=True)

lsensor.when_line = r.stop_motors
rsensor.when_line = r.stop_motors
r.set_left(60)
r.set_right(60)
while True:
  sleep(0.02)
