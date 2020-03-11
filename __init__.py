from flask import Flask, jsonify, request, Blueprint
from werkzeug.exceptions import HTTPException, NotFound, default_exceptions
import psycopg2
from flask_restful import Api
from flask_cors import CORS
from config import app_config
from flask_jwt_extended import JWTManager
from database import create_table, admin, drop_table
from app.order import Home
from app.user  import Register
from app.user  import Login
from app.parcel import CreateParcel
from app.parcel import CanceledParcel
from app.parcel import DeliveredParcel
from app.parcel import InTransitParcel
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
from app.order import Get_All_Bookings
from app.mpesa import Mpesa
from app.mpesa import Mpesadesk
from app.mpesa import PrintData
from app.mpesa import PaymentId
from app.mpesa import Cash
from app.mpesa import PrintMpesa
from app.mpesa import Callback
from app.admin import PaymentAdmin
from app.admin import PrintPayment
# from app.parcel import ParcelCallbackUrl
from app.desk_admin import Deskbooking
from app.admin import GetPrice_by_id
from app.admin import Sendsms
from app.admin import Emailsms
from app.order import BookingtId
from app.desk_admin import Get_All_Desk
from app.desk_admin import DeskId
from app.desk_admin import CashDesk
from app.desk_admin import PrintCash
from app.paymentsdata import SuccessClientPayments
from app.paymentsdata import FaildClientPayments
from app.paymentsdata import DesktopSuccessPayment
from app.paymentsdata import DesktopFaildPayment
from app.paymentsdata import DesktopCashpayment
from app.paymentsdata import ClientCashPayment
from app.admin import SearchPaymentsReciept
from app.cash_flow import Daily_Sum
from app.cash_flow import Weekly_Sum
from app.cash_flow import Monthly_Sum
from app.cash_flow import Daily_Sum_Receptions
from app.cash_flow import Weekly_Sum_Receptions
from app.cash_flow import Monthly_Sum_Receptions
from app.cash_flow import Daily_Book_Cash
from app.cash_flow import Weekly_Book_Cash
from app.cash_flow import Monthly_Book_Sum_Desk
from app.cash_flow import Daily_Desk_Cash
from app.cash_flow import Weekly_Desk_Cash
from app.cash_flow import Monthly_Desk_Sum_Desk
from app.admin import DeletePrice
from app.admin import Display

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
	api.add_resource(CanceledParcel,  '/parcel/v2/canceled')
	api.add_resource(DeliveredParcel, '/parcel/v2/delivered')
	api.add_resource(InTransitParcel, '/parcel/v2/intransit')
	api.add_resource(DeleteParcels, '/admin/v2/parcels/<int:parcel_id>')
	api.add_resource(PostPrice, '/admin/v2/locations')
	api.add_resource(EditPrices, '/admin/v2/locations/<int:price_id>')
	api.add_resource(GetPrice_by_id, '/admin/v2/locations/<int:price_id>')
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
	api.add_resource(Get_All_Bookings, '/admin/v2/bookings')
	api.add_resource(Mpesa, '/v2/lipa')
	api.add_resource(Mpesadesk, '/v2/desk/lipa')
	api.add_resource(PaymentId, '/v2/payments/<int:payment_id>')
	api.add_resource(Callback, '/v2/callback')
	api.add_resource(PaymentAdmin, '/admin/v2/payments/query')
	api.add_resource(PrintPayment, '/admin/v2/query/<int:payment_id>')
	# api.add_resource(ParcelCallbackUrl, '/v2/parcel/callbackurl')
	api.add_resource(Deskbooking, '/admin/v2/create/passenger')
	api.add_resource(Sendsms, '/admin/v2/sendmessage')
	api.add_resource(Emailsms, '/admin/v2/send/email/notification')
	api.add_resource(PrintData, '/v2/print/data')
	api.add_resource(Cash, '/v2/cash/payment/<int:book_id>')
	api.add_resource(BookingtId, '/v2/print/cash/<int:book_id>')
	api.add_resource(Get_All_Desk, '/v2/admin/desk/data')
	api.add_resource(DeskId, '/v2/admin/desk/<int:desk_id>')
	api.add_resource(CashDesk, '/v2/admin/desk/cash/<int:desk_id>')
	api.add_resource(PrintCash, '/v2/admin/print/cash')
	api.add_resource(SuccessClientPayments, '/v2/admin/success/client')
	api.add_resource(FaildClientPayments, '/v2/admin/faild/client')
	api.add_resource(DesktopSuccessPayment, '/v2/admin/succes/desk')
	api.add_resource(DesktopFaildPayment, '/v2/admin/faild/desk')
	api.add_resource(DesktopCashpayment,  '/v2/admin/cash/desktop')
	api.add_resource(ClientCashPayment, '/v2/admin/cash/client')
	api.add_resource(SearchPaymentsReciept, '/v2/admin/search/pay')
	api.add_resource(Daily_Sum, '/v2/admin/daily/total')
	api.add_resource(Weekly_Sum, '/v2/admin/weekly')
	api.add_resource(Monthly_Sum, '/v2/adman/monthly')
	api.add_resource(Daily_Sum_Receptions, '/v2/admin/desk/daily')
	api.add_resource(Weekly_Sum_Receptions, '/v2/admin/desk/weekly')
	api.add_resource(Monthly_Sum_Receptions, '/v2/admin/desk/monthly')
	api.add_resource(Daily_Book_Cash, '/v2/admin/book/daily')
	api.add_resource(Weekly_Book_Cash, '/v2/admin/book/weekly')
	api.add_resource(Monthly_Book_Sum_Desk, '/v2/admin/book/month')
	api.add_resource(Daily_Desk_Cash, '/v2/admin/resption/cash/daily')
	api.add_resource(Weekly_Desk_Cash, '/v2/admin/resption/cash/weekly')
	api.add_resource(Monthly_Desk_Sum_Desk, '/v2/admin/resption/cash/monthly')
	api.add_resource(DeletePrice, '/v2/admin/delete/price/<int:price_id>')
	api.add_resource(Display, '/v2/admin/display/price')
	api.add_resource(PrintMpesa, '/v2/admin/paid_with_mpasa')
	
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


