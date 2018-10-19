from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import cv2

size = (320, 240)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

def setup_camera():
    camera = PiCamera()
    camera.resolution = size
    camera.rotation = 180
    return camera

def start_stream(camera):
    image_storage = PiRGBArray(camera, size=size)

    cam_stream = camera.capture_continuous(image_storage, format="bgr", use_video_port=True)
    for raw_frame in cam_stream:
        yield raw_frame.array
        image_storage.truncate(0)

def get_encoded_bytes_for_frame(frame):
    result, encoded_image = cv2.imencode('.jpg', frame, encode_param)
    return encoded_image.tostring()

def get_largest_enclosing(masked_image):
    """Find the largest enclosing circle for all contours in a masked image"""
    # Find the contours of the image (outline points)
    contour_image = np.copy(masked_image)
    contours, _ = cv2.findContours(contour_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # Find enclosing circles
    circles = [cv2.minEnclosingCircle(cnt) for cnt in contours]
    # Filter for the largest one
    largest = (0, 0), 0
    for (x, y), radius in circles:
        if radius > largest[1]:
            largest = (int(x), int(y)), int(radius)
    return largest
