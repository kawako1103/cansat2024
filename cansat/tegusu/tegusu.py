import RPi.GPIO as GPIO
import time

# GPIO
GPIO.setmode(GPIO.BCM)

#
GPIO.setup(21, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(26, GPIO.OUT, initial=GPIO.LOW)


def cutWire():
    try:
        i = 0
        while i < 5:

            GPIO.output(21, GPIO.HIGH)
            GPIO.output(26, GPIO.LOW)
            time.sleep(1.0)

            GPIO.output(21, GPIO.LOW)
            GPIO.output(26, GPIO.HIGH)
            time.sleep(1.0)
            i += 1
    except KeyboardInterrupt:
        GPIO.cleanup()

    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    cutWire()
