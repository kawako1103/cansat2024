import time

#try to use gps, BNO055
#import sys
#import os

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#

from MPL3115A2 import MPL3115A2
#from GPS import gps #GPS will be sent to ground administrator via LoRa
from BNO055 import BNO055

ALTITUDE_MODE = 0
#PRESSURE_MODE = 1

if __name__ == "__main__":
    
    #MLP3115A2;)
    mpla = MPL3115A2(MPL3115A2.ALTITUDE_MODE)
    #mpla = MPL3115A2()
    #mplp = MPL3115A2(MPL3115A2.PRESSURE_MODE)


    #BNO055;
    bno = BNO055()
    time = 0

    while True:
        
        mpla.recordLog()

        bno.recordLog()
        print("Now time count : %f C" % time)
        time.sleep(1)
        time += 1

