from robot import Robot
from time import sleep

myrobot = Robot()

myrobot.set_left(30)
myrobot.set_right(30)

for n in range(8):
    myrobot.display.set_multiple_pixels(range(0, 7), (255, 0, 0))
    myrobot.display.set_multiple_pixels(range(7, 14), (0, 255, 0))
    myrobot.display.set_multiple_pixels(range(14, 21), (0, 0, 255))
    myrobot.display.set_multiple_pixels(range(21, 28), (255, 255, 255))
    myrobot.display.show()
    sleep(0.5)
    myrobot.display.clear()
    myrobot.display.show()
    sleep(0.5)


