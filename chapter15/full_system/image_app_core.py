"""The flask/webserver part is slightly independent of the behavior,
allowing the user to "tune in" to see, but should not stop the
robot running"""
import time
from multiprocessing import Process, Queue

from flask import (Flask, render_template,
    Response, redirect, request)


app = Flask(__name__)
control_queue = Queue()
display_queue = Queue(maxsize=2)
display_template = 'image_server'

@app.route('/')
def index():
    return render_template(display_template)

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = "no-cache, no-store, must-revalidate"
    return response
    
def frame_generator():
    """This is our main video feed"""
    while True:
        # at most 20 fps
        time.sleep(0.05)
        # Get (wait until we have data)
        encoded_bytes = display_queue.get()
        # Need to turn this into http multipart data.
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + encoded_bytes + b'\r\n')

@app.route('/display')
def display():
    return Response(frame_generator(),
        mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/exit')
def handle_exit():
    control_queue.put('exit')
    menu_server = request.url_root.replace('5001', '5000')
    return redirect(menu_server, code=302)

@app.route('/control/<path:control_name>')
def control(control_name):
    control_queue.put(control_name)
    return Response('queued')

def start_server_process(template_name):
    """Start the process, call .terminate to close it"""
    global display_template
    display_template = template_name
    server = Process(target=app.run, kwargs={"host": "0.0.0.0", "port": 5001})
    server.daemon = True
    server.start()
    print("App should be running")
    print("Process info name:", server.name, " alive:", server.is_alive())
    return server

def put_output_image(encoded_bytes):
    """Queue an output image"""
    if display_queue.empty():
        display_queue.put(encoded_bytes)

def get_control_instruction():
    """Get control instructions from the web app, if any"""
    if control_queue.empty():
        return None
    else:
        return control_queue.get()
