#!/usr/bin/python3
"""
script that handles RESTful API actions for Place
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place


@app_views.route('/api/v1/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def list_places(city_id):
    """ lists places in json format """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places_list = []
    for place in storage.all("Place").values():
        if place.city_id == city_id:
            places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('/api/v1/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """ retrieves a place """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/api/v1/place/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ deletes a place object """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/api/v1/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ creates a place object """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    place_json = request.get_json
    if place_json is None:
        abort(400, {"Not a JSON"})
    if 'user_id' not in place_json:
        abort(400, {"Missing user_id"})
    user_id = place_json["user_id"]
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    if not place_json["name"]:
        abort(400, {"Missing name"})
    place_json["city_id"] = city_id
    new_place = Place(**place_json)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/api/v1/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """ updates a city object """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    place_json = request.get_json
    if place_json is None:
        abort(400, {"Not a JSON"})
    ignore_keys = ["id", "created_at", "updated_at", "state_id"]
    for key, value in place_json.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
