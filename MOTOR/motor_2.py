from gpiozero import PWMOutputDevice, DigitalOutputDevice
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

# DCモータのピン設定
PIN_AIN1 = 27
PIN_AIN2 = 22
PIN_BIN1 = 13
PIN_BIN2 = 19

dcm_pins = {
    "right_backward": PIN_AIN2,
    "right_forward": PIN_AIN1,
    "left_backward": PIN_BIN2,
    "left_forward": PIN_BIN1,
}

class MotorPWM:
    def __init__(self, forward_pin, backward_pin, pwm_frequency=16000, pin_factory=None):#previous:pwm_frequency=16000
        self.forward = PWMOutputDevice(forward_pin, frequency=pwm_frequency, pin_factory=pin_factory)
        self.backward = PWMOutputDevice(backward_pin, frequency=pwm_frequency, pin_factory=pin_factory)
        self._value = 0.0  # _value属性の初期化

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, speed):
        self._value = speed
        if speed > 0:
            self.forward.value = speed
            self.backward.value = 0
        elif speed < 0:
            self.forward.value = 0
            self.backward.value = -speed
        else:
            self.forward.value = 0
            self.backward.value = 0

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
    motor_left = MotorPWM(forward_pin=dcm_pins["left_forward"],
                          backward_pin=dcm_pins["left_backward"],
                          pin_factory=factory)
    motor_right = MotorPWM(forward_pin=dcm_pins["right_forward"],
                           backward_pin=dcm_pins["right_backward"],
                           #pwm_frequency=16000,
                           pin_factory=factory)

def main():
    factory = PiGPIOFactory()
    motor_left = MotorPWM(forward_pin=dcm_pins["left_forward"],
                          backward_pin=dcm_pins["left_backward"],
                          pin_factory=factory)
    motor_right = MotorPWM(forward_pin=dcm_pins["right_forward"],
                           backward_pin=dcm_pins["right_backward"],
                           pin_factory=factory)

    try:
        #print("遅く遅く正回転 - 0.2秒")
        #smooth_transition(motor_left, 0.25)#previous 0.5
        #smooth_transition(motor_right, 0.25)
        #sleep(0.2)
        
        print("遅く正回転 - 0.2秒")
        smooth_transition(motor_left, 0.5)#previous 0.5
        smooth_transition(motor_right, 0.5)
        sleep(0.3)
        
        print("少し遅く正回転 - 0.2秒")
        smooth_transition(motor_left, 0.6)#previous 0.5
        smooth_transition(motor_right, 0.6)
        sleep(0.3)
        
        print("少し少し遅く正回転 - 0.2秒")
        smooth_transition(motor_left, 0.75)#previous 0.5
        smooth_transition(motor_right, 0.75)
        sleep(0.3)
        
        print("最高速で正回転 - 1秒")
        smooth_transition(motor_left, 1.0)#previous 1,0
        smooth_transition(motor_right, 1.0)
        sleep(1)
        
        print("少し遅く正回転 - 2秒")
        smooth_transition(motor_left, 0.75)#previous 0.75
        smooth_transition(motor_right, 0.75)
        sleep(2)
        
        print("少し少し遅く正回転 - 0.2秒")
        smooth_transition(motor_left, 0.6)#previous 0.5
        smooth_transition(motor_right, 0.6)
        sleep(0.2)
        
        print("遅く正回転 - 1秒")
        smooth_transition(motor_left, 0.5)#previous 0.5
        smooth_transition(motor_right, 0.5)
        sleep(1)
        
        print("遅く正回転 - 0.2秒")
        smooth_transition(motor_left, 0.5)#previous 0.5
        smooth_transition(motor_right, 0.5)
        sleep(0.2)
        
        print("停止 - 1秒")
        smooth_transition(motor_left, 0.0)
        smooth_transition(motor_right, 0.0)
        sleep(1)
        
        
        print("遅く逆回転 - 0.2秒")
        smooth_transition(motor_left, -0.5)#previous 0.5
        smooth_transition(motor_right, -0.5)
        sleep(0.2)
        
        print("少し遅く正回転 - 0.2秒")
        smooth_transition(motor_left, -0.6)#previous 0.5
        smooth_transition(motor_right, -0.6)
        sleep(0.2)
        
        print("少し少し遅く逆回転 - 0.2秒")
        smooth_transition(motor_left, -0.75)#previous 0.5
        smooth_transition(motor_right, -0.75)
        sleep(0.2)
        
        print("最高速で逆回転 - 1秒")
        smooth_transition(motor_left, -1.0)#previous -1.0
        smooth_transition(motor_right, -1.0)
        sleep(1)
        
        print("少し遅く逆回転 - 1秒")
        smooth_transition(motor_left, -0.75)#previous -0.75
        smooth_transition(motor_right, -0.75)
        sleep(1)
        
        print("遅く逆回転 - 1秒")
        smooth_transition(motor_left, -0.5)#previous -0.5
        smooth_transition(motor_right, -0.5)
        sleep(1)
        
        print("停止 - 1秒")
        smooth_transition(motor_left, 0.0)
        smooth_transition(motor_right, 0.0)
        sleep(1)
        
    except KeyboardInterrupt:
        print("stop")
        motor_left.value = 0.0
        motor_right.value = 0.0
    
