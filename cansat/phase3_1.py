from Router import router
from Motor import robot
import time
import csv

def phase3(goal_pos):
    rt = router.Router(goal_pos)
    log_file = "test_log.csv"
    
    with open(log_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Latitude", "Longitude", "Azimuth", "AngleDiff", "Distance", "Velocity"])
    
    while not rt.isGoal():
        times = 0
        rt.start()
        time.sleep(1)
        
        deg = rt.getAngleDiff()
        gps_pos = rt.getGpsPos()
        azimuth = rt.getAzimuth()
        distance = rt.getDistance()
        velocity = rt.getVelocity()
        
        with open(log_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([time.time(), gps_pos[0], gps_pos[1], azimuth, deg, distance, velocity])
        
        while abs(deg) > 15 and times < 5:
            robot.turn(deg)
            time.sleep(1)
            
            deg = rt.getAngleDiff()
            gps_pos = rt.getGpsPos()
            azimuth = rt.getAzimuth()
            distance = rt.getDistance()
            velocity = rt.getVelocity()
            
            with open(log_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([time.time(), gps_pos[0], gps_pos[1], azimuth, deg, distance, velocity])
            
            times += 1
        
        robot.move(0.75, 10)
        robot.stop()
        rt.stop()
    
    print("Arrived!!")

if __name__ == "__main__":
    goal_pos = [139.5182666, 35.463201]
    phase3(goal_pos)


# from Router import router
# from Motor import robot
# import time


# def phase3(goal_pos):
#     rt = router.Router(goal_pos)

#     while not rt.isGoal():
#         times = 0
#         rt.start()
#         time.sleep(1)
#         deg = rt.getAngleDiff()

#         while abs(deg) > 15 and times < 5:
#             robot.turn(deg)
#             deg = rt.getAngleDiff()
#             times += 1

#         robot.move(0.75, 10)
#         robot.stop()
#         rt.stop()

#     print("Arrived!!")

# if __name__ == "__main__":
#     goal_pos = [139.5182666, 35.463201]
#     phase3(goal_pos)
