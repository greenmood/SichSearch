from flask import render_template
from flask import Flask
from flask import request
from steamapi import getownedgames

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('hello.html')


@app.route('/', methods=['POST'])
def handleSteamid():
    steamid = request.form["steamid"]
    games = getownedgames('1EDB5F832945E4C16CCB727EE9394235', steamid)
    result = ''
    for game in games:
        result += str(game['appid'])
        result += ' '
    return render_template('hello.html') + result

if __name__ == "__main__":
    app.run(debug=True)
