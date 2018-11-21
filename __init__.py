from flask import Flask, jsonify, request, Blueprint
import psycopg2
from flask_restful import Api
from config import app_config
# from app import *
from home.view  import Home



def create_app(config_name):
	app = Flask(__name__, instance_relative_config=True)
	# app.config.from_object(app_config[config_name])
	app.config.from_pyfile('config.py')
	# db.int_app(app)
	v2 = Blueprint('api', __name__)
	api = Api(v2)
	app.register_blueprint(v2, url_prefix='/api')

	
	api.add_resource(Home, '/')
	return app 


