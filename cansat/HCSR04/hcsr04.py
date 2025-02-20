"""
import RPi.GPIO as GPIO
import time
import sys

trig_pin = 20                           # GPIO 38
echo_pin = 16                           # GPIO 36
speed_of_sound = 34370                  # 20℃での音速(cm/s)

GPIO.setmode(GPIO.BCM)                  # GPIOをBCMモードで使用
GPIO.setwarnings(False)                 # BPIO警告無効化
GPIO.setup(trig_pin, GPIO.OUT)          # Trigピン出力モード設定
GPIO.setup(echo_pin, GPIO.IN)           # Echoピン入力モード設定

def get_distance(): 
	#Trigピンを10μsだけHIGHにして超音波の発信開始
	GPIO.output(trig_pin, GPIO.HIGH)
	time.sleep(0.000010)
	GPIO.output(trig_pin, GPIO.LOW)

	while not GPIO.input(echo_pin):
		pass
	t1 = time.time() # 超音波発信時刻（EchoピンがHIGHになった時刻）格納

	while GPIO.input(echo_pin):
		pass
	t2 = time.time() # 超音波受信時刻（EchoピンがLOWになった時刻）格納

	return (t2 - t1) * speed_of_sound / 2 # 時間差から対象物までの距離計算



if __name__ == '__main__':
	while True:# 繰り返し処理
		try:
			distance = '{:.1f}'.format(get_distance())  # 小数点1までまるめ
			print("Distance: " + distance + "cm")       # 表示
			time.sleep(1)                               # 1秒まつ

		except KeyboardInterrupt:                       # Ctrl + C押されたたら
			GPIO.cleanup()                              # GPIOお片付け
			sys.exit()                                  # プログラム終了
	"""
 
import RPi.GPIO as GPIO
import time

trig_pin = 20                           # GPIO 38
echo_pin = 16                           # GPIO 36
speed_of_sound = 34370                  # Speed of sound at 20°C (cm/s)
timeout = 0.03                         # Timeout duration (30ms) 34370*0.03/2=5.16m

def setup():
    """Initialize GPIO settings"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(trig_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)

def cleanup():
    """Release GPIO resources"""
    GPIO.cleanup()

def get_distance():
    """Measure distance using the ultrasonic sensor"""
    GPIO.output(trig_pin, GPIO.HIGH)
    time.sleep(0.000010)
    GPIO.output(trig_pin, GPIO.LOW)

    start_time = time.time()
    
    # Wait for the Echo pin to go HIGH (with timeout)
    while not GPIO.input(echo_pin):
        if time.time() - start_time > timeout:
            return None  # Timeout occurred

    t1 = time.time()  # Timestamp when the pulse is sent

    # Wait for the Echo pin to go LOW (with timeout)
    while GPIO.input(echo_pin):
        if time.time() - t1 > timeout:
            return None  # Timeout occurred

    t2 = time.time()  # Timestamp when the pulse is received
    return (t2 - t1) * speed_of_sound / 2  # Calculate distance

if __name__ == '__main__':
    try:
        setup()  # Initialize GPIO
        while True:
            distance = get_distance()
            if distance is None:
                print("Measurement timeout!")
            else:
                print(f"Distance: {distance:.1f} cm")
            time.sleep(1)
    except KeyboardInterrupt:
        cleanup()  # Release GPIO before exiting
