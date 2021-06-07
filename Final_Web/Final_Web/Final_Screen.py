from flask import Flask, render_template, Response, request, redirect, url_for, jsonify
from Data_Bridge import get_value
app = Flask(__name__)
valueB = 0

@app.route('/_stuff', methods = ['GET'])
def stuff():
    valueA = get_value()
    if valueA == 0:
        return jsonify(result = 'FULL')
    else:
        return jsonify(result = valueA)


@app.route('/')
def index():
    if valueB == 0:
        return render_template('index.html', p2 = 'FULL')
    else:
        return render_template('index.html', p2 = valueB)

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 16628)
