from Router import router2 as router
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
        
        # デバッグ用出力
        print(f"GPS: {gps_pos}, Azimuth: {azimuth}, AngleDiff: {deg}, Distance: {distance}, Velocity: {velocity}")
        
        # GPSが正しく取得されているか確認
        if gps_pos[0] == 0.0 and gps_pos[1] == 0.0:
            print("Warning: GPS data is (0.0, 0.0), check if GPS is working correctly.")
        
        # velocity をスカラ値に変換
        velocity_value = velocity[-1] if isinstance(velocity, list) and len(velocity) > 0 else 0.0
        
        with open(log_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([time.time(), gps_pos[0], gps_pos[1], azimuth, deg, distance, velocity_value])
        
        while abs(deg) > 15 and times < 1: #5
            rt.update()
            #robot.turn(deg/100.0)
            robot.turn(deg/2.5)
            robot.stop()
            time.sleep(1)
            
            deg = rt.getAngleDiff()
            gps_pos = rt.getGpsPos()
            azimuth = rt.getAzimuth()
            distance = rt.getDistance()
            velocity = rt.getVelocity()
            
            print(f"GPS: {gps_pos}, Azimuth: {azimuth}, AngleDiff: {deg}, Distance: {distance}, Velocity: {velocity}")
            
            velocity_value = velocity[-1] if isinstance(velocity, list) and len(velocity) > 0 else 0.0
            
            with open(log_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([time.time(), gps_pos[0], gps_pos[1], azimuth, deg, distance, velocity_value])
            
            times += 1
        
        robot.move(0.75, 10)
        robot.stop()
        rt.stop()
    
    print("Arrived!!")

if __name__ == "__main__":
    goal_pos = [139.514296921, 35.461619311]
    #goal_pos = [13951.4296921, 3546.1619311]
    #goal_pos = [1.664396, 0.5961997]
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
