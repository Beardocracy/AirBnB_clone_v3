#!/usr/bin/python3
"""
script that handles RESTful API actions for Amenities
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.amenity import Amenity
from models.place import Place
from os import getenv


@app_views.route('/api/v1/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def list_amenities_of_a_place(place_id):
    """ lists amenities for a place in json format """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenities_list = []
    amenities_id_list = []
    if getenv("HBNB_TYPE_STORAGE") == "db":
        amenities_list = [am.to_dict() for am in place.amenities]
        return jsonify(amenities_list)
    else:
        if "amenity_ids" in place.to_dict().keys():
            amenities_id_list = place.to_dict()["amenity_ids"]
        else:
            return jsonify([])
    for amenity_id in amenities_id_list:
        amenity = storage.get('Amenity', amenity_id)
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route('/api/v1/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def remove_amenity_connection(place_id, amenity_id):
    """ deletes a amenity objects connection to a place """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity in place.amenities:
            place.amenities.remove(amenity)
            place.save()
            return jsonify({}), 200
    else:
        if "amenity_ids" in place.to_dict().keys():
            if amenity_id in place.amenity_ids:
                place.amenity_ids.remove(amenity_id)
                place.save()
                return jsonify({}), 200
            else:
                abort(404)
    return jsonify({}), 200


@app_views.route('/api/v1/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def create_amenity_connection(place_id, amenity_id):
    """ creates a amenity object connection to a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = storage.get('Amenity', amenity_id)
    if not amenity:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict())
        else:
            place.amenities.append(amenity)
            place.save()
            return jsonify(amenity.to_dict()), 201
    else:
        if "amenity_ids" in place.__dict__.keys():
            if amenity_id in place.amenity_ids:
                return jsonify(amenity.to_dict()), 200
            place.amenity_ids.append(amenity_id)
            place.save()
            return jsonify(amenity.to_dict()), 201
        else:
            place.__dict__.update({"amenity_ids": [amenity_id]})
            place.save()
            return jsonify(amenity.to_dict()), 201
    storage.save()
    return jsonify(amenity.to_dict()), 201
