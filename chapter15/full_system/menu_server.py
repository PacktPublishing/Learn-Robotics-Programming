import time
from flask import Flask, render_template, redirect, request
from robot_modes import RobotModes
from leds_8_apa102c import Leds

# A Flask App contains all its routes.
app = Flask(__name__)
# Prepare our robot modes for use
mode_manager = RobotModes()

leds = Leds()
leds.set_one(0, [0, 255, 0])
leds.show()

def render_menu(message=None):
    """Render the menu screen, with an optional status message"""
    return render_template('menu.html', menu=mode_manager.menu_config, message=message)

# These are the Flask routes - the different places we can go to in our browser.

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = "no-cache, no-store, must-revalidate"
    return response
    
@app.route("/")
def index():
    return render_menu()

@app.route("/run/<mode_name>")
def run(mode_name):
    global leds
    if leds:
        leds.clear()
        leds.show()
        leds = None

    # Use our robot app to run something with this mode_name
    mode_manager.run(mode_name)
    if mode_manager.should_redirect(mode_name):
        # Give the other process time to start
        time.sleep(3)
        # If it's not broken
        if mode_manager.is_running():
            # Now redirect
            new_url = request.url_root.replace('5000', '5001')
            return redirect(new_url)
        else:
           return render_menu(message="%s dead." % mode_name)
    return render_menu(message="%s running" % mode_name)

@app.route("/stop")
def stop():
    # Tell our system to stop the mode it's in.
    mode_manager.stop()
    return render_menu(message='Stopped')

# Start the app running
# if you enable debug, disable the reloader here.
app.run(host="0.0.0.0")

