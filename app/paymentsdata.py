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

conn = psycopg2.connect(dbname='d92a0rb0j8rphh', user='gaijmyignhvtkw', password='7e0acadc7013645d81437d922b7030782cdee4006cadf7f54501aa291b29d3e6', host='ec2-23-21-65-173.compute-1.amazonaws.com')
dbconnect = conn.cursor()

class SuccessClientPayments(Resource): 
	# This endpoints Queries all successfuly Payments for booking online Via M-pesa
	@jwt_required
	def get(self):

		current_user = get_jwt_identity()
		U = Users().get_user_role()
		if current_user != U:
			return {"message": "Access allowed only to admin"}, 403

		dbconnect.execute(" SELECT * FROM payments WHERE book_id = book_id AND status ='Paid' ORDER BY payment_id DESC ")
		conn.commit()
		book = dbconnect.fetchall()
		if not book:
			return jsonify({"message":"There is no Payments yet"})
		book_list = []
		for row in book:
			payment_id = row[0]
			bookingref = row[4]
			car_number = row[6]
			from_location = row[7]
			to_location = row[8]
			price = row[9]
			quality = row[10]
			dates = row[11]
			phone = row[12]
			amount = row[13]
			status = row[16]
			created_on = row[17].strftime("%Y-%m-%d %H:%M:%S")
			book_list.append({"payment_id":payment_id, "bookingref":bookingref, "car_number":car_number, "from_location":from_location, "to_location":to_location, "price":price, "quality":quality, "dates":dates, "amount":amount, "phone":phone, "status":status, "created_on":created_on})
		return {"book": book_list}

class FaildClientPayments(Resource):
	# This endpoint Queries all Faid payements for online bookings Via M-pesa
	@jwt_required
	def get(self):
		current_user = get_jwt_identity()
		U = Users().get_user_role()
		if current_user != U:
			return {"message": "Access allowed only to admin"}, 403

		dbconnect.execute(" SELECT * FROM payments WHERE book_id = book_id AND status = 'Faild' ORDER BY payment_id DESC ")
		conn.commit()
		book = dbconnect.fetchall()
		if not book:
			return jsonify({"message":"There is no Payments yet"})
		book_list = []
		for row in book:
			payment_id = row[0]
			bookingref = row[4]
			car_number = row[6]
			from_location = row[7]
			to_location = row[8]
			price = row[9]
			quality = row[10]
			dates = row[11]
			phone = row[12]
			amount = row[13]
			status = row[16]
			created_on = row[17].strftime("%Y-%m-%d %H:%M:%S")
			book_list.append({"payment_id":payment_id, "bookingref":bookingref, "car_number":car_number, "from_location":from_location, "to_location":to_location, "price":price, "quality":quality, "dates":dates, "amount":amount, "phone":phone, "status":status, "created_on":created_on})
		return {"book": book_list}

class DesktopSuccessPayment(Resource):
	# This endpoint Queries all Successfuly payments done by Company Via M-pesa

	@jwt_required
	def get(self):
		current_user = get_jwt_identity()
		U = Users().get_user_role()
		if current_user != U:
			return {"message": "Access allowed only to admin"}, 403

		dbconnect.execute(" SELECT * FROM payments WHERE desk_id = desk_id AND status = 'Paid' ORDER BY payment_id DESC ")
		conn.commit()
		book = dbconnect.fetchall()
		if not book:
			return jsonify({"message":"There is no Payments yet"})
		book_list = []
		for row in book:
			payment_id = row[0]
			bookingref = row[4]
			car_number = row[6]
			from_location = row[7]
			to_location = row[8]
			price = row[9]
			quality = row[10]
			dates = row[11]
			phone = row[12]
			amount = row[13]
			status = row[16]
			created_on = row[17].strftime("%Y-%m-%d %H:%M:%S")
			book_list.append({"payment_id":payment_id, "bookingref":bookingref, "car_number":car_number, "from_location":from_location, "to_location":to_location, "price":price, "quality":quality, "dates":dates, "amount":amount, "phone":phone, "status":status, "created_on":created_on})
		return {"book": book_list}


class DesktopFaildPayment(Resource):
	# This endpoint Queries all Faild payments done by Campany Via M-pesa
	@jwt_required
	def get(self):
		current_user = get_jwt_identity()
		U = Users().get_user_role()
		if current_user != U:
			return {"message": "Access allowed only to admin"}, 403

		dbconnect.execute(" SELECT * FROM payments WHERE desk_id = desk_id AND status = 'Faild' ORDER BY payment_id DESC ")
		conn.commit()
		book = dbconnect.fetchall()
		if not book:
			return jsonify({"message":"There is no Payments yet"})
		book_list = []
		for row in book:
			payment_id = row[0]
			bookingref = row[4]
			car_number = row[6]
			from_location = row[7]
			to_location = row[8]
			price = row[9]
			quality = row[10]
			dates = row[11]
			phone = row[12]
			amount = row[13]
			status = row[16]
			created_on = row[17].strftime("%Y-%m-%d %H:%M:%S")
			book_list.append({"payment_id":payment_id, "bookingref":bookingref, "car_number":car_number, "from_location":from_location, "to_location":to_location, "price":price, "quality":quality, "dates":dates, "amount":amount, "phone":phone, "status":status, "created_on":created_on})
		return {"book": book_list}

class DesktopCashpayment(Resource):
	# This Endpoint Queries all Cash payments data done by Campany
	@jwt_required
	def get(self):
		current_user = get_jwt_identity()
		U = Users().get_user_role()
		if current_user != U:
			return {"message": "Access allowed only to admin"}, 403

		dbconnect.execute("SELECT * FROM desk WHERE payments = 'Cash' ORDER BY desk_id DESC ")
		conn.commit()

		book = dbconnect.fetchall()
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

class ClientCashPayment(Resource):
	# This endpoint Queries all client paid by Cash
	@jwt_required
	def get(self):
		current_user = get_jwt_identity()
		U = Users().get_user_role()
		if current_user != U:
			return {"message": "Access allowed only to admin"}, 403

		dbconnect.execute("SELECT * FROM booking WHERE payments = 'Cash' ORDER BY book_id DESC")
		conn.commit()

		book = dbconnect.fetchall()
		if not book:
			return {"message":"There is no bookings yet"}
		book_list = []
		for row in book:
			book_id = row[0]
			bookingref = row[2]
			car_number = row[4]
			from_location = row[5]
			to_location = row[6]
			price = row[7]
			quality = row[8]
			dates = row[9]
			total = row[10]
			payments = row[11]
			created_on = row[13].strftime("%Y-%m-%d %H:%M:%S")
			book_list.append({"book_id":book_id, "bookingref":bookingref, "car_number":car_number, "from_location":from_location, "to_location":to_location, "price":price, "quality":quality, "dates":dates, "total":total, "payments":payments, "created_on":created_on})
		return jsonify({"book": book_list})	
