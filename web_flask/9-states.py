#!/usr/bin/python3
"""script that starts a Flask web application: Cities by states"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route("/states", strict_slashes=False)
@app.route("/states/<id>", strict_slashes=False)
def states(id=None):
    """ function thats Display states and state by id """
    all_states = storage.all('State')
    if id is not None:
        id = 'State.' + id
    return render_template('9-states.html', states=all_states, id=id)


@app.teardown_appcontext
def teardown_db(exception):
    """ close sqlalchemy session """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
