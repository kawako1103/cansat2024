import pigpio
import time
import collections
import numpy

TRIG = 20
ECHO = 16

pi = pigpio.pi()
#set GPIO direction (IN / OUT)
pi.set_mode(TRIG, pigpio.OUTPUT)
pi.set_mode(ECHO, pigpio.INPUT)

# mean filter box
history = collections.deque(maxlen=10)

def distance():
    time.sleep(0.05)
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
    for _ in range(10):
        time.sleep(0.05)
        history.append(distance())
    return numpy.median(history)
    #return numpy.mean(history)
 
if __name__ == '__main__':
    dist = distance_filtered()
    print("Measured Distance = %.1f cm" % dist)
    time.sleep(0.05)
