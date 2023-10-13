#!/usr/bin/python3
"""Place view"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def review_by_place(place_id):
    """Retrieves the list of all reviews objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([obj.to_dict() for obj in place.reviews])


@app_views.route("/reviews/<review_id>")
def get_review(place_id):
    """Retrieves a review object"""
    obj = storage.get(Review, review_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    """Deletes a review object"""
    obj = storage.get(Review, review_id)
    if not obj:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({})


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=["POST"])
def create_review(place_id):
    """Creates a review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    if "user_id" not in request.json:
        abort(400, "Missing user_id")
    user = storage.get(User, request.json['user_id'])
    if not user:
        abort(404)
    if "text" not in request.json:
        abort(400, "Missing text")
    obj = Review(**request.get_json())
    obj.place_id = place_id
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def update_review(review_id):
    """Updates a review object"""
    obj = storage.get(Review, review_id)
    if not obj:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    for k, v in request.get_json().items():
        if k not in ["id", "created_at", "updated_at", "user_id", "place_id"]:
            setattr(obj, k, v)
    obj.save()
    return jsonify(obj.to_dict())
