#!/usr/bin/python3
""" 14. Place-Amenity """

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from models.amenity import Amenity


@app_views.route('/api/v1/places/<place_id>/amenities', strict_slashes=False)
def all_amenities(place_id):
    """ retrieves all Amenity objects """
    if not storage.get(Place, place_id):
        abort(404)

    all_amenities = []
    for amenity in storage.all('Amenity').values():
        all_amenities.append(amenity.to_dict())
    return jsonify(all_amenities)


@app_views.route('/api/v1/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_by_place(place_id, amenity_id):
    """ deletes a Amenity object """
    if not storage.get(Place, place_id):
        abort(404)
    if not storage.get(Amenity, amenity_id):
        abort(404)
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place and amenity:
        place.amenities.remove(amenity)
    else:
        abort(404)
    storage.save()
    return jsonify({}), 200


@app_views.route('/api/v1/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_amenity(place_id, amenity_id):
    """ links a Amenity object to a Place """
    if not storage.get(Place, place_id):
        abort(404)
    if not storage.get(Amenity, amenity_id):
        abort(404)
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    else:
        place.amenities.append(amenity)
        storage.save()
    return jsonify(amenity.to_dict()), 201
