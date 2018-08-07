from robot import Robot
from time import sleep
#import leds_led_shim
import leds_8_apa102c


bot = Robot(leds_8_apa102c.Leds())
red = (255, 0, 0)
blue = (0, 0, 255)

while True:
    print("red")
    bot.leds.set_all(red)
    bot.leds.show()
    sleep(0.5)
    print("blue")
    bot.leds.set_all(blue)
    bot.leds.show()
    sleep(0.5)

