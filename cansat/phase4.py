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
    count = 0
    
    try:
        while True:
            count = count + 1
            if count >= 100:
                break
                
            # カメラで画像を撮影し緑が少ない方向を判定
            image_path = camera.capture_and_save()
            most_greenless_section, _ = camera.redthreshold_left_center_right(image_path)

            # 判定結果に応じて動作
            if most_greenless_section == "Right": #camera is reverse.
                log_message("Turning left")
                robot.turn(-20)  # 左に10度回転
                robot.stop()
                time.sleep(0.4)
            
            elif most_greenless_section == "Left": #camera is reverse.
                log_message("Turning right")
                #robot.start()
                robot.turn(20)  # 右に10度回転
                robot.stop()
                time.sleep(0.4)
            
            elif most_greenless_section == "Center":
                log_message("Moving forward")
                #robot.start()
                robot.move(0.5, 1)  # 前方に進む、速度0.3,時間0.54秒
                robot.stop()
                time.sleep(0.4)  # 次の操作までの短い遅延                    
                # 距離を測定
                #current_distance = distance_filtered()
                #current_distance = get_distance()
                ##if current_distance is None:
                #    log_message("Measurement timeout!")
                #    robot.turn(0.5)
                #    time.sleep(0.4)

                #else:
                    #log_message(f"Current Distance: {current_distance:.1f} cm")
                    #current_distance = 1 #for test                
                    # 5cm以下で終了
                    #if current_distance <= 5:
                    #    log_message("Goal reached!")
                    #    break
                    #elif current_distance >= 5:
                    #    log_message("Moving forward")
                    #    robot.move(0.3, 0.1)  # 前方に進む、速度0.3,時間0.54秒
                    #    time.sleep(0.4)  # 次の操作までの短い遅延
            
            elif most_greenless_section == "None":
                log_message("None cone picture")
                #robot.start()
                robot.turn(20)
                robot.stop()
                time.sleep(0.4)

            time.sleep(0.8)  # 次の操作までの短い遅延
            

    except Exception as e:
        log_message(f"An error occurred: {e}")
    finally:
        camera.stop_camera()
        robot.stop()
        log_message("Phase 4 completed.")

if __name__ == "__main__":
    phase4()
