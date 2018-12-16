from flask import Flask, jsonify, request, Blueprint
from werkzeug.exceptions import HTTPException, NotFound
import psycopg2
from flask_restful import Api
from config import app_config
from flask_jwt_extended import JWTManager
from database import create_table, admin
from app.order  import Home
from app.user  import Register
from app.user  import Login
from app.order import CreateParcel
from app.order import ModifyOrder
from app.order import AnOrder
from app.admin import Admin
from app.admin import Challenge
from app.admin import GetAllUser
from app.admin import Status
from app.admin import Canceled
from app.admin import Delivered
from app.admin import InTransit
from app.admin import DeleteParcels
from app.admin import PostPrice
from app.admin import EditPrices

def create_app(config_name):
	app = Flask(__name__, instance_relative_config=True)
	# app.config.from_object(app_config[config_name])
	# app.config.from_pyfile('config.py')
	# db.int_app(app)
	v2 = Blueprint('api', __name__)
	api = Api(v2)
	app.register_blueprint(v2, url_prefix='/api')
	app.config['JWT_SECRET_KEY'] = 'refuge'
	create_table()
	admin()
	
	jwt=JWTManager(app)
	
	api.add_resource(Home, '/')
	api.add_resource(Register, '/v2/auth/signup')
	api.add_resource(Login, '/v2/auth/signin')
	api.add_resource(CreateParcel, '/v2/parcels')
	api.add_resource(ModifyOrder, '/v2/parcels/<int:parcel_id>')
	api.add_resource(AnOrder, '/v2/parcels/<int:parcel_id>/destination')
	api.add_resource(Admin, '/admin/v2/parcels')
	api.add_resource(Challenge, '/admin/v2/parcels/<int:parcel_id>/presentLocation')
	api.add_resource(Status, '/admin/v2/parcels/<int:parcel_id>/status')
	api.add_resource(GetAllUser, '/admin/v2/users')
	api.add_resource(Canceled,  '/admin/v2/canceled')
	api.add_resource(Delivered, '/admin/v2/delivered')
	api.add_resource(InTransit, '/admin/v2/intransit')
	api.add_resource(DeleteParcels, '/admin/v2/parcels/<int:parcel_id>')
	api.add_resource(PostPrice, '/admin/v2/locations')
	api.add_resource(EditPrices, '/admin/v2/locations/<int:price_id>')


	# @app.errorhandler(404)
	# def not_found(error):
	# 	return {"message": "Page Not Found"},404

	# @app.errorhandler(500)
	# def internal_error(error):
	# 	return "500 error"

	@app.errorhandler(HTTPException)
	def http_exception(e):
		return 'generic', 500

	@app.errorhandler(NotFound)
	def notfound_exception(e):
		return 'not found', 404

	return app 


