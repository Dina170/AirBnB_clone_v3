#!/usr/bin/python3
"""amenities view"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities')
def amenities():
    """Retrieves the list of all amenities objects"""
    return jsonify([obj.to_dict() for obj in storage.all(Amenity).values()])


@app_views.route("/amenities/<amenity_id>")
def get_amenity(amenity_id):
    """Retrieves an amenity object"""
    obj = storage.get(Amenity, amenity_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """Deletes an amenity object"""
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({})


@app_views.route("/amenities", strict_slashes=False,
                 methods=["POST"])
def create_amenity():
    """Creates an amenity"""
    if not request.json:
        abort(400, "Not a JSON")
    if "name" not in request.json:
        abort(400, "Missing name")
    obj = Amenity(**request.get_json())
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def update_amenity(amenity_id):
    """Updates an amenity object"""
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    for k, v in request.get_json().items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(obj, k, v)
    obj.save()
    return jsonify(obj.to_dict())
