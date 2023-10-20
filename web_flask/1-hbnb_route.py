#!/usr/bin/python3
""" script that starts a Flask web application """
from flask import FLASK

app = FLASK(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """
    /: display “Hello HBNB!”
    """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """ /hbnb: display “HBNB” """
    return "HBNB"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
