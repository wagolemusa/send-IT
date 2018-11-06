from flask import Flask, jsonify, request, Blueprint
from flask_restful import Api
import json
from models import *

from app.order  import Home
from auth.users import Register
from auth.users import Login
from auth.users import Profile
from app.order import Parcels





v1 = Blueprint('api', __name__)
api = Api(v1)


api.add_resource(Home, '/')
api.add_resource(Register, '/v1/auth/signup')
api.add_resource(Login,    '/v1/auth/signin')
api.add_resource(Profile,  '/v1/users')
api.add_resource(Parcels,  '/v1/parcels')



