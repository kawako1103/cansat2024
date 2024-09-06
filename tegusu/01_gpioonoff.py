import RPi.GPIO as GPIO
import time

# GPIOモードの設定
GPIO.setmode(GPIO.BCM)

# 使用するGPIOピンの設定
GPIO.setup(21, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(26, GPIO.OUT, initial=GPIO.LOW)

try:
    while True:
        # GPIO21をON、GPIO26をOFF
        GPIO.output(21, GPIO.HIGH)
        GPIO.output(26, GPIO.LOW)
        time.sleep(0.1)

        # GPIO21をOFF、GPIO26をON
        GPIO.output(21, GPIO.LOW)
        GPIO.output(26, GPIO.HIGH)
        time.sleep(0.1)

except KeyboardInterrupt:
    # スクリプトがCTRL+Cで終了されたときにGPIOピンの設定をクリーンアップ
    GPIO.cleanup()
