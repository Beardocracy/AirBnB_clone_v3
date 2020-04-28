#!/usr/bin/python3
"""
Blueprint description for index
"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route('/api/v1/status', strict_slashes=False)
def status():
    """ Returns status message """
    status = {"status": "OK"}
    return jsonify(status)


@app_views.route('/api/v1/stats', strict_slashes=False)
def obj_stats():
    """ Retrieves the number of each object by type """
    classes = {"amenities": "Amenity",
               "cities": "City",
               "places": "Place",
               "reviews": "Review",
               "states": "State",
               "users": "User"}
    for key, value in classes.items():
        classes[key] = storage.count(value)
    return jsonify(classes)
