from flask import render_template
from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('hello.html')


@app.route('/', methods=['POST'])
def handleSteamid():
    myvar = request.form["steamid"]
    return render_template('hello.html') + myvar

if __name__ == "__main__":
    app.run(debug=True)
