import RPi.GPIO as GPIO
import time

# 40番ピンを出力モードに設定
pin_number = 40
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin_number, GPIO.OUT)

try:
    while True:
        # 2秒間LEDを点灯
        GPIO.output(pin_number, GPIO.HIGH)
        time.sleep(2)

        # 2秒間LEDを消灯
        GPIO.output(pin_number, GPIO.LOW)
        time.sleep(2)

except KeyboardInterrupt:
    # Ctrl+Cでプログラムを終了
    GPIO.cleanup()

