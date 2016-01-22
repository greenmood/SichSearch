from flask import render_template
from flask import Flask
from flask import request
from steamapi import getownedgames
from steamapi import choosegame
from PIL import Image
import io
from io import StringIO

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('hello.html')


@app.route('/', methods=['POST'])
def handleSteamid():
    steamid = request.form["steamid"]
    games = getownedgames('1EDB5F832945E4C16CCB727EE9394235', steamid)
    game = choosegame(games)
    print(game)
    image = Image.open(io.BytesIO(game["image"]))
    img = Image.new('RGB','200x200')
    return render_template('hello.html', image=image) + serve_pil_image(img)


def serve_pil_image(pil_img):
    img_io = StringIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


if __name__ == "__main__":
    app.run(debug=True)
