from flask import Flask, jsonify, request, Blueprint
from flask_restful import Api
import json
from .views.order import Home
from .views.users import Register
from .views.users import Login
from .views.users import Profile
from .views.order import Parcels
from .views.order import ParcelID
from .views.order import SpecificUser
from .views.order import Cancel


v1 = Blueprint('api', __name__)
api = Api(v1)


api.add_resource(Home, '/')
api.add_resource(Register, '/v1/auth/signup')
api.add_resource(Login,    '/v1/auth/signin')
api.add_resource(Profile,  '/v1/users/<int:userId>')
api.add_resource(SpecificUser, '/v1/user/<int:user_id>/parcels')
api.add_resource(Parcels,  '/v1/parcels')
api.add_resource(ParcelID,  '/v1/parcels/<int:parcelId>')
api.add_resource(Cancel, '/v1/parcels/<int:parcel_id>/cancel')




