#!/usr/bin/python3
""" Blueprint description for state """

from models.state import State
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route('/api/v1/states', strict_slashes=False)
def list_all_states():
    """ Lists all states in JSON """
    all_states = []
    for state in storage.all('State').values():
        all_states.append(state.to_dict())
    return jsonify(all_states)
