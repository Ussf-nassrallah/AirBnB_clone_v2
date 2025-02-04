#!/usr/bin/python3
"""
List of states by :
  using storage for fetching data from the storage engine
  (FileStorage or DBStorage)
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def states_list():
    """
    display a HTML page thats contain states list
    """
    states = sorted(list(storage.all("State").values()), key=lambda x: x.name)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown_db(exception):
    """ close sqlalchemy session """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
