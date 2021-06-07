from flask import Flask, render_template, Response, request, redirect, url_for
from Data_Bridge import control

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('control_gate.html')

@app.route("/forward/", methods=['POST'])
def open_gate():
    control()
    return render_template('control_gate.html')

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 80)
