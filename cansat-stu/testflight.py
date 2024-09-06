from MPL3115A2 import MPL3115A2
from GPS import gps
from Motor import motor
from BNO055 import BNO055
import time
from pygame import joystick

mpl = MPL3115A2.MPL3115A2(MPL3115A2.ALTITUDE_MODE)
bno = BNO055.BNO055()
bno.begin()
joystick.init()
joy = joystick.Joystick(0)

print("Initialization OK")

while True:
    mpl.recordLog()
    bno.recordLog()
    gps.recordLog()

    Lx = joy.get_axis(0)
    button_A = joy.get_button(2)
    button_B = joy.get_button(2)

    if button_A:
        print("Push A")
        motor.move(7.5 * (1 - Lx), 7.5 * (1 + Lx), 0.1)

    if button_B:
    print("Push B")
        motor.stop()
