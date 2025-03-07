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
    # 
    global robot  # 既存の `robot` を更新する
    if robot is not None:
        robot.close()  # 既存の `robot` を閉じて GPIO を解放
    # 
    robot = Robot(left=(PIN_BIN1, PIN_BIN2), right=(PIN_AIN1, PIN_AIN2))
##

#TODO left rightでdutyを調整したい 正回転と逆回転を調整
# def move(target_speed, mtime, speed=0.1, step=0.01):
#     while target_speed > speed and mtime > 0.0:
#         speed += 0.01
#         mtime -= step
#         robot.forward(speed, curve_right=0.1)
#         time.sleep(step)
#     time.sleep(abs(mtime))

##
def move(target_speed, mtime, speed=0.1, step=0.01, right_bias=0.044):
    """
    target_speed: 目標速度 (0.0 ~ 1.0)
    mtime: 移動時間 (秒)
    speed: 初期速度
    step: 速度増加のステップサイズ
    right_bias: 右の車輪のPWMを増やす割合 (デフォルト0.05)
    """
    while target_speed > speed and mtime > 0.0:
        speed += step
        mtime -= step
        left_speed = speed
        right_speed = speed + right_bias  # 右を少し速くする

        # 安全に1.0を超えないように制限
        right_speed = min(1.0, right_speed)

        robot.left_motor.forward(left_speed)
        robot.right_motor.forward(right_speed)

        time.sleep(step)

    time.sleep(abs(mtime))
    stop()
##




def turn(degree):
    # 180 deg is 1s
    mtime = abs(degree / 180.0)
    if degree > 0.0:
        robot.right(0.5)
        time.sleep(mtime)
    else:
        robot.left(0.5)
        time.sleep(mtime)


def stop():
    robot.stop()


def start():
    while running == True:
        thread = threading.Thread(target=move(7.5, 100.0))
        thread.start()


if __name__ == "__main__":
    # move(0.4, 0.8) #move(0.75, 5)
    move(0.75, 5) #move(0.75, 5)
    # turn(-90.0/2.5)
    stop()
