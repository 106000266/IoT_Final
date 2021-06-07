from flask import Flask, render_template, Response, request, redirect, url_for
from Data_Bridge import get_value
app = Flask(__name__)
valueA = 1
valueB = 0

@app.route('/')

def index():
    valueA = get_value()
    if valueA == 0:
        return render_template('index.html', p1 = 'FULL', p2 = valueB)
    elif valueB == 0:
        return render_template('index.html', p1 = valueA, p2 = 'FULL')
    else:
        return render_template('index.html', p1 = valueA, p2 = valueB)

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 16628)
