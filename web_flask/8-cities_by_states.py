#!/usr/bin/python3
"""script that starts a Flask web application: Cities by states"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    """ function thats Display Cities by states """
    all_states = storage.all('State')
    all_states = dict(sorted(
        all_states.items(),
        key=lambda item: item[1].name))
    return render_template('8-cities_by_states.html', states=all_states)


@app.teardown_appcontext
def teardown_db(exception):
    """ close sqlalchemy session """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
