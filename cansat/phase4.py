from Motor import robot
from Camera.camera import Camera
#from HCSR04.hcsr04 import distance_filtered
from HCSR04.hcsr04 import get_distance, setup
import time
import os

# Generate log file name with date_
log_filename = os.path.join(os.path.dirname(__file__),f"phase4_{time.strftime('%Y%m%d')}.log")

setup() #HCSr04pinsetup
def log_message(message):
        """Log messages to both console and log file."""
        print(message)
        with open(log_filename, "a") as log_file:
                log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

# camera is reverse. Left is right. Right is left.                
def phase4():
    camera = Camera()
    
    try:
        while True:
            # capture and search a cone
            image_path = camera.capture_and_save()
            most_greenless_section, _ = camera.redthreshold_left_center_right(image_path)

            # Action based on the judgments results
            if most_greenless_section == "Right": #camera is reverse.
                log_message("Turning left")
                log_message("robot.sleep(2)")
                log_message("robot.turn(-10)")
                time.sleep(2)  
                robot.turn(-10)
                robot.stop()
                log_message("robot.sleep(2)")
                time.sleep(2)
                
            elif most_greenless_section == "Left": #camera is reverse.
                log_message("robot.sleep(2)")
                log_message("Turning right")
                time.sleep(2)
                log_message("robot.turn(10)")
                robot.turn(10)
                robot.stop()
                log_message("robot.sleep(2)")
                time.sleep(2)
                
                
            elif most_greenless_section == "Center":
                log_message("Moving forward")
                log_message("robot.sleep(2)")
                time.sleep(2)
                log_message("robot.move(0.2,0.4)")
                robot.move(0.2, 0.4)
                robot.stop()
                log_message("robot.sleep(2)")
                time.sleep(2)
                    
                # Measuring distance
                #current_distance = distance_filtered()
                current_distance = get_distance()
                if current_distance is None:
                    log_message("Measurement timeout!")
                    log_message("robot.sleep(2)")
                    time.sleep(2)
                    log_message("robot.turn(10)")
                    robot.turn(10)
                    robot.stop()
                    log_message("robot.sleep(2)")
                    time.sleep(2)

                else:
                    log_message(f"Current Distance: {current_distance:.1f} cm")
                    #current_distance = 1 #for test                
                    # if 5cm or less, it's over.
                    if current_distance <= 5:
                        log_message("Goal reached!")
                        break
                    elif current_distance >= 5.0:
                        log_message("Moving forward")
                        time.sleep(2)
                        log_message("robot.move(0.2,0.4)")
                        robot.move(0.2, 0.4)
                        log_message("robot.sleep(2)")
                        time.sleep(2)
                        robot.stop()
            log_message("robot.sleep(2)")            
            time.sleep(2)

    except Exception as e:
        time.sleep(2)
        log_message(f"An error occurred: {e}")
        robot.stop()
        
    finally:
        camera.stop_camera()
        robot.stop()
        log_message("Phase 4 completed.")

if __name__ == "__main__":
    phase4()
