import robot
from time import sleep

r = robot.Robot()
r.set_left(70)
r.set_right(70)
sleep(1)
r.set_left(-70)
sleep(1)
r.set_left(70)
sleep(1)
r.set_right(20)
sleep(1)
r.set_right(70)
r.set_left(70)
sleep(1)