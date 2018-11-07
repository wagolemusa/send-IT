from flask import Flask, jsonify, request, Blueprint
from flask_restful import Api
import json
from models import *
from decorator import *
from app.order  import Home
from auth.users import Register
from auth.users import Login
from auth.users import Profile
from app.order import Parcels
from app.order import ParcelID


v1 = Blueprint('api', __name__)
api = Api(v1)


api.add_resource(Home, '/')
api.add_resource(Register, '/v1/auth/signup')
api.add_resource(Login,    '/v1/auth/signin')
api.add_resource(Profile,  '/v1/users')
api.add_resource(Parcels,  '/v1/parcels')
api.add_resource(ParcelID,  '/v1/parcels/<int:parcel_id>')




