#!/usr/bin/python3
"""Review objects that handles all default RestFul API actions"""
from models.review import Review
from models.place import Place
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User


# GET all reviews
# ============================================================================
@app_views.route("/places/<place_id>/reviews", methods=["GET"], strict_slashes=False)
def get_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = storage.all(Review).values()
    reviews_list = [review.to_dict() 
                    for review in reviews if review.place_id == place_id]
    return jsonify(reviews_list)


# GET one review (id)
# ============================================================================
@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


# DELETE one review (id)
# ============================================================================
@app_views.route("/reviews/<review_id>", methods=["DELETE"], strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


# POST (create a review)
# ============================================================================
@app_views.route("/places/<place_id>/reviews", methods=["POST"], strict_slashes=False)
def create_review(place_id):
    """Creates a Review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    req_json = request.get_json()
    if req_json is None:
        abort(400, description="Not a JSON")
    if "user_id" not in request.get_json():
        abort(400, description="Missing user_id")
    user = storage.get(User, request.get_json["user_id"])
    if user is None:
        abort(404)
    if "text" not in req_json():
        abort(400, description="Missing text")
    req_json["place_id"] = place_id
    review = Review(**req_json)
    review.save()
    return jsonify(review.to_dict()), 201


# PUT (update a review)
# ============================================================================
@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    req_json = request.get_json()
    if req_json is None:
        abort(400, description="Not a JSON")
    ignore_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for key, value in req_json.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
