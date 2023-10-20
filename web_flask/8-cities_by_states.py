#!/usr/bin/python3
""" a script that starts a flask application."""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def citiespost():
    """ it renders a page with all states in the db ordred by their names"""
    states = list(storage.all(State).values())
    cities = list(storage.all(City).values())
    sorted_states = sorted(states, key=lambda state: state.name)
    sorted_cities = sorted(cities, key=lambda city: city.name)
    return render_template(
            '8-cities_by_states.html', states=sorted_states,
            cities=sorted_cities)


@app.teardown_appcontext
def teardowndb(exception):
    """it ends the sqlalchemy session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
