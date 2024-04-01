#!/usr/bin/python3
'''
    API endpoint for the handling CRUD operations
    for the places model
'''
from api.v1.views import app_views
from flask import request, abort, Flask, make_response
import json
from models import storage
from models.place import Place
from models.user import User
from models.city import City
from models.amenity import Amenity
from models.state import State


@app_views.route('/cities/<string:city_id>/places', methods=['GET', 'POST'], strict_slashes=False)
def places_ops(city_id):
    '''
    Handles places CRUD ops
    '''
    if request.method == 'GET':
        city_obj = storage.get(City, f"{city_id}")
        if city_obj is None:
            abort(404)

        places = []
        for place in city_obj.places:
            places.append(place.to_dict())
        return json.dumps(places, indent=4)
    
    if request.method == 'POST':
        payload = request.get_json()
        if payload is None:
            return make_response(json.dumps({'error': 'Not a JSON'}, indent=4), 400)
        if payload.get('user_id') is None:
            return make_response(json.dumps({'error': 'Missing user_id'}, indent=4), 400)
        user = storage.get(User, payload['user_id'])
        if user is None:
            abort(404)
        if payload.get('name') is None:
            return make_response(json.dumps({'error': 'Missing name'}, indent=4), 400)
        payload['city_id'] = city_id
        new_place = Place(**payload)
        new_place.save()
        return make_response(json.dumps(new_place.to_dict(), indent=4), 201)


@app_views.route('/places/<string:place_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def places_id(place_id):
    '''
    Handles endpoint with place id
    '''
    place_obj = storage.get(Place, f"{place_id}")
    if place_obj is None:
        abort(404)
    if request.method == 'GET':
        return json.dumps(place_obj.to_dict(), indent=4)
    
    if request.method == 'DELETE':
        place_obj.delete()
        storage.save()
        return json.dumps({})

    if request.method == 'PUT':
        payload = request.get_json()
        if payload is None:
            return make_response(json.dumps({'error': 'Not a JSON'}, indent=4), 400)
        for attr, value in payload.items():
            if attr not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
                setattr(place_obj, attr, value)
        place_obj.save()
        return json.dumps(place_obj.to_dict(), indent=4)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    '''
    Search enpoint for places
    '''
    if request.get_json is None:
        return make_response(json.dumps({'error': 'Not a JSON'}, indent=4), 400)
    
    params = request.get_json()
    states = params.get('states', [])
    cities = params.get('cities', [])
    amenities = params.get('amenities', [])
    amenity_objects = []
    for amenity_id in amenities:
        amenity = storage.get(Amenity, f"{amenity_id}")
        if amenity:
            amenity_objects.append(amenity)
    
    if states == cities == []:
        places = storage.all('Place').values()
    else:
        places = []
        for state_id in states:
            state = storage.get(State, f"{state_id}")
            state_cities = state.cities
            for city in state_cities:
                if city.id not in cities:
                    cities.append(city.id)
        for city_id in cities:
            city = storage.get(City, f"{city_id}")
            for place in city.places:
                places.append(place)
    
    confirmed_places = []
    for place in places:
        place_amenities = place.amenities
        confirmed_places.append(place.to_dict())
        for amenity in amenity_objects:
            if amenity not in place_amenities:
                confirmed_places.pop()
                break
    
    return json.dumps(confirmed_places)