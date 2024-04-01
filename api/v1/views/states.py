#!/usr/bin/python3
"""
view for State objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def retrieve_states():
    """
    Retrieves the list of all State objects
    """
    all_states = [obj.to_dict() for obj in storage.all(State).values()]

    return jsonify(all_states)


@app_views.route("/states/<string:state_id>",  methods=["GET"],
                 strict_slashes=False)
def retrieve_state_id(state_id):
    """Retrieves a State object by id"""
    stateId = storage.get(State, state_id)
    if stateId is None:
        abort(404)
    return jsonify(stateId.to_dict())


@app_views.route("/states/<string:state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state_id(state_id):
    """Deletes a State object by id"""
    stateId = storage.get(State, state_id)
    if stateId is None:
        abort(404)
    storage.delete(stateId)
    storage.save()
    return jsonify({})


@app_views.route('/states/', methods=['POST'],
                 strict_slashes=False)
def create_state():
    """creates a state"""
    dict_json = request.get_json(silent=True)
    if dict_json is None:
        abort(400, 'Not a JSON')
    if "name" not in dict_json:
        abort(400, 'Missing name')

    created_state = State(**dict_json)
    created_state.save()
    return jsonify(created_state.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """creates a state"""
    dict_json = request.get_json(silent=True)
    if dict_json is None:
        abort(400, 'Not a JSON')
    stateId = storage.get(State, state_id)
    if stateId is None:
        abort(404)
    for key, value in dict_json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(stateId, key, value)
    storage.save()
    return jsonify(stateId.to_dict())
