from PIL import Image
import numpy as np
import time
import os
from picamera2 import Picamera2
from libcamera import Transform

# Define image dimensions
height = 100
width = 100

# Generate log file name with date_
log_filename = os.path.join(os.path.dirname(__file__), f"Camera_{time.strftime('%Y%m%d')}.log")

def log_message(message):
    """Log messages to both console and log file."""
    print(message)
    with open(log_filename, "a") as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

class Camera:
    def __init__(self):
        self.picam2 = Picamera2()
        camera_config = self.picam2.create_still_configuration(
            main={"size": (height, width)}
        )
        self.picam2.configure(camera_config)
        self.picam2.start()
        print("Camera initialized")

    def initialize_camera(self):
        print("Camera already initialized.")

    def capture_and_save(self, filename=None):
        # ファイルを保存する相対ディレクトリ
        save_dir = os.path.dirname(__file__)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # 現在の時刻を取得してファイル名に利用
        if filename is None:
            timeStamp = time.strftime("%Y%m%d-%H%M%S")
            filename = os.path.join(save_dir, f"img_{timeStamp}.jpg")
        
        # 撮影した画像を保存
        self.picam2.capture_file(filename)
        log_message(f"Image captured and saved to {filename}.")
        return filename

    def redthreshold_left_center_right(self, image_path, red_threshold=150, green_threshold=40, black_threshold=50):
        # 画像を読み込み
        image = Image.open(image_path)
        image_rgb = np.array(image)

        # 画像サイズとRGBチャンネル取得
        width, height, _ = image_rgb.shape
        r_channel = image_rgb[:, :, 0]
        g_channel = image_rgb[:, :, 1]
        b_channel = image_rgb[:, :, 2]

        # 赤色の判定マスクを作成
        red_mask = (r_channel > red_threshold) & (g_channel < green_threshold) & (r_channel > b_channel)

        # 黒色を除外
        black_mask = (r_channel < black_threshold) & (g_channel < black_threshold) & (b_channel < black_threshold)
        red_mask &= ~black_mask

        # 二値化画像作成
        red_binary = np.where(red_mask, 255, 0).astype(np.uint8)

        # 二値化画像を保存
        save_dir = os.path.dirname(__file__)
        threshold_image_path = os.path.join(save_dir, f"threshold_{os.path.basename(image_path)}")
        Image.fromarray(red_binary).convert("L").save(threshold_image_path)
        log_message(f"Threshold processed image saved to {threshold_image_path}.")

        # 画像をx方向に3分割
        section_width = width // 3
        sections = [red_binary[:, :section_width],
                    red_binary[:, section_width:2 * section_width],
                    red_binary[:, 2 * section_width:]]

        # 各セクションで赤色領域の割合を計算
        total_pixels = height * section_width
        counts = [np.sum(section == 255) for section in sections]
        percentages = [(count / total_pixels) * 100 for count in counts]

        # 最も赤色領域が多いセクションを判定
        max_count_index = np.argmax(counts)
        sections_labels = ["Left", "Center", "Right"]
        most_red_section = sections_labels[max_count_index]

        # ログに記録
        for label, percent in zip(sections_labels, percentages):
            log_message(f"{label}: {percent:.2f}% red area")
        log_message(f"Most red section: {most_red_section}")

        return most_red_section, percentages

    def stop_camera(self):
        # カメラのプレビュー停止と終了処理
        self.picam2.stop()
        log_message("Camera stopped.")

if __name__ == "__main__":
    camera = Camera()
    try:
        # 画像を撮影して保存
        image_path = camera.capture_and_save()

        # 保存した画像を解析（緑ではなく赤を検出）
        result, percentages = camera.redthreshold_left_center_right(image_path)
        log_message(f"The area with the most red is: {result}")

    except Exception as e:
        log_message(f"An error occurred: {e}")

    finally:
        camera.stop_camera()
