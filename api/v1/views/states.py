#!/usr/bin/python3
""" Blueprint description for state """

from models.state import State
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
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


@app_views.route('/api/v1/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Deletes a state """
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        abort(404)
    state_obj.delete()
    storage.save()
    return {}


@app_views.route('/api/v1/states', methods=['POST'],
                 strict_slashes=False)
def add_state():
    """ Adds a new state """
    state_json = request.get_json()
    if not state_json:
        abort(400, {'Not a JSON'})
    if 'name' not in state_json:
        abort(400, {'Missing name'})
    state = State(**state_json)
    storage.new(state)
    storage.save()
    return state.to_dict(), 201


@app_views.route('/api/v1/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """ Updates a state """
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    json_info = request.get_json()
    if not json_info:
        abort(400, {'Not a JSON'})
    for k, v in json_info.items():
        setattr(state, k, v)
    storage.save()
    return state.to_dict()
