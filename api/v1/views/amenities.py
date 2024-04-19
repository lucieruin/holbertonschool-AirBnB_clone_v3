#!/usr/bin/python3
""" Amenities API routes """

from api.v1.views import app_views
from flask import abort
from flask import jsonify
from flask import request
from models import storage
from models.amenity import Amenity


# GET all amenities
# ============================================================================

@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_all_amenities():
    """ Retrieves all amenities """
    amenities = storage.all(Amenity).values()

    list_amenities = [amenity.to_dict() for amenity in amenities]

    return jsonify(list_amenities)


# GET one amenity (id)
# ============================================================================

@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_one_amenity(amenity_id):
    """ Retrieves an amenity by its id """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    return jsonify(amenity.to_dict())


# DELETE one amenity (id)
# ============================================================================

@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes an amenity by its id """
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    amenity.delete()
    storage.save()
    return jsonify({}), 200


# POST (create an amenity)
# ============================================================================

@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def post_amenity():
    """ Creates an amenity """
    try:
        data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON: {}".format(str(e)))

    if data is None:
        abort(400, description="Not a JSON")

    if "name" not in data:
        abort(400, description="Missing name")

    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


# PUT (update an amenity by its id)
# ============================================================================

@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """ Updates an amenity by its id """
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
