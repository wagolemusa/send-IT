from flask import Flask, jsonify, request, Blueprint
from werkzeug.exceptions import HTTPException, NotFound, default_exceptions
import psycopg2
from flask_restful import Api
from flask_cors import CORS
from config import app_config
from flask_jwt_extended import JWTManager
from database import create_table, admin, drop_table
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
from app.admin import GetNumbers
from app.admin import SearchSerial
from app.admin import SearchDates
from app.order import Booking
from app.order import BookPostpond
from app.order import SearchBooking
from app.order import Users
from app.order import UpdateUser
from app.admin import BookingNumber
from app.admin import ParcelNumber
from app.admin import Booking_By_Id


def create_app(config_name):
	app = Flask(__name__, instance_relative_config=True)
	# app.config.from_object(app_config[config_name])
	# app.config.from_pyfile('config.py')
	# db.int_app(app)
	v2 = Blueprint('api', __name__)
	CORS(v2, resources=r'/api/*', headers='Content-Type')
	api = Api(v2)
	app.register_blueprint(v2, url_prefix='/api')

	app.config['JWT_SECRET_KEY'] = 'refuge'
	create_table()
	admin()
	# drop_table()
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
	api.add_resource(GetNumbers, '/admin/v2/number')
	api.add_resource(Booking, '/v2/book')
	api.add_resource(BookPostpond, '/v2/book/<int:book_id>/postpond')
	api.add_resource(SearchBooking, '/v2/search')
	api.add_resource(Users, '/v2/profile')
	api.add_resource(UpdateUser, '/v2/profile/<int:user_id>')
	api.add_resource(SearchSerial, '/v2/search/bookers')
	api.add_resource(SearchDates, '/v2/search/date')
	api.add_resource(BookingNumber, '/v2/booking/numbers')
	api.add_resource(ParcelNumber, '/v2/parcel/numbers')
	api.add_resource(Booking_By_Id, '/admin/v2/booking/<int:book_id>')

	# @app.errorhandler(404)
	# def not_found(error):
	# 	return {"message": "Page Not Found"},404

	# @app.errorhandler(500)
	# def internal_error(error):
	# 	return "500 error"
	# for code, ex in default_exceptions:
	# 	app.errorhandler(code)(_handle_http_exception)


	# @app.errorhandler(HTTPException)
	# def http_exception(e):
	# 	return 'Oops! Internal Error', 500

	@app.errorhandler(NotFound)
	def notfound_exception(e):
		return 'Page not found', 404

	return app 


