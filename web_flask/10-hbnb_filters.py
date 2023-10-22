#!/usr/bin/python3
"""
Script that starts a Flask web application:
  hbnb_filter
"""
from flask import Flask, render_template
from models import *
from models import storage


app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """ document """
    all_states = storage.all('State').values()
    all_amenities = storage.all('Amenity').values()
    return render_template('10-hbnb_filters.html', states=all_states,
                           amenities=all_amenities)


@app.teardown_appcontext
def teardown_db(exception):
    """close Sqlalchemy session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
