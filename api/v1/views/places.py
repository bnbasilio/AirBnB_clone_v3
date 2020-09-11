#!/usr/bin/python3
""" 11. Place """

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State


@app_views.route('/api/v1/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_places(city_id):
    """ retrieves the list of all Place objects of a City """
    if not storage.get(City, city_id):
        abort(404)

    all_places = []
    for place in storage.all('Place').values():
        if city_id == place.to_dict()['city_id']:
            all_places.append(place.to_dict())
    return jsonify(all_places)


@app_views.route('/api/v1/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """ retrieves a Place object """
    place = storage.get(Place, place_id)

    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/api/v1/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ deletes a Place object """
    place = storage.get(Place, place_id)

    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/api/v1/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ creates a Place object """
    place_obj = request.get_json()
    if not storage.get(City, city_id):
        abort(404)
    if not place_obj:
        abort(400, {'Not a JSON'})
    if 'user_id' not in place_obj:
        abort(400, {'Missing user_id'})
    if not storage.get(User, place_obj['user_id']):
        abort(404)
    if 'name' not in place_obj:
        abort(400, {'Missing name'})
    place_obj['city_id'] = city_id
    this_place = Place(**place_obj)
    storage.new(this_place)
    storage.save()
    return jsonify(this_place.to_dict()), 201


@app_views.route('/api/v1/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """ updates a Place object """
    if not storage.get(Place, place_id):
        abort(404)
    upd_place = request.get_json()
    if not upd_place:
        abort(400, {'Not a JSON'})
    this_place = storage.get(Place, place_id)
    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in upd_place.items():
        if key not in ignore:
            setattr(this_place, key, value)
    storage.save()
    return jsonify(this_place.to_dict()), 200
