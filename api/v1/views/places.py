#!/usr/bin/python3
"""Place view"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.city import City
from models.user import User
from models.place import Place


@app_views.route('/cities/<city_id>/places')
def places_by_city(city_id):
    """Retrieves the list of all Places objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify([obj.to_dict() for obj in city.places])


@app_views.route("/places/<place_id>")
def get_place(place_id):
    """Retrieves a place object"""
    obj = storage.get(Place, place_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """Deletes a Place object"""
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({})


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=["POST"])
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    if "user_id" not in request.json:
        abort(400, "Missing user_id")
    user = storage.get(User, request.json['user_id'])
    if not user:
        abort(404)
    if "name" not in request.json:
        abort(400, "Missing name")
    obj = City(**request.get_json())
    obj.city_id = city_id
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=["PUT"])
def update_place(place_id):
    """Updates a Place object"""
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    for k, v in request.get_json().items():
        if k not in ["id", "created_at", "updated_at", "user_id", "city_id"]:
            setattr(obj, k, v)
    obj.save()
    return jsonify(obj.to_dict())
