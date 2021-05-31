from flask import Flask, render_template

app = Flask(__name__)
valueA = 2
valueB = 2

def get_value_A(keyword):
    valueA = keyword

def get_value_B(keyword):
    valueB = keyword

@app.route('/')
def index():
    if valueA == 0:
        return render_template('index.html', p1 = 'FULL', p2 = valueB)
    elif valueB == 0:
        return render_template('index.html', p1 = valueA, p2 = 'FULL')
    else:
        return render_template('index.html', p1 = valueA, p2 = valueB)

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 16628)
