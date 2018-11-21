from flask import Flask, jsonify, request, Blueprint
from flask_restful import Api

from config import app_config
# method that creates out app

from app.order import Home
from app.users import Register
from app.users import Login
from app.users import Profile
from app.users import UserID
from app.order import Parcels
from app.order import ParcelID
from app.order import SpecificUser
from app.order import Cancel

def create_app(config_name):
	app = Flask(__name__, instance_relative_config=True)
	# app.config.from_pyfile('config.py')

	v1 = Blueprint('api', __name__)
	api = Api(v1)
	app.register_blueprint(v1, url_prefix='/api')
	
	api.add_resource(Home, '/')
	api.add_resource(Register, '/v1/auth/signup')
	api.add_resource(Login,    '/v1/auth/signin')
	api.add_resource(Profile,  '/v1/users')
	api.add_resource(UserID,   '/v1/users/<int:userId>')
	api.add_resource(SpecificUser, '/v1/user/<int:user_id>/parcels')
	api.add_resource(Parcels,  '/v1/parcels')
	api.add_resource(ParcelID,  '/v1/parcels/<int:parcelId>')
	api.add_resource(Cancel, '/v1/parcels/<int:parcel_id>/cancel')
	return app