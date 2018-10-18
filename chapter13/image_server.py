from flask import Flask, render_template, Response
import pi_camera_stream
import time


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('image_server.html')

def frames_for_camera():
    """This is our main video feed"""
    camera = pi_camera_stream.setup_camera()

    # allow the camera to warmup
    time.sleep(0.1)

    for frame in pi_camera_stream.start_stream(camera):
        encoded_bytes = pi_camera_stream.get_encoded_bytes_for_stream(frame)
        # Need to turn this into http multipart data.
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + encoded_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(frames_for_camera(),
        mimetype='multipart/x-mixed-replace; boundary=frame')

app.run(host="0.0.0.0", debug=True, port=5001)
