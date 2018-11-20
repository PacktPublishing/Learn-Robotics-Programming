import time

from image_app_core import start_server_process, get_control_instruction, put_output_image
import pi_camera_stream

def controlled_image_server_behavior():
    # Setup the camera
    camera = pi_camera_stream.setup_camera()
    # allow the camera to warmup
    time.sleep(0.1)
    # Send frames from camera to server
    for frame in pi_camera_stream.start_stream(camera):
        encoded_bytes = pi_camera_stream.get_encoded_bytes_for_frame(frame)
        put_output_image(encoded_bytes)
        # Check any control instructions
        instruction = get_control_instruction()
        if instruction == "exit":
            print("Stopping")
            return

process = start_server_process('control_image_behavior.html')
controlled_image_server_behavior()
