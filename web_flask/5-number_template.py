#!/usr/bin/python3
""" script that starts a Flask web application """
from flask import Flask, render_template

app = Flask(__name__)


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


@app.route("/c/<text>", strict_slashes=False)
def cText(text):
    """
    /c/<text>: display “C ” followed by the value of the text
      variable (replace underscore _ symbols with a space )
    """
    return "C {}".format(text.replace("_", " "))


@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def pText(text="is cool"):
    """
    /python/<text>: display “Python ”, followed by the value
      of the text variable (replace underscore _ symbols with a space )
      The default value of text is “is cool”
    """
    return f"Python {text.replace('_', ' ')}"


@app.route("/number/<int:n>", strict_slashes=False)
def nNumber(n):
    """
    /number/<n>: display “n is a number” only if n is an integer
    """
    if isinstance(n, int):
        return f"{n} is a number"


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n):
    """
    display a HTML page only if n is an integer:
    """
    if isinstance(n, int):
        return render_template('5-number.html', n=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
