from Router import router2 as router
import lora_tx_release_pre2 as LoRaTX
from Motor import robot
import time
import csv
import os

def phase3(goal_pos, port, baudrate, reset_pin, file_path_lora,file_path_al):
    start_time = time.time()  #add
    rt = router.Router(goal_pos)
    tx=LoRaTX.LoRaTransmitter(port, baudrate, reset_pin,file_path_lora)
    tx.initialize_device()
    
    for file in [file_path_lora,file_path_al]:
        if not os.path.exists(file):
            with open(file, mode='w', newline='') as f:
                writer = csv.writer(f)
    
    while not (rt.isGoal() and rt.longitude_flag==True and rt.latitude_flag==True) :
        times = 0
        rt.start()
        tx.start()
        status = "00" 
        
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
        
         
        
        if deg > 0:
            deg = deg if abs(deg) < abs(deg - 360) else deg - 360
        else:
            deg = deg if abs(deg) < abs(deg + 360) else deg + 360

        ## log
            with open(file_path_al, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([f"before turn|| GPS:{gps_pos}, Azimuth: {azimuth}, AngleDiff: {deg}, Distance: {distance}, Velocity: {velocity}"])
                writer.writerow([f"before turn|| AngleDiff is {deg}"])

        
        while abs(deg) > 15.0 and times < 40:
            print(f"before turn GPS|| {gps_pos}, Azimuth: {azimuth}, AngleDiff: {deg}, Distance: {distance}, Velocity: {velocity}")
            
            if deg > 0:
                status = robot.turn(20)  
                print(f"Turn right! status:{status}")
            else:
                status = robot.turn(-20)  
                print(f"Turn left! status:{status}")
            
            robot.stop()
            time.sleep(1)
            
            rt.update()
            deg = rt.getAngleDiff()
            gps_pos = rt.getGpsPos()
            azimuth = rt.getAzimuth()
            distance = rt.getDistance()
            velocity = rt.getVelocity()
            time_stamp = time.time() - start_time 
            
            #####
            if gps_pos[0] < 130:
                rt.longitude_flag = False
            else:
                rt.longitude_flag = True
                

            if gps_pos[1] < 30:
                rt.latitude_flag = False
            else:
                rt.latitude_flag = True
            #####         
            
            
            ## velocity = [1.5, 2.0, 3.2] -> velocity[-1]=3.2  
            velocity_value = velocity[-1] if isinstance(velocity, list) and len(velocity) > 0 else 0.0
            formatted_lon = f"{gps_pos[0]:011.7f}" 
            formatted_lat = f"{gps_pos[1]:011.8f}"  

            print(f"after turn|| GPS:{gps_pos}, Azimuth: {azimuth}, AngleDiff: {deg}, Distance: {distance}, Velocity: {velocity}")
            print(f"after turn|| goal_flag:{rt.goal_flag}, longitude_flag:{rt.longitude_flag}, latitude_flag:{rt.latitude_flag}")
            
            ## log
            with open(file_path_al, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([f"after turn|| GPS:{gps_pos}, Azimuth: {azimuth}, AngleDiff: {deg}, Distance: {distance}, Velocity: {velocity}"])
                writer.writerow([f"after turn|| AngleDiff is {deg}"])
                
        
            with open(file_path_lora, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([formatted_lon, formatted_lat])
            
            times += 1
            if time==40 :
                print("time out !!! count=40")
                ## log
                with open(file_path_al, mode='a', newline='') as file:
                    file.write("time out !!! count=40\n") 
        
        
        status = robot.move(0.75, 3)
        print(f"End Turn-phase ! AngleDiff is {deg}")
        print(f"Move forward! status:{status}")
        print(f"after going forward||  GPS:{gps_pos}, Azimuth: {azimuth}, AngleDiff: {deg}, Distance: {distance}, Velocity: {velocity}") 
        print(f"goal_flag:{rt.goal_flag}, longitude_flag:{rt.longitude_flag}, latitude_flag:{rt.latitude_flag}")
        
        ## log
        # with open(file_path_al, mode='a', newline='') as file:
        #     writer = csv.writer(file)
        #     writer.writerow([time_stamp, gps_pos[0], gps_pos[1], azimuth, deg, distance, velocity_value, status])
        #     file.write(f"End Turn-phase ! AngleDiff is {deg}\n")
        #     file.write(f"Move forward! status:{status}") 
        #     file.write(f"after going forward: {gps_pos}, Azimuth: {azimuth}, AngleDiff: {deg}, Distance: {distance}, Velocity: {velocity}")
        with open(file_path_al, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([f"End Turn-phase ! AngleDiff is {deg}"])
            writer.writerow([f"befor move forward|| {gps_pos}, Azimuth: {azimuth}, AngleDiff: {deg}, Distance: {distance}, Velocity: {velocity}"])
            writer.writerow([f"Move forward! status:{status}"])
            writer.writerow([f"after move forward|| {gps_pos}, Azimuth: {azimuth}, AngleDiff: {deg}, Distance: {distance}, Velocity: {velocity}"])
    
        ## LORA
        with open(file_path_lora, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([formatted_lon, formatted_lat])
        
        robot.stop() 
        rt.stop()
    
    print(f"goal_flag:{rt.goal_flag}, longitude_flag:{rt.longitude_flag}, latitude_flag:{rt.latitude_flag}")
    print("Arrived!!")
    ## log
    with open(file_path_al, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([f"Arrival point|| GPS:{gps_pos}, Azimuth: {azimuth}, AngleDiff: {deg}, Distance: {distance}, Velocity: {velocity}"])
            writer.writerow([f"goal_flag:{rt.goal_flag}, longitude_flag:{rt.longitude_flag}, latitude_flag:{rt.latitude_flag}"])
            writer.writerow([f"Arrived!!"])

    tx.stop()

if __name__ == "__main__":
    goal_pos = [130.9012733, 30.41519633333333]#deg? center aozora_park@tanegashima
    PORT = "/dev/ttyS0"
    BAUDRATE = 115200
    # RESET_PIN = 22 #~0305
    RESET_PIN = 25 #0305~


    FILE_PATH_LoRa = "/home/cansat-stu/cansat/sensor_0308_only_gps_3.log"   # file for LoRa
    FILE_PATH_ALL = "/home/cansat-stu/cansat/sensor_0308_al_3.log"    # file for all sensors
    
    phase3(goal_pos,PORT, BAUDRATE, RESET_PIN, FILE_PATH_LoRa, FILE_PATH_ALL)


