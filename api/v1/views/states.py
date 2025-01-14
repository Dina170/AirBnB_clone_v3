#!/usr/bin/python3
"""states view"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.state import State


@app_views.route('/states/', strict_slashes=False)
def states_list():
    """Retrieves the list of all State objects"""
    return jsonify([obj.to_dict() for obj in storage.all(State).values()])


@app_views.route("/states/", methods=["POST"])
def create_state():
    """Creates a State"""
    if not request.json:
        abort(400, "Not a JSON")
    if "name" not in request.json:
        abort(400, "Missing name")
    obj = State(**request.get_json())
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route("/states/<state_id>")
def get_state(state_id):
    """Retrieves a State object"""
    obj = storage.get(State, state_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state(state_id):
    """Updates a State object"""
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    for k, v in request.get_json().items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(obj, k, v)
    obj.save()
    return jsonify(obj.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """Deletes a State object"""
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({})
