#!/usr/bin/python3
"""User objets that handles all default RestFul API actions"""
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, abort


# GET all users
# ============================================================================
@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""
    users = storage.all(User).values()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list)


# GET one user (id)
# ============================================================================
@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


# DELETE one user (id)
# ============================================================================
@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


# POST (create a user)
# ============================================================================
@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Creates a User"""
    req_json = request.get_json()
    if req_json is None:
        abort(400, description="Not a JSON")
    if "email" not in request.get_json():
        abort(400, description="Missing email")
    if "password" not in request.get_json():
        abort(400, description="Missing password")
    new_user = User(**request.json)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


# PUT (update a user)
# ============================================================================
@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    req_json = request.get_json()
    if req_json is None:
        abort(400, description="Not a JSON")
    ignore_key = ["id", "email", "created_at", "updated_at"]
    for key, value in request.json.items():
        if key not in ignore_key:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
