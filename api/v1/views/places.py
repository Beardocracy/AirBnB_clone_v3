#!/usr/bin/python3
"""
script that handles RESTful API actions for Place
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.state import State
from os import getenv


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


@app_views.route('/api/v1/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ deletes a place object """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/api/v1/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ creates a place object """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    place_json = request.get_json()
    if place_json is None:
        abort(400, {"Not a JSON"})
    if 'user_id' not in place_json:
        abort(400, {"Missing user_id"})
    user_id = place_json["user_id"]
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    if 'name' not in place_json:
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
    place_json = request.get_json()
    if place_json is None:
        abort(400, {"Not a JSON"})
    ignore_keys = ["id", "user_id", "created_at", "updated_at", "city_id"]
    for key, value in place_json.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/api/v1/places_search', methods=['POST'],
                 strict_slashes=False)
def search_places():
    """ Returns all places based on search parameters """
    json_info = request.get_json()
    if json_info is None:
        abort(400, {"Not a JSON"})
    state_ids = []
    city_ids = []
    amenity_ids = []
    places = []
    state_places = []
    city_list = []

    if "states" in json_info:
        state_ids = json_info["states"]
        for state_id in state_ids:
            state = storage.get("State", state_id)
            if state:
                for city in storage.all("City").values():
                    if city.state_id == state_id:
                        city_list.append(city.id)
        if len(city_list) != 0:
            for place in storage.all("Place").values():
                if place.city_id in city_list:
                    places.append(place)

    if "cities" in json_info:
        city_ids = json_info["cities"]
        for city_id in city_ids:
            for place in storage.all("Place").values():
                if place.city_id == city_id and place not in places:
                    places.append(place)

    if len(places) == 0:
        places = storage.all("Place").values()
    place_matches = list(places).copy()
    if "amenities" in json_info:
        amenity_ids = json_info["amenities"]
        for amenity_id in amenity_ids:
            for place in places:
                if getenv("HBNB_TYPE_STORAGE") == "db":
                    place_amenity_ids = [am.id for am in place.amenities]
                    if amenity_id not in place_amenity_ids:
                        if place in place_matches:
                            place_matches.remove(place)
                else:
                    if amenity_id not in place.amenity_ids:
                        if place in place_matches:
                            place_matches.remove(place)

    final_list = []
    for pm in place_matches:
        final_list.append(pm.to_dict())
    for pl in final_list:
        if "amenities" in pl:
            del pl["amenities"]

    return jsonify(final_list)
