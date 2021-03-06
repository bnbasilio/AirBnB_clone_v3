#!/usr/bin/python3
""" 12. Reviews """

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/api/v1/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews(place_id):
    """ retrieves the list of all Review objects of a Place """
    if not storage.get(Place, place_id):
        abort(404)

    all_reviews = []
    for review in storage.all('Review').values():
        if place_id == review.to_dict()['place_id']:
            all_reviews.append(review.to_dict())
    return jsonify(all_reviews)


@app_views.route('/api/v1/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """ retrieves a Review object """
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/api/v1/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ deletes a Review object """
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/api/v1/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ creates a Review object """
    review_obj = request.get_json()
    if not storage.get(Place, place_id):
        abort(404)
    if not review_obj:
        abort(400, {'Not a JSON'})
    if 'user_id' not in review_obj:
        abort(400, {'Missing user_id'})
    if not storage.get(User, review_obj['user_id']):
        abort(404)
    if 'text' not in review_obj:
        abort(400, {'Missing text'})
    review_obj['place_id'] = place_id
    this_review = Review(**review_obj)
    storage.new(this_review)
    storage.save()
    return jsonify(this_review.to_dict()), 201


@app_views.route('/api/v1/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """ updates a Review object """
    upd_review = request.get_json()
    if not storage.get(Review, review_id):
        abort(404)
    if not upd_review:
        abort(400, {'Not a JSON'})
    this_review = storage.get(Review, review_id)
    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in upd_review.items():
        if key not in ignore:
            setattr(this_review, key, value)
    storage.save()
    return jsonify(this_review.to_dict()), 200
