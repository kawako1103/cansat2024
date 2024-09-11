from gpiozero import Robot
import threading
import time

PIN_AIN1 = 27
PIN_AIN2 = 22
PIN_BIN1 = 13
PIN_BIN2 = 19


robot = Robot(left=(PIN_BIN1, PIN_BIN2), right=(PIN_AIN1, PIN_AIN2))


def move(target_speed, mtime, speed=0.1, step=0.01):
    while target_speed > speed and mtime > 0:
        speed += 0.01
        mtime -= step
        robot.forward(speed, curve_right=0.1)
        time.sleep(step)
    time.sleep(abs(mtime))


def turn(degree):
    # 180 deg is 1s
    mtime = abs(degree / 180)
    if degree > 0:
        robot.right(0.5)
        time.sleep(mtime)
    else:
        robot.left(0.5)
        time.sleep(mtime)


def stop():
    robot.stop()


def start():
    while running == True:
        thread = threading.Thread(target=move(7.5, 100))
        thread.start()


if __name__ == "__main__":
    move(0.75, 5)
    # turn(90)
    stop()
