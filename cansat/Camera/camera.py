from PIL import Image
import numpy as np
import time
import os
from picamera2 import Picamera2
from libcamera import controls

class Camera:
    def __init__(self):
        # Picamera2のインスタンス作成と初期化
        self.picam2 = Picamera2()
        camera_config = self.picam2.create_preview_configuration()
        self.picam2.configure(camera_config)
        self.picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
        self.picam2.start()
        print("Camera initialized.")

    def initialize_camera(self):
        # 既に初期化済みのため特に必要な処理なし
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
        print(f"Image captured and saved to {filename}.")
        return filename

    def greenthreshold_left_center_right(self, image_path, threshold=40):
        # 画像を読み込み
        image = Image.open(image_path)

        # 画像サイズとRGB値の取得
        width, height = image.size
        image_rgb = np.array(image)
        g_channel = image_rgb[:, :, 1]  # 緑チャンネル

        # 閾値処理
        g_threshold = np.where(g_channel >= threshold, 255, 0).astype(np.uint8)  # 二値化

        # 二値化画像を保存
        save_dir = os.path.dirname(__file__)
        threshold_image_path = os.path.join(save_dir, f"threshold_{os.path.basename(image_path)}")
        Image.fromarray(g_threshold).convert("L").save(threshold_image_path)
        print(f"Threshold processed image saved to {threshold_image_path}.")

        # 画像をx方向に3分割して緑色が薄い領域を判定
        section_width = width // 3
        sections = [g_threshold[:, :section_width],
                    g_threshold[:, section_width:2*section_width],
                    g_threshold[:, 2*section_width:]]
        
        # 各セクションで緑色が薄い領域（40未満のピクセル）の割合を計算
        total_pixels = height * section_width
        counts = [np.sum(section == 0) for section in sections]
        percentages = [(count / total_pixels) * 100 for count in counts]

        # 最も緑が薄いセクションを判定
        max_count_index = np.argmax(counts)
        sections_labels = ["Left", "Center", "Right"]
        most_greenless_section = sections_labels[max_count_index]

        # 各セクションの緑が薄い領域の割合を表示
        for label, percent in zip(sections_labels, percentages):
            print(f"{label}: {percent:.2f}% greenless area")

        print(f"Most greenless section: {most_greenless_section}")
        return most_greenless_section, percentages

    def stop_camera(self):
        # カメラのプレビュー停止と終了処理
        self.picam2.stop()
        print("Camera stopped.")

if __name__ == "__main__":
    camera = Camera()
    try:
        # 画像を撮影して保存
        image_path = camera.capture_and_save()

        # 保存した画像を解析
        result, percentages = camera.greenthreshold_left_center_right(image_path)
        print(f"The area with the least green is: {result}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        camera.stop_camera()
