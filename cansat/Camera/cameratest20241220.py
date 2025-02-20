from picamera2 import Picamera2
import cv2
import numpy as np

# Picamera2の初期化
picam2 = Picamera2()

# カメラ設定のカスタマイズ
config = picam2.create_still_configuration(main={"size": (200, 200)})
picam2.configure(config)

# カメラ開始
picam2.start()

# 画像を撮影
image = picam2.capture_array()

# カメラ停止
picam2.stop()

# 画像を確認（必要に応じて保存）
cv2.imwrite("captured_image_200.jpg", image)

# Thonnyで簡単に表示する
from PIL import Image
img = Image.fromarray(image)
img.show()
