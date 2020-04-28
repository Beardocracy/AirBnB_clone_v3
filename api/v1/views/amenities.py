#!/usr/bin/python3
""" Blueprint description for amenities """

from models.amenity import Amenity
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage


@app_views.route('/api/v1/amenities', strict_slashes=False)
def list_all_amenities():
    """ Lists all amenities in JSON """
    all_amenities = []
    for amenity in storage.all('Amenity').values():
        all_amenities.append(amenity.to_dict())
    return jsonify(all_amenities)


@app_views.route('/api/v1/amenities/<amenity_id>', strict_slashes=False)
def list_amenity_by_id(amenity_id):
    """ List a amenity if the id exists """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/api/v1/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes a amenity """
    amenity_obj = storage.get('Amenity', amenity_id)
    if amenity_obj is None:
        abort(404)
    amenity_obj.delete()
    storage.save()
    return {}


@app_views.route('/api/v1/amenities', methods=['POST'],
                 strict_slashes=False)
def add_amenity():
    """ Adds a new amenity """
    amenity_json = request.get_json()
    if not amenity_json:
        abort(400, {'Not a JSON'})
    if 'name' not in amenity_json:
        abort(400, {'Missing name'})
    amenity = Amenity(**amenity_json)
    storage.new(amenity)
    storage.save()
    return amenity.to_dict(), 201


@app_views.route('/api/v1/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Updates a amenity """
    amenity = storage.get('Amenity', amenity_id)
    if not amenity:
        abort(404)
    json_info = request.get_json()
    if not json_info:
        abort(400, {'Not a JSON'})
    for k, v in json_info.items():
        setattr(amenity, k, v)
    storage.save()
    return amenity.to_dict()
