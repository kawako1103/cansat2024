import cv2

camera = cv2.VideoCapture(0)

if not camera.isOpend():
    print("not tsunageru camera")
    exit()
    
try:
    ret, frame = camera.read()
    
    if ret:
        resized_frame = cv2.resize(frame, (250, 250))
        
        output_file = "20241214_1.jpg"
        cv2.imwrite(output_File, resized_frame)
        print(f"save picture: {output_file}")
    else:
        print("cannot save picture")
        
finally:
    camera.release()