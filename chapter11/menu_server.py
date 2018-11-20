from flask import Flask, render_template
from robot_modes import RobotModes

# A Flask App contains all its routes.
app = Flask(__name__)
# Prepare our robot modes for use
mode_manager = RobotModes()

def render_menu(message=None):
    """Render the menu screen, with an optional status message"""
    return render_template('menu.html', menu=mode_manager.menu_config, message=message)

# These are the Flask routes - the different places we can go to in our browser.

@app.route("/")
def index():
    return render_menu()

@app.route("/run/<mode_name>")
def run(mode_name):
    # Use our robot app to run something with this mode_name
    mode_manager.run(mode_name)
    return render_menu(message="%s running" % mode_name)

@app.route("/stop")
def stop():
    # Tell our system to stop the mode it's in.
    mode_manager.stop()
    return render_menu(message='Stopped')

# Start the app running
app.run(host="0.0.0.0", debug=True)
