#!/usr/bin/python3
'''
    API endpoint for the State model
'''
from api.v1.views import app_views
from flask import jsonify, request, abort
from flask import Flask
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
        # return jsonify(states)
        return json.dumps(states, indent=4)
    
    if request.method == 'POST':
        data = request.get_json()

        if data is None:
            abort(400, 'Not a JSON')
        if data.get("name") is None:
            abort(400, 'Missing name')
        new_state = State(**data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def state_id(state_id=None):
    '''
    Gets a single state from the storage engines
    '''
    state = storage.get(State, f"{state_id}")
    if state is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(state.to_dict())
    
    if request.method == 'DELETE':
        state.delete()
        del state
        return jsonify({})
    
    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        for attr, value in data.items():
            if attr not in ['id', 'created_at', 'updated_at']:
                setattr(state, attr, value)
        state.save()
        return jsonify(state.to_dict())
