from flask import Flask, jsonify, request, Blueprint
from flask_restful import Api
import json
# from run import app 
from models import *

from config import app_config
# from app import *
from home.order  import Home
from auth.user import Register
from auth.user import Profile
from auth.user import Login
from home.order import Parcels
from home.order import ParcelID


api_bp = Blueprint('api', __name__)
api = Api(api_bp)


api.add_resource(Home, '/')
api.add_resource(Register, '/v1/auth/signup')
api.add_resource(Profile,  '/v1/users')
api.add_resource(Login,    '/v1/auth/signin')
api.add_resource(Parcels,  '/v1/parcels')
api.add_resource(ParcelID,  '/v1/parcels/<int:parcel_id>')



