from flask import Flask, jsonify, request, Blueprint
from flask_restful import Api


from config import app_config
# from app import *
from home.order  import Home
from auth.user import Register
from auth.user import Profile
from auth.user import Login


def create_app(config_name):
	app = Flask(__name__, instance_relative_config=True)
	# app.config.from_object(app_config[config_name])
	app.config.from_pyfile('config.py')
	# db.int_app(app)
	api_bp = Blueprint('api', __name__)
	api = Api(api_bp)
	app.register_blueprint(api_bp, url_prefix='/api')


	api.add_resource(Home, '/')
	api.add_resource(Register, '/v1/auth/signup')
	api.add_resource(Profile,  '/v1/users')
	api.add_resource(Login,    '/v1/auth/signin')


	return app 


