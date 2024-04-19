#!/usr/bin/python3
""" Cities API routes """

from api.v1.views import app_views
from flask import abort
from flask import jsonify
from flask import request
from models import storage
from models.state import City
from models.state import State


# GET all cities by state ID
# ============================================================================

@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def get_all_cities(state_id):
    """ Retrieves all cities by state ID """
    state = storage.get(State, state_id)

    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


# GET one city (id)
# ============================================================================

@app_views.route("cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_one_city(city_id):
    """ Retrieves a city by its id """
    city = storage.get(City, city_id)

    if city is None:
        abort(404)
    return jsonify(city.to_dict())


# DELETE one city (id)
# ============================================================================

@app_views.route("cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """ Deletes a city by its id """
    city = storage.get(City,  city_id)

    if city is None:
        abort(404)

    city.delete()
    storage.save()
    return jsonify({}), 200


# POST (create a city)
# ============================================================================

@app_views.route("states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def post_city(state_id):
    """ Creates a city using the state's id """
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    try:
        data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON: {}".format(str(e)))

    if data is None:
        abort(400, description="Not a JSON")

    if "name" not in data:
        abort(400, description="Missing name")

    data["state_id"] = state_id

    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


# PUT (update a city by its id)
# ============================================================================

@app_views.route("cities/<city_id>", methods=["PUT"], strict_slashes=False)
def put_city(city_id):
    """ Updates a city by its id """
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    try:
        data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON: {}".format(str(e)))

    if data is None:
        abort(400, description="Not a JSON")

    if "id" in data and data["id"] != city_id:
        abort(404, description="error: Not found")

    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(city, key, value)

    city.save()
    return jsonify(city.to_dict()), 200
