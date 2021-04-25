from flask import Flask, url_for, request, render_template
from mongodb import mdb, search_or_save_user, save_user_info

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


@app.route('/users')
def users():
    all_info = list(mdb.users.find({}))
    print(all_info)
    return render_template('users.html', info=all_info)


if __name__ == '__main__':
    app.run(port=8045, host='127.0.0.1')