#motor's max duty is "duty" and motor will rotate for "time" seconds in this method, motor won't stop.
def move_forward(duty, time):
    factory = PiGPIOFactory()
    motor_left = MotorPWM(forward_pin=dcm_pins["left_forward"],
                          backward_pin=dcm_pins["left_backward"],
                          pin_factory=factory)
    motor_right = MotorPWM(forward_pin=dcm_pins["right_forward"],
                           backward_pin=dcm_pins["right_backward"],
                           pin_factory=factory)
    
    #motor will be rotated when duty is more than 0.5
    #therefore if you input the duty, motor should rotate absolutely
    #ex:if you input duty = 0 or duty = 0.5 or duty = 1.0, duty ratio is 0.5, 0.75, 1 respectively. 
    duty_ratio = 0.5*(1 + duty)
     
    try:
        print("遅く正回転 - 0.2秒")
        smooth_transition(motor_left, 0.5 * duty_ratio)#previous 0.5
        smooth_transition(motor_right, 0.5 * duty_ratio)
        sleep(0.3)
        
        print("少し遅く正回転 - 0.2秒")
        smooth_transition(motor_left, 0.6 * duty_ratio)#previous 0.5
        smooth_transition(motor_right, 0.6 * duty_ratio)
        sleep(0.3)
        
        print("少し少し遅く正回転 - 0.2秒")
        smooth_transition(motor_left, 0.75 * duty_ratio)#previous 0.5
        smooth_transition(motor_right, 0.75 * duty_ratio)
        sleep(0.3)
        
        print("最高速で正回転 - time秒")
        smooth_transition(motor_left, 1.0 * duty_ratio)#previous 1,0
        smooth_transition(motor_right, 1.0 * duty_ratio)
        sleep(time)
        
    except KeyboardInterrupt:
        print("stop")
        motor_left.value = 0.0
        motor_right.value = 0.0
        
def motor_stop():
    factory = PiGPIOFactory()
    motor_left = MotorPWM(forward_pin=dcm_pins["left_forward"],
                          backward_pin=dcm_pins["left_backward"],
                          pin_factory=factory)
    motor_right = MotorPWM(forward_pin=dcm_pins["right_forward"],
                           backward_pin=dcm_pins["right_backward"],
                           pin_factory=factory)

    try:
        print("遅く逆回転 - 0.2秒")
        smooth_transition(motor_left, -0.5)
        smooth_transition(motor_right, -0.5)
        sleep(0.2)
        
        print("停止 - 0.5秒")
        smooth_transition(motor_left, 0.0)
        smooth_transition(motor_right, 0.0)
        sleep(0.5)
        
    except KeyboardInterrupt:
        print("stop")
        motor_left.value = 0.0
        motor_right.value = 0.0
        

def turn_right_test():
    factory = PiGPIOFactory()
    motor_left = MotorPWM(forward_pin=dcm_pins["left_forward"],
                          backward_pin=dcm_pins["left_backward"],
                          pin_factory=factory)
    motor_right = MotorPWM(forward_pin=dcm_pins["right_forward"],
                           backward_pin=dcm_pins["right_backward"],
                           pin_factory=factory)

    try:
        print("遅く回転 - 0.2秒")
        smooth_transition(motor_left, 0.5)#previous 0.5
        smooth_transition(motor_right, -0.5)
        sleep(0.3)
        
        print("少し遅く回転 - 0.2秒")
        smooth_transition(motor_left, 0.6)#previous 0.5
        smooth_transition(motor_right, -0.6)
        sleep(0.3)
        
        print("少し少し遅く回転 - 0.2秒")
        smooth_transition(motor_left, 0.75)#previous 0.5
        smooth_transition(motor_right, -0.75)
        sleep(0.3)
        
        print("最高速で回転 - 1秒")
        smooth_transition(motor_left, 1.0)#previous 1,0
        smooth_transition(motor_right, -1.0)
        sleep(1)
        
        print("少し遅く回転 - 2秒")
        smooth_transition(motor_left, 0.75)#previous 0.75
        smooth_transition(motor_right, -0.75)
        sleep(2)
        
        print("少し少し遅く回転 - 0.2秒")
        smooth_transition(motor_left, 0.6)#previous 0.5
        smooth_transition(motor_right, -0.6)
        sleep(0.2)
        
        print("遅く回転 - 1秒")
        smooth_transition(motor_left, 0.5)#previous 0.5
        smooth_transition(motor_right, -0.5)
        sleep(1)
        
        print("遅く回転 - 0.2秒")
        smooth_transition(motor_left, 0.5)#previous 0.5
        smooth_transition(motor_right, -0.5)
        sleep(0.2)
        
        print("停止 - 1秒")
        smooth_transition(motor_left, 0.0)
        smooth_transition(motor_right, 0.0)
        sleep(1)
        
    except KeyboardInterrupt:
        print("stop")
        motor_left.value = 0.0
        motor_right.value = 0.0

