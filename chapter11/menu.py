from flask import Flask
import subprocess
app = Flask(__name__)

class RobotModes(object):
    menu_config = {
        "avoid_behavior": ("Avoid Behavior", "avoid_behavior.py"),
        "circle_pan_tilt_behavior": ("Circle Head", "circle_pan_tilt_behavior.py"),
        "test_leds": ("Test LEDS", "leds_test.py"),
        "test_hcsr04": ("Test HC-SR04", "test_hcsr04.py"),
        "stop_at_line": ("Stop At Line", "stop_at_line.py"),
        "line_following_behavior": ("Line Following", "line_following_behavior.py"),
        "behavior_line": ("Drive In A Line", "behavior_line.py"),
        "behavior_path": ("Drive a Path", "behavior_path.py")
    }

    def __init__(self):
        self.current_process = None
    
    def run(self, mode_name):
        if not self.current_process or self.current_process.returncode is not None:
            self.current_process = subprocess.Popen(["python", self.menu_config[mode_name][1]])

    def stop(self):
        self.current_process.send_signal(subprocess.signal.SIGINT)
        self.current_process = None

robot_modes = RobotModes()

def show_menu(message=None):
    screen = "<h1>Choose a Menu<h1>"
    if message:
        screen += "<p>" + message + "</p>"

    screen += "<ul>"

    for item in robot_modes.menu_config:
        screen += "<li><a href='/run/{mode_name}'>{mode_text}</a></li>".format(mode_name=item, mode_text=robot_modes.menu_config[item][0])
    
    screen += "</ul>"
    return screen

@app.route("/")
def index():
    return show_menu()

@app.route("/run/<mode_name>")
def run(mode_name):
    robot_modes.run(mode_name)
    return "<b>Mode_name running</b><br><a href='/stop'>Stop</a>"

@app.route("/stop")
def stop():
    robot_modes.stop()
    return show_menu(message='Stopped')


app.run('0.0.0.0')

