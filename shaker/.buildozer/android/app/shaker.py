# Photo Shaker by Shipra Singh.

from microbit import *
import random
import os
import Image
import time

path = "/home/shipra/Awwnindya/images"
while True:
    display.show(':)')
    if accelerometer.was_gesture('shake'):
        display.clear()
        time.sleep(1000)
        display.show(random.choice([
            x for x in os.listdir(path)
            if os.path.isfile(os.path.join(path, x))]))
    time.sleep(10)
