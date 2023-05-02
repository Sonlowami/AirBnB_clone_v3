#!/usr/bin/python3
<<<<<<< HEAD
"""states.py"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """get amenity information for all amenities"""
    amenities = []
    for amenity in storage.all("Amenity").values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """get amenity information for specified amenity"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """deletes an amenity based on its amenity_id"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """create a new amenity"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    amenity = Amenity(**request.get_json())
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """update an amenity"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, attr, val)
    amenity.save()
    return jsonify(amenity.to_dict())
=======
"""This module contain API for model class Amenity"""
from models import storage
import uuid
from models.amenity import Amenity
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.get('/amenities', strict_slashes=False)
def get_amenities():
    """Retrieve all amenities in memory"""
    amenities = storage.all(Amenity)
    if not amenities:
        abort(404)
    amenities_list = [amenity.to_dict() for amenity in amenities.values()]
    return jsonify(amenities_list)


@app_views.get('/amenities/<string:amenity_id>',
               strict_slashes=False)
def get_amenity(amenity_id):
    """Get a Amenity given it's ID"""
    amenity = storage.get(Amenity, amenity_id)
    try:
        return jsonify(amenity.to_dict())
    except AttributeError:
        abort(404)


@app_views.delete('/amenities/<string:amenity_id>', strict_slashes=False)
def delete_Amenity(amenity_id):
    """Delete amenity from the the database"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.post('/amenities', strict_slashes=False)
def add_amenity():
    """Add a Amenity to a amenity where it belongs"""
    try:
        data = request.get_json()
        amenity = Amenity()
        amenity.id = data.get('id', str(uuid.uuid4()))
        amenity.name = data['name']
        amenity.save()
        return make_response(jsonify(amenity.to_dict()), 201)

    except KeyError:
        abort(400, "Missing name")
    except Exception:
        abort(400, "Not a JSON")


@app_views.put('/amenities/<string:amenity_id>', strict_slashes=False)
def update_amenity(amenity_id):
    """Update amenity with new input"""
    amenity = storage.get(Amenity, amenity_id)
    try:
        data = request.get_json()
        if data['name'] and type(data['name']) is str:
            amenity.name = data.get('name')
            amenity.save()
        return make_response(jsonify(amenity.to_dict()), 200)

    except KeyError:
        abort(400, "Missing name")
    except AttributeError:
        abort(404)
    except Exception:
        abort(400, "Not a JSON")
>>>>>>> 8d4cbbeca324b9e151ffc2f68dcb7e76e9972330
