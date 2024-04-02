#!/usr/bin/python3
'''
    API endpoint for the State model
'''
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
import json
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def state_no_id():
    '''
    handles GET requests for the states api endpoint
    '''
    if request.method == 'GET':
        states = storage.all('State')
        states = list(obj.to_dict() for obj in states.values())
        return json.dumps(states, indent=4)

    if request.method == 'POST':
        data = request.get_json()

        if data is None:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        if data.get("name") is None:
            return make_response(jsonify({"error": "Missing name"}), 400)
        new_state = State(**data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<string:state_id>',
                 methods=['GET', 'POST', 'DELETE', 'PUT'])
def state_id(state_id=None):
    '''
    Gets a single state from the storage engines
    '''
    state = storage.get(State, state_id)
    if state is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return json.dumps(state.to_dict(), indent=4)

    if request.method == 'DELETE':
        state.delete()
        storage.save()
        return jsonify({})

    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        for attr, value in data.items():
            if attr not in ['id', 'created_at', 'updated_at']:
                setattr(state, attr, value)
        state.save()
        return json.dumps(state.to_dict(), indent=4)
