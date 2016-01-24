from flask import render_template
from flask import Flask
from flask import request
from steamapi import getownedgames
from steamapi import choosegame
import os

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('hello.html')


@app.route('/', methods=['POST'])
def handleSteamid():
    steamid = request.form["steamid"]
    apikey = getApiKey()
    games = getownedgames(apikey, steamid)
    game = choosegame(games)
    image = game["image"]
    return render_template('hello.html', image=image)


def getApiKey():
    if os.path.isfile('apikey.txt'):
        f = open('apikey.txt', 'r')
        apikey = f.read().splitlines()[0]
        print(apikey)
        return apikey


if __name__ == "__main__":
    app.run(debug=True)