def turn_left_test():
    factory = PiGPIOFactory()
    motor_left = MotorPWM(forward_pin=dcm_pins["left_forward"],
                          backward_pin=dcm_pins["left_backward"],
                          pin_factory=factory)
    motor_right = MotorPWM(forward_pin=dcm_pins["right_forward"],
                           backward_pin=dcm_pins["right_backward"],
                           pin_factory=factory)

    try:
        print("遅く回転 - 0.2秒")
        smooth_transition(motor_left, -0.5)#previous 0.5
        smooth_transition(motor_right, 0.5)
        sleep(0.3)
        
        print("少し遅く回転 - 0.2秒")
        smooth_transition(motor_left, -0.6)#previous 0.5
        smooth_transition(motor_right, 0.6)
        sleep(0.3)
        
        print("少し少し遅く回転 - 0.2秒")
        smooth_transition(motor_left, -0.75)#previous 0.5
        smooth_transition(motor_right, 0.75)
        sleep(0.3)
        
        print("最高速で回転 - 1秒")
        smooth_transition(motor_left, -1.0)#previous 1,0
        smooth_transition(motor_right, 1.0)
        sleep(1)
        
        print("少し遅く回転 - 0.2秒")
        smooth_transition(motor_left, -0.75)#previous 0.75
        smooth_transition(motor_right, 0.75)
        sleep(0.2)
        
        print("少し少し遅く回転 - 0.2秒")
        smooth_transition(motor_left, -0.6)#previous 0.5
        smooth_transition(motor_right, 0.6)
        sleep(0.2)
        
        print("遅く回転 - 0.2秒")
        smooth_transition(motor_left, -0.5)#previous 0.5
        smooth_transition(motor_right, 0.5)
        sleep(0.2)
        
        print("遅く回転 - 0.2秒")
        smooth_transition(motor_left, -0.5)#previous 0.5
        smooth_transition(motor_right, 0.5)
        sleep(0.2)
        
        print("停止 - 1秒")
        smooth_transition(motor_left, 0.0)
        smooth_transition(motor_right, 0.0)
        sleep(1)
        
    except KeyboardInterrupt:
        print("stop")
        motor_left.value = 0.0
        motor_right.value = 0.0

def turn_right(duty, time):
    factory = PiGPIOFactory()
    motor_left = MotorPWM(forward_pin=dcm_pins["left_forward"],
                          backward_pin=dcm_pins["left_backward"],
                          pin_factory=factory)
    motor_right = MotorPWM(forward_pin=dcm_pins["right_forward"],
                           backward_pin=dcm_pins["right_backward"],
                           pin_factory=factory)
    
    #motor will be rotated when duty is more than 0.5
    #therefore if you input the duty, motor should rotate absolutely
    #ex:if you input duty = 0 or duty = 0.5 or duty = 1.0, duty ratio is 0.5, 0.75, 1 respectively. 
    duty_ratio = 0.5*(1 + duty)

    try:
        print("遅く回転 - 0.2秒")
        smooth_transition(motor_left, 0.5 * duty_ratio)#previous 0.5
        smooth_transition(motor_right, -0.5 * duty_ratio)
        sleep(0.3)
        
        print("少し遅く回転 - 0.2秒")
        smooth_transition(motor_left, 0.6 * duty_ratio)#previous 0.5
        smooth_transition(motor_right, -0.6 * duty_ratio)
        sleep(0.3)
        
        print("少し少し遅く回転 - 0.2秒")
        smooth_transition(motor_left, 0.75 * duty_ratio)#previous 0.5
        smooth_transition(motor_right, -0.75 * duty_ratio)
        sleep(0.3)
        
        print("最高速で回転 - time秒")
        smooth_transition(motor_left, 1.0 * duty_ratio)#previous 1,0
        smooth_transition(motor_right, -1.0 * duty_ratio)
        sleep(time)
        
        print("少し遅く回転 - 0.2秒")
        smooth_transition(motor_left, 0.75 * duty_ratio)#previous 0.75
        smooth_transition(motor_right, -0.75 * duty_ratio)
        sleep(0.2)
        
        print("少し少し遅く回転 - 0.2秒")
        smooth_transition(motor_left, 0.6 * duty_ratio)#previous 0.5
        smooth_transition(motor_right, -0.6 * duty_ratio)
        sleep(0.2)
        
        print("遅く回転 - 0.2秒")
        smooth_transition(motor_left, 0.5 * duty_ratio)#previous 0.5
        smooth_transition(motor_right, -0.5 * duty_ratio)
        sleep(0.2)
        
        print("停止 - 1秒")
        smooth_transition(motor_left, 0.0)
        smooth_transition(motor_right, 0.0)
        sleep(1)
        
    except KeyboardInterrupt:
        print("stop")
        motor_left.value = 0.0
        motor_right.value = 0.0

    
