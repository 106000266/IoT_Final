from flask import Flask, render_template, Response, request, redirect, url_for
from Final_IoT import control_gate

app = Flask(__name__)
valueA = 2
valueB = 2

@app.route('/')
def index():
    return render_template('control_gate.html')

@app.route("/forward/", methods=['POST'])
def open_gate():
    control_gate()
    return render_template('control_gate.html')

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 80)
