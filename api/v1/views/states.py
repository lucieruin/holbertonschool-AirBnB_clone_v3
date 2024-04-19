#!/usr/bin/python3
""" States API routes """

from api.v1.views import app_views
from flask import abort
from flask import jsonify
from flask import request
from models import storage
from models.state import State


# GET all states
# ============================================================================

@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_all_states():
    """ Retrieves all states """
    states = storage.all(State).values()

    list_states = [state.to_dict() for state in states]

    return jsonify(list_states)


# GET one state (id)
# ============================================================================

@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_one_state(state_id):
    """ Retrieves a state by its id """
    state = storage.get(State, state_id)

    if state is None:
        abort(404)
    return jsonify(state.to_dict())


# DELETE one state (id)
# ============================================================================

@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """ Deletes a state by its id """
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    state.delete()
    storage.save()
    return jsonify({}), 200


# POST (create a state)
# ============================================================================

@app_views.route("/states", methods=["POST"], strict_slashes=False)
def post_state():
    """ Creates a state """
    try:
        data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON: {}".format(str(e)))

    if data is None:
        abort(400, description="Not a JSON")

    if "name" not in data:
        abort(400, description="Missing name")

    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


# PUT (update a state)
# ============================================================================

@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def put_state(state_id):
    """ Updates a state by its id """
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, description="Not a JSON")

    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)

    state.save()
    return jsonify(state.to_dict()), 200
