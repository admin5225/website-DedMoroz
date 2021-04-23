from flask import Flask, url_for, request, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/perses')
def perses():
    return render_template('perses.html')


@app.route('/game')
def game():
    return render_template('game.html')


if __name__ == '__main__':
    app.run(port=8045, host='127.0.0.1')
