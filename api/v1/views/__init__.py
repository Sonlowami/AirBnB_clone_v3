#!/usr/bin/python3
<<<<<<< HEAD
"""Initialize Blueprint views"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.amenities import *
from api.v1.views.cities import *
from api.v1.views.places import *
from api.v1.views.places_amenities import *
from api.v1.views.places_reviews import *
from api.v1.views.states import *
from api.v1.views.users import *
=======
"""This is a blueprint for my APIs"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.cities import *
from api.v1.views.states import *
from api.v1.views.places import *
from api.v1.views.users import *
from api.v1.views.amenities import *
from api.v1.views.reviews import *
>>>>>>> 8d4cbbeca324b9e151ffc2f68dcb7e76e9972330
