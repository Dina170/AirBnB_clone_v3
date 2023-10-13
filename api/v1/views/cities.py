#!/usr/bin/python3
"""cities view"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def cities_by_state(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify([obj.to_dict() for obj in state.cities])


@app_views.route("/cities/<city_id>")
def get_city(city_id):
    """Retrieves a City object"""
    obj = storage.get(City, city_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """Deletes a City object"""
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states/<state_id>/cities/", strict_slashes=False,
                 methods=["POST"])
def create_city(state_id):
    """Creates a City"""
    print("id inside createcity ", state_id)
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    if "name" not in request.json:
        abort(400, "Missing name")
    obj = City(**request.get_json())
    obj.state_id = state_id
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    """Updates a City object"""
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    for k, v in request.get_json().items():
        if k not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(obj, k, v)
    obj.save()
    return jsonify(obj.to_dict())
