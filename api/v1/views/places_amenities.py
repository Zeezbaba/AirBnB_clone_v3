#!/usr/bin/python3
"""
API endpoint for the handling CRUD operations
for the places_amenities.py model
"""
import os
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity
from models.place import Place
from flasgger.utils import swag_from


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def retrive_amenities(place_id):
    """ retrieves all amenities """
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)
    amenities = [obj.to_dict() for obj in place_obj.amenities]
    return jsonify(amenities)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    """ delete amenity from place """
    place_obj = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)
    if amenity_obj not in place_obj.amenities:
        abort(404)
    place_obj.amenities.remove(amenity_obj)
    storage.save()
    return jsonify({})


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_amenity(place_id, amenity_id):
    """ Link amenities to place """
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)
    if amenity_obj in place_obj.amenities:
        return (jsonify(amenity_obj.to_dict()), 200)
    place_obj.amenities.append(obj)
    storage.save()
    return (jsonify(amenity_obj.to_dict(), 201))
