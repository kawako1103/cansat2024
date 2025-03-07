from gpiozero import Robot
import threading
import time

PIN_AIN1 = 27
PIN_AIN2 = 22
PIN_BIN1 = 13
PIN_BIN2 = 19

robot = Robot(left=(PIN_BIN1, PIN_BIN2), right=(PIN_AIN1, PIN_AIN2))

##0303
def initialize():
    global robot  
    if robot is not None:
        robot.close()  
    robot = Robot(left=(PIN_BIN1, PIN_BIN2), right=(PIN_AIN1, PIN_AIN2))


def move(target_speed, mtime, speed=0.1, step=0.01, right_bias=0.044):
    while target_speed > speed and mtime > 0.0:
        speed += step
        mtime -= step
        left_speed = speed
        right_speed = speed + right_bias  

        right_speed = min(1.0, right_speed) 

        robot.left_motor.forward(left_speed)
        robot.right_motor.forward(right_speed)
        
        time.sleep(step)
    time.sleep(abs(mtime))
    stop()
    ###
    return "00"  
    ### 


def turn(degree):
    mtime = abs(degree / 180.0)
    if degree > 0.0:
        robot.right(0.5)
        time.sleep(mtime)
        stop()
        return "01"  
    else:
        robot.left(0.5)
        time.sleep(mtime)
        stop()
        return "10"  


def stop():
    robot.stop()


def start():
    while running:
        thread = threading.Thread(target=move(7.5, 100.0))
        thread.start()


if __name__ == "__main__":
    result = move(0.75, 5)  
    print(result)  
    
    result = turn(-90.0 / 2.5)  
    print(result)  
    
    stop()
