from scipy.integrate import cumtrapz
from pyproj import Geod
import time
import threading

#try to use gps, BNO055
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#

#from BNO055 import BNO055
from GPS import gps
from BNO055 import BNO055
#from GPS import gps

class Router:
    def __init__(self, goal_pos):#*goal_pos to goal_pos by kawako
        self.goal_flag = False
        self.goal_pos = goal_pos
        self.gps_pos = [000.0000000, 000.0000000]
        self.bno = BNO055.BNO055()
        self.geod = Geod(ellps="WGS84")
        self.azimuth = 0
        self.bwk_azimuth = 0
        self.distance = 0
        self.angle_N = 0.0
        self.start_time = time.monotonic()
        self.acc_data = [0.0]
        self.time_data = [0.0]
        self.vel = 0.0
        self.running = True

    def initialize(self):
        self.acc_data = [0]
        self.time_data = [0]
        self.start_time = time.monotonic()
        self.vel = 0

    def getGpsPos(self):
        return self.gps_pos

    def getDistance(self):
        return self.distance

    def getAzimuth(self):
        return self.azimuth

    def getVelocity(self):
        return self.vel

    def getNorth(self):
        return self.angle_N

    def getAngleDiff(self):
        return self.azimuth - self.angle_N

    def isGoal(self):
        return self.goal_flag

    def calcAngleDist(self):
        #kawako change the code like below
        lon1, lat1 = self.gps_pos[0], self.gps_pos[1]
        lon2, lat2 = self.goal_pos[0], self.goal_pos[1]
        self.azimuth, self.bwk_azimuth, self.distance = self.geod.inv(lon1, lat1, lon2, lat2)
        #previous code is below(by koyama)
        #c2g_pos = (self.gps_pos[0], self.gps_pos[1], self.goal_pos[0], self.goal_pos[1])
        #self.azimuth, self.bwk_azimuth, self.distance = self.geod.inv(c2g_pos)

    def checkGoal(self):
        if self.distance < 10:
            self.goal_flag = True

    def update(self):
        pos = gps.getLonLat(DEG=True)
        if sum(pos) != 0:
            self.gps_pos = pos

        self.angle_N = self.bno.getEulerInQuat()[0]
        #Check Later
        accy = self.bno.getVector(self.bno.VECTOR_LINEARACCEL)[1] * -1
        self.acc_data.append(accy)
        timestamp = round((time.monotonic() - self.start_time) / 10, 2)
        self.time_data.append(timestamp)
        self.vel = cumtrapz(self.acc_data, self.time_data)
        self.calcAngleDist()
        self.checkGoal()

    def start(self, interval= 0.05):
        self.running = True

        def run():
            while self.running:
                self.update()
                time.sleep(interval)

        thread = threading.Thread(target=run)
        thread.start()
        return thread

    def stop(self):
        self.initialize()
        self.running = False


if __name__ == "__main__":
    goal_pos = [139.870595, 35.769833]#kanamachi station_decimal(10) number(not sexagesimal(60))
    #router = Router(*goal_pos)
    router = Router(goal_pos)

    router.update()
    router.getAzimuth()
    router.getDistance()
    print("")

    router.start()

    while True:
        router.getGpsPos()
        router.getAzimuth()
        router.getDistance()
        print("")
        time.sleep(0.01)
