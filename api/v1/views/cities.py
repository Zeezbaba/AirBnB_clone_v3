#!/usr/bin/python3
'''
    API endpoint for the handling CRUD operations
    for the city model
'''
from api.v1.views import app_views
from flask import request, abort, Flask, make_response
import json
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<string:state_id>/cities', methods=['GET', 'POST'], strict_slashes=False)
def cities_from_state(req, state_id):
    '''
    Serves endpoints for city from a state objs
    '''
    state_obj = storage.get(State, f"{state_id}")
    if state_obj is None:
        abort(404)
    if req.method == 'GET':
        cities = []
        for city in state_obj.cities:
            cities.append(city.to_dict)
        return json.dumps(cities, indent=4)
    
    if request.method == 'POST':
        payload = request.get_json()
        if payload is None:
            return make_response({'error': 'Not a JSON'}, 404)
        if payload.get('name') is None:
            return make_response(json.dumps({'error': 'Missing name'}, indent=4), 400)
        kwargs = payload
        kwargs['state_id'] = state_id
        city = City(**kwargs)
        city.save()
        return make_response(json.dumps(city.to_dict(), indent=4), 201)


@app_views.route('/cities/<city_id>', methods=['GET', 'POST', 'DELETE', 'PUT'], strict_slashes=False)
def cities_id(city_id=None):
    '''
    Serves requests for city API endpoint
    '''
    city_obj = storage.get(City, f"{city_id}")
    if city_obj is None:
        abort(404)
    
    if request.method == 'GET':
        return json.dumps(city_obj.to_dict(), indent=4)
    
    if request.method == 'DELETE':
        city_obj.delete()
        storage.save()
        return json.dumps({})
    
    if request.method == 'PUT':
        payload = request.get_json()
        if payload is None:
            return make_response(json.dumps({'error': 'Not a JSON'}, indent=4), 400)
        for attr, value in payload.items():
            if attr not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city_obj, attr, value)
        city_obj.save()
        return json.dumps(city_obj.to_dict(), indent=4)
