from flask import Flask, jsonify, request, Blueprint
import psycopg2
from flask_restful import Api
from config import app_config
from database import create_table
from home.view  import Home
from auth.view  import Register
from auth.view  import Login
from home.view import CreateParcel



def create_app(config_name):
	app = Flask(__name__, instance_relative_config=True)
	# app.config.from_object(app_config[config_name])
	app.config.from_pyfile('config.py')
	# db.int_app(app)
	v2 = Blueprint('api', __name__)
	api = Api(v2)
	app.register_blueprint(v2, url_prefix='/api')
	create_table()

	
	api.add_resource(Home, '/')
	api.add_resource(Register, '/v1/auth/signup')
	api.add_resource(Login, '/v1/auth/signin')
	api.add_resource(CreateParcel, '/v1/parcels')
	return app 


