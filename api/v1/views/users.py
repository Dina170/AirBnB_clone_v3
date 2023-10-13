#!/usr/bin/python3
"""users view"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def users():
    """Retrieves the list of all users objects"""
    return jsonify([obj.to_dict() for obj in storage.all(User).values()])


@app_views.route("/users/<user_id>")
def get_user(user_id):
    """Retrieves an user object"""
    obj = storage.get(User, user_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Deletes an user object"""
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({})


@app_views.route("/users", strict_slashes=False,
                 methods=["POST"])
def create_user():
    """Creates an user"""
    if not request.json:
        abort(400, "Not a JSON")
    if "email" not in request.json:
        abort(400, "Missing email")
    if "password" not in request.json:
        abort(400, "Missing password")
    obj = User(**request.get_json())
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    """Updates an user object"""
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    for k, v in request.get_json().items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(obj, k, v)
    obj.save()
    return jsonify(obj.to_dict())
