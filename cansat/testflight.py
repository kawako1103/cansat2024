from MPL3115A2 import MPL3115A2
from GPS import gps
from Motor import motor
from BNO055 import BNO055
import pygame
import time

mpl = MPL3115A2.MPL3115A2(0)
bno = BNO055.BNO055()
bno.begin()

pygame.init()
pygame.joystick.init()
joy = pygame.joystick.Joystick(0)
joy.init()

button_A = 0
button_B = 0
Lx = 0

while True:
    mpl.recordLog()
    bno.recordLog()
    gps.recordLog()

    if pygame.event.get():

        Lx = joy.get_axis(0)
        button_A = joy.get_button(2)
        button_B = joy.get_button(3)

        if button_A:
            print("A")
            motor.move(0.75 * (1 - Lx), 0.75 * (1 + Lx), 0.01)
            button_A = 0

        if button_B:
            print("B")
            motor.stop()
            button_B = 0
    else:
        time.sleep(0.01)
