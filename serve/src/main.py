from flask import Flask, request

app = Flask(__name__)


@app.route("/json/plant/<name>", methods=["GET", "POST"])
def plant(name):
    match request.method:
        case "GET":
            return {}
        case "POST":
            return {}


@app.route("/json/location/<name>", methods=["GET", "POST"])
def location(name):
    match request.method:
        case "GET":
            return {}
        case "POST":
            return {}


if __name__ == '__main__':
    app.run(host="0.0.0.0")
