from Router import router2 as router
from Motor import robot
import time
import csv

def phase3(goal_pos):
    start_time = time.time()
    rt = router.Router(goal_pos)
    log_file = "test_log_mayu2.csv"
    
    with open(log_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Latitude", "Longitude", "Azimuth", "AngleDiff", "Distance", "Velocity", "Status"])
    
    while not rt.isGoal():
        times = 0
        rt.start()
        time.sleep(1)
        
        deg = rt.getAngleDiff()
        gps_pos = rt.getGpsPos()
        azimuth = rt.getAzimuth()
        distance = rt.getDistance()
        velocity = rt.getVelocity()
        time_stamp = time.time() - start_time
        
        if gps_pos[0] == 0.0 and gps_pos[1] == 0.0:
            print("Warning: GPS data is (0.0, 0.0), check if GPS is working correctly.")
        
        velocity_value = velocity[-1] if isinstance(velocity, list) and len(velocity) > 0 else 0.0
        
        status = "00"
        
        if deg > 0:
            deg = deg if abs(deg) < abs(deg - 360) else deg - 360
        else:
            deg = deg if abs(deg) < abs(deg + 360) else deg + 360
        
        while abs(deg) > 15.0 and times < 40:
            # print(f"before turn GPS: {gps_pos}, Azimuth: {azimuth}, AngleDiff: {deg}, Distance: {distance}, Velocity: {velocity}")
            
            if deg > 0:
                status = robot.turn(20) 
                print(f"Turn right! Status : {status}")
            else:
                status = robot.turn(-20)
                print(f"Turn left! Status : {status}")
            
            robot.stop()
            time.sleep(1)
            
            rt.update()
            deg = rt.getAngleDiff()
            gps_pos = rt.getGpsPos()
            azimuth = rt.getAzimuth()
            distance = rt.getDistance()
            velocity = rt.getVelocity()
            time_stamp = time.time() - start_time 
            
            print(f"after turn GPS: {gps_pos}, Azimuth: {azimuth}, AngleDiff: {deg}, Distance: {distance}, Velocity: {velocity}")
            
            velocity_value = velocity[-1] if isinstance(velocity, list) and len(velocity) > 0 else 0.0
            
            with open(log_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([time_stamp, gps_pos[0], gps_pos[1], azimuth, deg, distance, velocity_value, status])
            
            times += 1
        
        print("Move")
        status = robot.move(0.75, 3) 
        robot.stop()
        
        with open(log_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([time_stamp, gps_pos[0], gps_pos[1], azimuth, deg, distance, velocity_value, status])  
        
        rt.stop()
    
    print("Arrived!!")

if __name__ == "__main__":
    goal_pos = [130.5758851, 30.2248274]
    phase3(goal_pos)