def turn_left(duty, time):
    factory = PiGPIOFactory()
    motor_left = MotorPWM(forward_pin=dcm_pins["left_forward"],
                          backward_pin=dcm_pins["left_backward"],
                          pin_factory=factory)
    motor_right = MotorPWM(forward_pin=dcm_pins["right_forward"],
                           backward_pin=dcm_pins["right_backward"],
                           pin_factory=factory)
    
    #motor will be rotated when duty is more than 0.5
    #therefore if you input the duty, motor should rotate absolutely
    #ex:if you input duty = 0 or duty = 0.5 or duty = 1.0, duty ratio is 0.5, 0.75, 1 respectively. 
    duty_ratio = 0.5*(1 + duty)

    try:
        print("遅く回転 - 0.2秒")
        smooth_transition(motor_left, -0.5 * duty_ratio)#previous 0.5
        smooth_transition(motor_right, 0.5 * duty_ratio)
        sleep(0.3)
        
        print("少し遅く回転 - 0.2秒")
        smooth_transition(motor_left, -0.6 * duty_ratio)#previous 0.5
        smooth_transition(motor_right, 0.6 * duty_ratio)
        sleep(0.3)
        
        print("少し少し遅く回転 - 0.2秒")
        smooth_transition(motor_left, -0.75 * duty_ratio)#previous 0.5
        smooth_transition(motor_right, 0.75 * duty_ratio)
        sleep(0.3)
        
        print("最高速で回転 time秒")
        smooth_transition(motor_left, -1.0 * duty_ratio)#previous 1,0
        smooth_transition(motor_right, 1.0 * duty_ratio)
        sleep(time)
        
        print("少し遅く回転 - 0.2秒")
        smooth_transition(motor_left, -0.75 * duty_ratio)#previous 0.75
        smooth_transition(motor_right, 0.75 * duty_ratio)
        sleep(0.2)
        
        print("少し少し遅く回転 - 0.2秒")
        smooth_transition(motor_left, -0.6 * duty_ratio)#previous 0.5
        smooth_transition(motor_right, 0.6 * duty_ratio)
        sleep(0.2)
        
        print("遅く回転 - 0.2秒")
        smooth_transition(motor_left, -0.5 * duty_ratio)#previous 0.5
        smooth_transition(motor_right, 0.5 * duty_ratio)
        sleep(0.2)
        
        print("停止 - 1秒")
        smooth_transition(motor_left, 0.0)
        smooth_transition(motor_right, 0.0)
        sleep(1)
        
    except KeyboardInterrupt:
        print("stop")
        motor_left.value = 0.0
        motor_right.value = 0.0

if __name__ == "__main__":
    print("straight")
    #main()
    
    #move_forward should be used with motor_stop()
    #move_forward(duty, time)
    move_forward(0.5, 5.0)
    #stop
    print("stop")
    motor_stop()
    
    
    print("left")
    #turn_left(duty, time)
    turn_left(0.5, 2)
    
    #turn_right(duty, time)
    print("right")
    turn_right(0.5, 2)

def rotate():
    factory = PiGPIOFactory()
    motor_left = MotorPWM(forward=dcm_pins["left_forward"],
                          backward=dcm_pins["left_backward"],
                          pin_factory=factory)
    motor_right = MotorPWM(forward=dcm_pins["right_forward"],
                           backward=dcm_pins["right_backward"],
                           pin_factory=factory)

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
        motor_left.value = 0.0
        motor_right.value = 0.0

    return