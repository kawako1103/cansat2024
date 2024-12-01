from Motor import robot
from Camera import Camera
from HCSR04 import distance_filtered
import time


#カメラで実際にコーンを3mの場所において撮影して確かめたい。
#どのぐらいの割合になるのか確認
#日本語消す。phase4追加、main.pyに追記、camera.py追加、hcsr04.py追加
#余裕あれば、YOLO5やりたい。 https://github.com/jhan15/traffic_cones_detection

def phase4():
    camera = Camera()
    try:
        while True:
            # 距離を測定
            current_distance = distance_filtered()
            print(f"Current Distance: {current_distance:.1f} cm")

            # 1cm以下で終了
            if current_distance <= 1:
                print("Goal reached!")
                break

            # カメラで画像を撮影し緑が少ない方向を判定
            image_path = camera.capture_and_save()
            most_greenless_section, _ = camera.greenthreshold_left_center_right(image_path)

            # 判定結果に応じて動作
            if most_greenless_section == "Left":
                print("Turning left")
                robot.turn(-10)  # 左に10度回転
            elif most_greenless_section == "Right":
                print("Turning right")
                robot.turn(10)  # 右に10度回転
            elif most_greenless_section == "Center":
                print("Moving forward")
                robot.move(0.75, 10)  # 前方に進む、速度0.75、時間10秒?、1秒ぐらいにしたい。

            time.sleep(0.5)  # 次の操作までの短い遅延

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        camera.stop_camera()
        robot.stop()
        print("Phase 4 completed.")

if __name__ == "__main__":
    phase4()
