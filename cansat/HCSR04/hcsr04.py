import pigpio
import time
import collections
import numpy

TRIG = 23 #どこ？
ECHO = 24  #どこ？

pi = pigpio.pi()
 
#set GPIO direction (IN / OUT)
pi.set_mode(TRIG, pigpio.OUTPUT)
pi.set_mode(ECHO, pigpio.INPUT)

# 中央値フィルター用の箱10個
history = collections.deque(maxlen=10)

def distance():
    # set Trigger to HIGH
    pi.write(TRIG, 1)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    pi.write(TRIG, 0)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while pi.read(ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while pi.read(ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # sonic speed (34300 cm/s)
    distance = (TimeElapsed * 34300) / 2
 
    return distance

def distance_filtered():
    history.append(distance())
    return numpy.median(history)
 
if __name__ == '__main__':
    try:
        while True:
            dist = distance_filtered()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(0.2)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        pi.stop()