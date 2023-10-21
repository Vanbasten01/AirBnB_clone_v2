#!/usr/bin/python3
""" a script that starts a flask application."""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def statepost():
    """ it renders a page with all states in DB """
    states = list(storage.all(State).values())
    sorted_states = sorted(states, key=lambda state: state.name)
    return render_template('9-states.html', states=sorted_states)


@app.route('/states/<id>', strict_slashes=False)
def states(id):
    """ it renders a page with all cities related
        to a specified state's id if found otherwise it displays a
        Not found message.
    """
    cities = []
    count = 0
    states = list(storage.all(State).values())
    for state in states:
        if state.id == str(id):
            count = 1
            break
    Cities = list(storage.all(City).values())
    for city in Cities:
        if city.state_id == state.id:
            cities.append(city)
    cities = sorted(cities, key=lambda city: city.name)
    if count:
        return render_template('9-states.html', state=state, cities=cities)
    return render_template('9-states.html', state=None, cities=None)


@app.teardown_appcontext
def teardowndb(exception):
    """it ends the sqlalchemy session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
