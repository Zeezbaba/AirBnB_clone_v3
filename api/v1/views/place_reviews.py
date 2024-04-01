#!/usr/bin/python3
'''
    API endpoint for the handling CRUD operations
    for the REviews model
'''
from api.v1.views import app_views
from flask import request, abort, Flask, make_response
import json
from models import storage
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'], strict_slashes=False)
def reviews_for_place(place_id):
    '''
    Handles reviews for a particular place
    '''
    place = storage.get(Place, f"{place_id}")
    if place is None:
        abort(404)
    
    if request.method == 'GET':
        reviews = []
        for review in place.reviews:
            reviews.append(review.to_dict())
        return json.dumps(reviews)
    
    if request.method == 'POST':
        payload = request.get_json()
        if payload is None:
            return make_response({'error': 'Not a JSON'}, 404)
        if payload.get('user_id') is None:
            return make_response(json.dumps({'error': 'Missing user_id'}, indent=4), 400)
        user = storage.get(User, f"{payload['user_id']}")
        if user is None:
            abort(404)
        if payload.get('text') is None:
            return make_response(json.dumps({'error': 'Missing user_id'}, indent=4), 400)
        payload['places_id'] = place_id
        review = Review(**payload)
        review.save()
        return make_response(json.dumps(review.to_dict(), indent=4), 201)


@app_views.route('/reviews/<string:review_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def reviews(review_id):
    '''
    Handles reviews
    '''
    review = storage.get(Review, f"{review_id}")
    if review is None:
        abort(404)
    if request.method == 'GET':
        return json.dumps(review.to_dict(), indent=4)
    if request.method == 'DELETE':
        review.delete()
        storage.save()
        return json.dumps({})
    
    if request.method == 'PUT':
        payload = request.get_json()
        if payload is None:
            return make_response(json.dumps({'error': 'Not a JSON'}, indent=4), 400)
        for attr, value in payload.items():
            if attr not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
                setattr(review, attr, value)
        review.save()
        return json.dumps(review.to_dict(), indent=4)
