#!/usr/bin/python3
""" Blueprint description for state """

from models.state import State
from api.v1.views import app_views
from flask import Flask, jsonify, abort
from models import storage


@app_views.route('/api/v1/states', strict_slashes=False)
def list_all_states():
    """ Lists all states in JSON """
    all_states = []
    for state in storage.all('State').values():
        all_states.append(state.to_dict())
    return jsonify(all_states)


@app_views.route('/api/v1/states/<state_id>', strict_slashes=False)
def list_state_by_id(state_id):
    """ List a state if the id exists """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())
