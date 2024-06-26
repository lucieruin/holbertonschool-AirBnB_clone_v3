#!/usr/bin/python3
""" Place objects that handles all default RESTFul API actions """

from api.v1.views import app_views
from flask import abort
from flask import jsonify
from flask import request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


# GET all places (by city id)
# ============================================================================
@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_place(city_id):
    """ Retrieves the list of all Place objects of a City """
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    list_places = [place.to_dict() for place in city.places]

    return jsonify(list_places)


# GET one place by place_id
# ============================================================================
@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """ Retrieves a Place object """
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    return jsonify(place.to_dict())


# DELETE: delete one place by id
# ============================================================================
@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ delete a place by id """
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    place.delete()
    storage.save()
    return jsonify({}), 200


# POST: create a place by id
# ============================================================================
@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """ create a place """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    try:
        data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON: {}".format(str(e)))

    if data is None:
        abort(400, description="Not a JSON")

    if "user_id" not in data:
        abort(400, description="Missing user_id")

    user = storage.get(User, data["user_id"])
    if user is None:
        abort(404)

    if "name" not in data:
        abort(400, description="Missing name")

    data["city_id"] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


# PUT: update a place by id
# ============================================================================
@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def put_places(place_id):
    """ Updates a place by its id """
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    try:
        data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON: {}".format(str(e)))

    if data is None:
        abort(400, description="Not a JSON")

    if "id" in data and data["id"] != place_id:
        abort(404, description="error: Not found")

    for key, value in data.items():
        if key not in ["id", "user_id", "created_at", "updated_at"]:
            setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict()), 200
