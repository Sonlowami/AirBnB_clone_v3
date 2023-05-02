#!/usr/bin/python3
<<<<<<< HEAD
"""cities.py"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """get city information for all cities in a specified state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """get city information for specified city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """deletes a city based on its city_id"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/states/<string:state_id>/cities/', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """create a new city"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    kwargs = request.get_json()
    kwargs['state_id'] = state_id
    city = City(**kwargs)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """update a city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, attr, val)
    city.save()
    return jsonify(city.to_dict())
=======
"""This module contain API for model class City"""
from models import storage
import uuid
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.get('/states/<string:state_id>/cities',
               strict_slashes=False)
def get_cities_by_state(state_id):
    """Get a all cities in a certain state"""
    state = storage.get(State, state_id)
    try:
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)
    except AttributeError:
        abort(404)


@app_views.get('/cities/<string:city_id>',
               strict_slashes=False)
def get_city(city_id):
    """Get a city given it's ID"""
    city = storage.get(City, city_id)
    try:
        return jsonify(city.to_dict())
    except AttributeError:
        abort(404)


@app_views.delete('/cities/<string:city_id>', strict_slashes=False)
def delete_city(city_id):
    """Delete city from the the database"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.post('/states/<string:state_id>/cities',
                strict_slashes=False)
def add_city(state_id):
    """Add a city to a state where it belongs"""
    state = storage.get(State, state_id)
    try:
        data = request.get_json()
        city = City()
        city.id = data.get('id', str(uuid.uuid4()))
        city.name = data['name']
        city.state_id = state.id
        city.save()
        return make_response(jsonify(city.to_dict()), 201)
    except KeyError:
        abort(400, "Missing name")
    except AttributeError:
        abort(404)
    except Exception:
        abort(400, "Not a JSON")


@app_views.put('/cities/<string:city_id>', strict_slashes=False)
def update_city(city_id):
    """Update city with new input"""
    city = storage.get(City, city_id)
    try:
        data = request.get_json()
        if data['name'] and type(data['name']) is str:
            city.name = data.get('name')
            city.save()
            return make_response(jsonify(city.to_dict()), 201)
    except KeyError:
        abort(400, "Missing name")
    except AttributeError:
        abort(404)
    except Exception:
        abort(400, "Not a JSON")
>>>>>>> 8d4cbbeca324b9e151ffc2f68dcb7e76e9972330
