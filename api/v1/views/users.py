#!/usr/bin/python3
""" Blueprint description for users """

from models.user import User
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage


@app_views.route('/api/v1/users', strict_slashes=False)
def list_all_users():
    """ Lists all users in JSON """
    all_users = []
    for user in storage.all('User').values():
        all_users.append(user.to_dict())
    return jsonify(all_users)


@app_views.route('/api/v1/users/<user_id>', strict_slashes=False)
def list_user_by_id(user_id):
    """ List a user if the id exists """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/api/v1/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes a user """
    user_obj = storage.get('User', user_id)
    if user_obj is None:
        abort(404)
    user_obj.delete()
    storage.save()
    return {}, 200


@app_views.route('/api/v1/users', methods=['POST'],
                 strict_slashes=False)
def add_user():
    """ Adds a new user """
    user_json = request.get_json()
    if not user_json:
        abort(400, {'Not a JSON'})
    if 'name' not in user_json:
        abort(400, {'Missing name'})
    if 'email' not in user_json:
        abort(400, {'Missing email'})
    if 'password' not in user_json:
        abort(400, {'Missing password'})
    user = User(**user_json)
    storage.new(user)
    storage.save()
    return user.to_dict(), 201


@app_views.route('/api/v1/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """ Updates a user """
    user = storage.get('User', user_id)
    if not user:
        abort(404)
    json_info = request.get_json()
    if not json_info:
        abort(400, {'Not a JSON'})
    for k, v in json_info.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, k, v)
    storage.save()
    return user.to_dict(), 200
