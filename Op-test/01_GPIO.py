import RPi.GPIO as GPIO
import time

# GPIO Pin number
LED_PIN = 23

# GPIO Setting
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    # Blink
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)  # LED ON
        time.sleep(1)  # Wait 1s
        GPIO.output(LED_PIN, GPIO.LOW)   # LED OFF
        time.sleep(1)  # Wait 1s

except KeyboardInterrupt:
    # プログラムの終了時にGPIOをクリーンアップ
    GPIO.cleanup()
