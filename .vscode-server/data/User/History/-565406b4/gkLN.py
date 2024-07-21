from gpiozero import Motor
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

# DCモータのピン設定
PIN_AIN1 = 
PIN_AIN2 = 23
PIN_BIN1 = 24
PIN_BIN2 = 13

dcm_pins = {
    "left_forward": PIN_AIN2,
    "left_backward": PIN_AIN1,
    "right_forward": PIN_BIN2,
    "right_backward": PIN_BIN1,
}

def smooth_transition(motor, target_value, step=0.01, delay=0.02):
    current_value = motor.value
    while current_value != target_value:
        if current_value < target_value:
            current_value = min(current_value + step, target_value)
        else:
            current_value = max(current_value - step, target_value)
        motor.value = current_value
        sleep(delay)

def reset():
    factory = PiGPIOFactory()
    motor_left = Motor(forward=dcm_pins["left_forward"],
                       backward=dcm_pins["left_backward"],
                       pin_factory=factory,
                       pwm=True,
                       pwm_frequency=16000)
    motor_right = Motor(forward=dcm_pins["right_forward"],
                        backward=dcm_pins["right_backward"],
                        pin_factory=factory,
                        pwm=True,
                        pwm_frequency=16000)

def main():
    factory = PiGPIOFactory()
    motor_left = Motor(forward=dcm_pins["left_forward"],
                       backward=dcm_pins["left_backward"],
                       pin_factory=factory,
                       pwm=True,
                       pwm_frequency=16000)
    motor_right = Motor(forward=dcm_pins["right_forward"],
                        backward=dcm_pins["right_backward"],
                        pin_factory=factory,
                        pwm=True,
                        pwm_frequency=16000)

    try:
        print("最高速で正回転 - 1秒")
        smooth_transition(motor_left, 1.0)
        smooth_transition(motor_right, 1.0)
        sleep(1)
        
        print("少し遅く正回転 - 2秒")
        smooth_transition(motor_left, 0.75)
        smooth_transition(motor_right, 0.75)
        sleep(2)
        
        print("遅く正回転 - 1秒")
        smooth_transition(motor_left, 0.5)
        smooth_transition(motor_right, 0.5)
        sleep(1)
        
        print("停止 - 1秒")
        smooth_transition(motor_left, 0.0)
        smooth_transition(motor_right, 0.0)
        sleep(1)
        
        print("最高速で逆回転 - 1秒")
        smooth_transition(motor_left, -1.0)
        smooth_transition(motor_right, -1.0)
        sleep(1)
        
        print("少し遅く逆回転 - 1秒")
        smooth_transition(motor_left, -0.75)
        smooth_transition(motor_right, -0.75)
        sleep(1)
        
        print("遅く逆回転 - 1秒")
        smooth_transition(motor_left, -0.5)
        smooth_transition(motor_right, -0.5)
        sleep(1)
        
        print("停止 - 1秒")
        smooth_transition(motor_left, 0.0)
        smooth_transition(motor_right, 0.0)
        sleep(1)
    except KeyboardInterrupt:
        print("stop")
        motor_left.stop()
        motor_right.stop()

if __name__ == "__main__":
    main()

def rotate():
    factory = PiGPIOFactory()
    motor_left = Motor(forward=dcm_pins["left_forward"],
                       backward=dcm_pins["left_backward"],
                       pin_factory=factory,
                       pwm=True,
                       pwm_frequency=16000)
    motor_right = Motor(forward=dcm_pins["right_forward"],
                        backward=dcm_pins["right_backward"],
                        pin_factory=factory,
                        pwm=True,
                        pwm_frequency=16000)

    try:
        print("最高速で正回転 - 2秒")
        smooth_transition(motor_left, 1.0)
        smooth_transition(motor_right, 1.0)
        sleep(2)
        
        print("遅く正回転 - 2秒")
        smooth_transition(motor_left, 0.5)
        smooth_transition(motor_right, 0.5)
        sleep(2)
        
        print("停止 - 2秒")
        smooth_transition(motor_left, 0.0)
        smooth_transition(motor_right, 0.0)
        sleep(2)
        
        print("遅く逆回転 - 2秒")
        smooth_transition(motor_left, -0.5)
        smooth_transition(motor_right, -0.5)
        sleep(2)
        
        print("最高速で逆回転 - 2秒")
        smooth_transition(motor_left, -1.0)
        smooth_transition(motor_right, -1.0)
        sleep(2)
        
        print("停止 - 2秒")
        smooth_transition(motor_left, 0.0)
        smooth_transition(motor_right, 0.0)
        sleep(2)
    except KeyboardInterrupt:
        print("stop")
        motor_left.stop()
        motor_right.stop()

    return
