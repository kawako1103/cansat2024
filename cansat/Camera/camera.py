from PIL import Image
import numpy as np
import time
import os
from picamera2 import Picamera2
#from libcamera import controls

# Define image dimensions
height = 100
width = 100

class Camera:
    def __init__(self):
        # Create and initialize the Picamera2 instance
        self.picam2 = Picamera2()
        camera_config = self.picam2.create_still_configuration(main={"size": (height, width)})
        self.picam2.configure(camera_config)
        #self.picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
        self.picam2.start()
        print("Camera initialized.")

    def initialize_camera(self):
        # No additional initialization is needed since the camera is already initialized
        print("Camera already initialized.")

    def capture_and_save(self, filename=None):
        # Define the directory to save the captured images
        save_dir = os.path.dirname(__file__)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Generate a filename using the current timestamp if none is provided
        if filename is None:
            timeStamp = time.strftime("%Y%m%d-%H%M%S")
            filename = os.path.join(save_dir, f"img_{timeStamp}.jpg")
        
        # Capture and save the image
        self.picam2.capture_file(filename)
        print(f"Image captured and saved to {filename}.")
        return filename

    def greenthreshold_left_center_right(self, image_path, threshold=40):
        # Load the image
        image = Image.open(image_path)

        # Get image dimensions and extract the green channel
        width, height = image.size
        image_rgb = np.array(image)
        g_channel = image_rgb[:, :, 1]  # Extract green channel

        # Apply thresholding to create a binary image
        g_threshold = np.where(g_channel >= threshold, 255, 0).astype(np.uint8)  # Binarization

        # Save the thresholded image
        save_dir = os.path.dirname(__file__)
        threshold_image_path = os.path.join(save_dir, f"threshold_{os.path.basename(image_path)}")
        Image.fromarray(g_threshold).convert("L").save(threshold_image_path)
        print(f"Threshold processed image saved to {threshold_image_path}.")

        # Divide the image into three vertical sections (left, center, right)
        section_width = width // 3
        sections = [g_threshold[:, :section_width],
                    g_threshold[:, section_width:2*section_width],
                    g_threshold[:, 2*section_width:]]
        
        # Calculate the percentage of non-green areas in each section
        total_pixels = height * section_width
        counts = [np.sum(section == 0) for section in sections]
        percentages = [(count / total_pixels) * 100 for count in counts]

        # Determine the section with the least green content
        max_count_index = np.argmax(counts)
        sections_labels = ["Left", "Center", "Right"]
        most_greenless_section = sections_labels[max_count_index]

        # Print the percentage of non-green areas in each section
        for label, percent in zip(sections_labels, percentages):
            print(f"{label}: {percent:.2f}% greenless area")

        print(f"Most greenless section: {most_greenless_section}")
        return most_greenless_section, percentages

    def stop_camera(self):
        # Stop the camera preview and clean up resources
        self.picam2.stop()
        print("Camera stopped.")

if __name__ == "__main__":
    camera = Camera()
    try:
        # Capture an image and save it
        image_path = camera.capture_and_save()

        # Analyze the saved image for green content
        result, percentages = camera.greenthreshold_left_center_right(image_path)
        print(f"The area with the least green is: {result}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Stop the camera before exiting
        camera.stop_camera()
