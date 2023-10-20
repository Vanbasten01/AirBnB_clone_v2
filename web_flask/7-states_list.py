#!/usr/bin/pyhton3
""" a script that starts a flask application."""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def statespost():
    """ it renders a page with all states in the db ordred by their names"""
    states = list(storage.all(State).values())
    sorted_states = sorted(states, key=lambda state: state.name)
    return render_template('7-states_list.html', states=sorted_states)


@app.teardown_appcontext
def teardowndb(exception):
    """it ends the sqlalchemy session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
