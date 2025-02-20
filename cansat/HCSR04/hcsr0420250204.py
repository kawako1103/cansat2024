import RPi.GPIO as GPIO
import time
GPIO.cleanup()

# pin number (BCM)
TRIG = 20 #GPIO20 (pin=38)
ECHO = 16 #GPIO16 (pin=36)

#GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def get_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00002) # 10us
    GPIO.output(TRIG, False)

    timeout = time.time() + 1  # 1秒でタイムアウト
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        if time.time() > timeout:
            print("ECHOnotachiagarigakensyutusarenai")
            return None  # タイムアウト時はNoneを返す

    timeout = time.time() + 1
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        if time.time() > timeout:
            print("ECHOnotachiagarigakensyutusarenai")
            return None

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 2)

	
try:
	while True:
		time.sleep(1)
		dist = get_distance()
		
		print(f"distance: {dist} cm")
		time.sleep(1)
		
except KeyboardInterrupt:
	print("finish distance")
	
finally:	
	GPIO.cleanup()
