#!/usr/bin/python3
""" Amenity objects that handles all default RESTFul API actions """

from api.v1.views import app_views
from flask import abort
from flask import jsonify
from flask import request
from models import storage
from models.amenity import Amenity


# GET all Amenities
# ============================================================================
@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ Retrieves the list of all Amenity objects """
    amenities = storage.all(Amenity).values()

    list_amenities = [amenity.to_dict() for amenity in amenities]

    return jsonify(list_amenities)


# GET a amenity by id
# ============================================================================
@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_one_amenity(amenity_id):
    """ retrieves a amenitie by id """
    amenity = storage.all(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    return jsonify(amenity.to_dict())


# DELETE one amenity (id)
# ============================================================================
@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ delete a amenitie by id """
    amenity = storage.all(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    amenity.delete()
    storage.save()
    return jsonify({}), 200


# POST: create an amenity
# ============================================================================
@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ POST: create an amenity """
    try:
        data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON: {}".format(str(e)))

    if data is None:
        abort(400, description="Not a JSON")

    if "name" not in data:
        abort(400, description="Missing name")

    new_amenity = Amenity(** request.json)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


# PUT: update an amenity
# ============================================================================
@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ PUT: update an amenity """
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    try:
        data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON: {}".format(str(e)))

    if data is None:
        abort(400, description="Not a JSON")

    if "id" in data and data["id"] != amenity_id:
        abort(404, description="error: Not found")

    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)

    amenity.save()
    return jsonify(amenity.to_dict()), 200
