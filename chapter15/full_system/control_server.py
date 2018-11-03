from flask import Flask, render_template, request, Response, send_from_directory, send_file


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("touch_sliders.html")

@app.route('/motor/<name>', methods=['POST'])
def set_motor(name):
    print("Setting motor {} to {}".format(name, request.form['speed']))
    return ''

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/display')
def display():
    return send_file('static/display_sample.jpg')

app.run(**{"host": "0.0.0.0", "port": 5001, "debug": True})
