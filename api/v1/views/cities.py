#!/usr/bin/python3
"""
script that handles RESTful API actions for City
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/api/v1/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def list_cities(state_id):
    """ lists all cities in JSON format """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    city_list = []
    for city in storage.all("City").values():
        if city.state_id == state_id:
            city_list.append(city.to_dict())
    return jsonify(city_list), 200


@app_views.route('/api/v1/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """ retrieves a city """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/api/v1/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ deletes a city object """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/api/v1/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ creates a city object """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    city_json = request.get_json()
    if city_json is None:
        abort(400, {"Not a JSON"})
    if 'name' not in city_json:
        abort(400, {"Missing name"})
    city_json["state_id"] = state_id
    new_city = City(**city_json)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/api/v1/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """ updates a city object """
    city_json = request.get_json()
    if city_json is None:
        abort(400, {"Not a JSON"})
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    ignore_keys = ["id", "created_at", "updated_at", "state_id"]
    for key, value in city_json.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
