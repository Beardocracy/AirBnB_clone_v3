#!/usr/bin/python3
"""
script that handles RESTful API actions for Reviews
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place


@app_views.route('/api/v1/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def list_reviews(place_id):
    """ lists reviews for a place in json format """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews_list = []
    for review in storage.all("Review").values():
        if review.place_id == place_id:
            reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route('/api/v1/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """ retrieves a review """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/api/v1/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ deletes a review object """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/api/v1/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ creates a review object """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    review_json = request.get_json()
    if review_json is None:
        abort(400, {"Not a JSON"})
    if 'user_id' not in review_json:
        abort(400, {"Missing user_id"})
    user_id = review_json["user_id"]
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    if 'text' not in review_json:
        abort(400, {"Missing text"})
    review_json["place_id"] = place_id
    new_review = Review(**review_json)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/api/v1/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """ updates a review object """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    review_json = request.get_json()
    if review_json is None:
        abort(400, {"Not a JSON"})
    ignore_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for key, value in review_json.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
