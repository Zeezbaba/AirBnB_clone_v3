#!/usr/bin/python3
'''
    API endpoint for the handling CRUD operations
    for the users model
'''
from api.v1.views import app_views
from flask import request, abort, Flask, make_response
import json
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def users_no_id():
    '''
    Serves users API edpoint with no id param
    '''
    if request.method == 'GET':
        users = []
        for user in storage.all("User").values():
            users.append(user.to_dict())
        return json.dumps(users)
    
    if request.method == 'POST':
        payload = request.get_json()
        if payload is None:
            return make_response(json.dumps({'error': 'Not a JSON'}, indent=4), 400)
        if payload.get('email') is None:
            return make_response(json.dumps({'error': 'Missing email'}, indent=4), 400)
        if payload.get('password') is None:
            return make_response(json.dumps({'error': 'Missing password'}, indent=4), 400)
        
        new_user = User(**payload)
        new_user.save()
        return make_response(json.dumps(new_user.to_dict(), indent=4), 201)


@app_views.route('/users/<string:user_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def users_id(user_id):
    '''
    Serves API endpoint with id param
    '''
    user_obj = storage.get(User, f"{user_id}")
    if user_obj is None:
        abort(404)
    
    if request.method == 'GET':
        return json.dumps(user_obj.to_dict(), indent=4)
    
    if request.method == 'DELETE':
        user_obj.delete()
        storage.save()
        return json.dumps({})
    
    if request.method == 'PUT':
        payload = request.get_json()
        if payload is None:
            return make_response(json.dumps({'error': 'Not a JSON'}, indent=4), 400)
        for attr, value in payload.items():
            if attr not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user_obj, attr, value)
        user_obj.save()
        return json.dumps(user_obj.to_dict(), indent=4)
