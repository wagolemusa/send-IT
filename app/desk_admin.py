import datetime
import psycopg2
import smtplib
import random
import base64
from flask import Flask,jsonify,request, make_response
from flask_restful import Resource
from functools import wraps
from flask_jwt_extended import (
  	jwt_required, create_access_token, get_current_user, 
    get_jwt_identity 
)
from models.user_model import Usermodel, Users
import africastalking

types_status = ["delivered", "cancled"]

connection = psycopg2.connect(dbname='d92a0rb0j8rphh', user='gaijmyignhvtkw', password='7e0acadc7013645d81437d922b7030782cdee4006cadf7f54501aa291b29d3e6', host='ec2-23-21-65-173.compute-1.amazonaws.com')
curr = connection.cursor()

class Deskbooking(Resource):
	@jwt_required

	def post(self):

		"""
		This methods helps a user to book the transport service
		"""
		current_user = get_jwt_identity()
		U = Users().get_user_role()
		if current_user != U:
			return {"message": "Access allowed only to admin"}, 403

		data = request.get_json(force=True)
		bookingref = random.randint(1, 100000)
		bookingref = str(bookingref)
		car_number = data['car_number']
		from_location = data['from_location']
		to_location = data['to_location']
		price = data['price']
		customer_name = data['customer_name']
		customer_number = data['customer_number']
		quantiy = data['quantiy']
		date_when = data['date_when']
		amount = data['amount']

		current_user = get_jwt_identity()
		username = current_user
		curr.execute(""" INSERT INTO desk(bookingref, username, car_number, from_location, to_location, price, customer_name, customer_number,\
																			 quantiy, date_when, amount)
																			VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",\
																			(bookingref, username, car_number, from_location, to_location, price, customer_name, customer_number, quantiy, date_when, amount))
		connection.commit()
		return {"message": "Succussfully Created"}


class Get_All_Desk(Resource):
	@jwt_required
	def get(self):
		
		username = get_jwt_identity()

		current_user = get_jwt_identity()
		U = Users().get_user_role()
		if current_user != U:
			return {"message": "Access allowed only to admin"}, 403
		# curr.execute(" SELECT * FROM booking WHERE username =%s", [username])
		curr.execute(" SELECT * FROM desk WHERE username =%s ORDER BY desk_id DESC LIMIT 1 ", [username])

		book = curr.fetchall()
		if not book:
			return jsonify({"message":"There is no bookings yet"})
		book_list = []
		for row in book:
			desk_id = row[0]
			bookingref = row[2]
			username = row[3]
			car_number = row[4]
			from_location = row[5]
			to_location = row[6]
			quantiy = row[7]
			price = row[8]
			amount = row[9]
			customer_name = row[10]
			customer_number = row[11]
			date_when = row[12]
			created_on = row[13].strftime("%Y-%m-%d %H:%M:%S")
			book_list.append({"desk_id":desk_id, "bookingref":bookingref, "car_number":car_number, "username":username, "from_location":from_location, "to_location":to_location, "price":price, "quantiy":quantiy, "date_when":date_when, "amount":amount, "created_on":created_on})
		return jsonify({"book": book_list})	


class DeskId(Resource):

	""" 
	Methods Queries all  bookings by ID
	
	"""
	@jwt_required
	def get(self, desk_id):

		current_user = get_jwt_identity()
		U = Users().get_user_role()
		if current_user != U:
			return {"message": "Access allowed only to admin"}, 403

		curr.execute("SELECT * FROM desk WHERE desk_id = %s",[desk_id])

		connection.commit()

		data = curr.fetchall()
		if not data:
			return {"message":"There is no bookings yet"}
		booker = []
		for row in data:
			desk_id = row[0]
			bookingref = row[2]
			username = row[3]
			car_number = row[4]
			from_location = row[5]
			to_location = row[6]
			quantiy = row[7]
			price = row[8]
			amount = row[9]
			customer_name = row[10]
			customer_number = row[11]
			date_when = row[12]
			created_on = row[13].strftime("%Y-%m-%d %H:%M:%S")
			payments = row[14]
			booker.append({"desk_id":desk_id, "bookingref":bookingref, "car_number":car_number, "username":username, "from_location":from_location, "to_location":to_location, "price":price, "quantiy":quantiy, "date_when":date_when, "amount":amount, "customer_name":customer_name, "customer_number":customer_number, "created_on":created_on, "payments":payments})
		return {"data": booker}




class CashDesk(Resource):
	# it updates the colomn in payment table to
	# indecate paided cash
	@jwt_required
	def put(self, desk_id):

		payment = "Cash"
		payments = payment
		username = get_jwt_identity()

		print(payments)
		curr.execute("""UPDATE desk SET payments =%s WHERE  payments='mpesa' AND desk_id=%s""",(payments, desk_id,))
		connection.commit()
		return {"message": "Thanks for booking with us"}


class PrintCash(Resource):
	"""
	This methods prints the recipts from desk booking clients

	"""
	@jwt_required
	def get(self):
		curr.execute("SELECT * FROM desk WHERE payments = 'Cash' ORDER BY desk_id DESC LIMIT 1")
		connection.commit()

		book = curr.fetchall()
		if not book:
			return jsonify({"message":"There is no bookings yet"})
		book_list = []
		for row in book:
			desk_id = row[0]
			bookingref = row[2]
			username = row[3]
			car_number = row[4]
			from_location = row[5]
			to_location = row[6]
			quantiy = row[7]
			price = row[8]
			amount = row[9]
			customer_name = row[10]
			customer_number = row[11]
			date_when = row[12]
			created_on = row[13].strftime("%Y-%m-%d %H:%M:%S")
			payments = row[14]
			book_list.append({"desk_id":desk_id, "bookingref":bookingref, "car_number":car_number, "username":username, "from_location":from_location, "to_location":to_location, "price":price, "quantiy":quantiy, "customer_name":customer_name, "customer_number":customer_number, "date_when":date_when, "amount":amount, "created_on":created_on, "payments":payments})
		return jsonify({"book": book_list})	