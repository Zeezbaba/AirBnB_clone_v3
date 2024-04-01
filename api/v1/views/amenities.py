#!/usr/bin/python3
'''
    API endpoint for the handling CRUD operations
    for the AMenities model
'''
from api.v1.views import app_views
from flask import request, abort, Flask, make_response
import json
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def get_amenities():
    '''
    Serves requests for amenities API
    '''
    if request.method == 'GET':
        amenities = []
        for amenity in storage.all("Amenity").values():
            amenities.append(amenity.to_dict())
        return json.dumps(amenities, indent=4)
    
    if request.method == 'POST':
        payload  = request.get_json()
        if payload is None:
            return make_response(json.dumps({'error': 'Not a JSON'}, indent=4), 400)
        if payload.get('name') is None:
            return make_response(json.dumps({'error': 'Missing name'}, indent=4), 400)
        new_amenity = Amenity(**payload)
        new_amenity.save()
        return make_response(json.dumps({new_amenity.to_dict()}, indent=4), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def amenities(amenity_id):
    '''
    amenity API
    '''
    amenity_obj = storage.get(Amenity, f"{amenity_id}")
    if amenity_obj is None:
        abort(404)
    
    if request.method == 'GET':
        return json.dumps(amenity_obj.to_dict(), indent=4)
    
    if request.method == 'DELETE':
        amenity_obj.delete()
        storage.save()
        return json.dumps({})
    
    if request.method == 'PUT':
        payload = request.get_json()
        if payload is None:
            return make_response(json.dumps({'error': 'Not a JSON'}, indent=4), 400)
        for attr, value in payload.items():
            if attr not in ['id', 'created_at', 'updated_at']:
                setattr(amenity_obj, attr, value)
        amenity_obj.save()
        return json.dumps(amenity_obj.to_dict(), indent=4)
