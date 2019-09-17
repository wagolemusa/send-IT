import datetime
import psycopg2
import random   #706705005 706705005 706284799
import base64
import requests
import ssl
import json
from requests.auth import HTTPBasicAuth
from flask import Flask,jsonify,request, make_response
from flask_restful import Resource
from functools import wraps
from flask_jwt_extended import (
  	jwt_required, create_access_token, get_current_user, 
    get_jwt_identity 
)
import africastalking
from models.user_model import Usermodel

post_pond = ["postpond"]
 
connection = psycopg2.connect(dbname='d92a0rb0j8rphh', user='gaijmyignhvtkw', password='7e0acadc7013645d81437d922b7030782cdee4006cadf7f54501aa291b29d3e6', host='ec2-23-21-65-173.compute-1.amazonaws.com')
curr = connection.cursor()

class Home(Resource):
	def get(self):
		return {"message": "SendIT is one of the popular courier services"}

	@jwt_required
	def get(self):
		""" Method for get all Parcel Orders """
		username = get_jwt_identity()
		curr.execute(" SELECT * FROM orders WHERE username =%s", [username])
		data = curr.fetchall()
		if not data:
			return jsonify({"message":"There is no orders yet"})
		data_list = []
		for row in data:
			parcel_id = row[0]
			title = row[2]
			pickup = row[4]
			rec_id = row[5]
			rec_phone = row[6]
			rec_name = row[7]
			destination = row[8]
			weight = row[9]
			status = row[10]
			created_on = row[11]
			data_list.append({"parcel_id":parcel_id, "title":title, "pickup":pickup, "rec_id":rec_id, "rec_phone":rec_phone, "rec_name":rec_name, "destination":destination, "weight":weight, "status":status, "created_on":created_on})
		return jsonify({"data": data_list})	

class ModifyOrder(Resource):
	""" Class for put an order """
	@jwt_required
	def put(self, parcel_id):
		""" Method to update an order """		
		
		parcel_order = Usermodel().found_by_Id(parcel_id)

		if not parcel_order:
			return {"message":"There is no order ID {} found".format(parcel_id)}, 403	

		title = request.json['title']
		pickup = request.json['pickup']
		rec_id = request.json['rec_id']
		rec_phone = request.json['rec_phone']
		rec_name  = request.json['rec_name']
		destination = request.json['destination']
		weight = request.json['weight']

		curr.execute("""UPDATE orders SET title= %s, pickup=%s, rec_id=%s, rec_phone=%s, rec_name=%s, destination=%s, weight=%s
																														WHERE parcel_id=%s """,(title, pickup, rec_id, rec_phone, rec_name, destination, weight, parcel_id))
		connection.commit()
		return {"message": "Successfuly Updated"}

	@jwt_required
	def delete(self, parcel_id):
		username = get_jwt_identity()
		""" Method for deleting a specific order """
		parcel_order = Usermodel().found_by_Id(parcel_id)

		if not parcel_order:
			return {"message":"There is no order ID {} found".format(parcel_id)}, 403	
		curr.execute("""DELETE FROM orders WHERE parcel_id = %s AND username = %s""",(parcel_id, username))
		connection.commit()
		return {"message":"Post Deleted"}


class AnOrder(Resource):
	"""
	This class it enables the user to change the destination
	"""
	def check_user(self):
		curr.execute("SELECT phone FROM users WHERE is_admin = 'True'")
		connection.commit()
		user = curr.fetchone()
		return user

	@jwt_required
	def put(self, parcel_id):
		data = request.get_json(force=True)
		
		destination = data['destination']
		curr.execute("""UPDATE orders SET destination=%s WHERE parcel_id=%s """,(destination,	parcel_id))
		connection.commit()

		owner_data = self.check_user()
		for number in owner_data:
			phone = str(number)

			# Sends sms to mobile phone
			message = "The destination is changed by user to {}".format(destination)
			username = "refuge"    # use 'sandbox' for development in the test environment
			api_key = "73d787253bd6446b12686b20f063042cbfc7d687301f4ab8a89233b6dd523883"      # use your sandbox app API key for development in the test environment
			africastalking.initialize(username, api_key)

			# Initialize a service e.g. SMS
			sms = africastalking.SMS
			# Use the service synchronously
			response = sms.send(message, ['+254' + phone ])

		curr.execute(" SELECT * FROM orders WHERE parcel_id =%s", [parcel_id])
		data = curr.fetchall()
		data_list = []
		for row in data:
			parcel_id = row[0]
			destination = row[8]
			data_list.append({"parcel_id":parcel_id, "destination":destination})
			return {"data": data_list}
		return {"message": "Successfuly Updated"}
	


class Booking(Resource):
	@jwt_required
	def post(self):
		"""
		This methods helps a user to book the transport service
		"""
		data = request.get_json(force=True)
		bookingref = random.randint(1, 100000)
		bookingref = str(bookingref)
		car_number = data['car_number']
		from_location = data['from_location']
		to_location = data['to_location']
		price = data['price']
		quality = data['quality']
		dates  = data['dates']
		total = data['total']
		# if car_number.strip() == '' or from_location.strip() == '' or price.strip() == '' or quality.strip() == '' or data.strip() == '':
			# return{"message": "All Fields Cannot be empty!"}

		current_user = get_jwt_identity()
		username = current_user
		curr.execute(""" INSERT INTO booking(bookingref, username, car_number,from_location, to_location, price, quality, dates, total)
																				VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)""",\
																				(bookingref, username, car_number, from_location, to_location,price, quality, dates, total))
		connection.commit()
		return jsonify({"message": 'Thanks for booking make sure that you came with number'})
	

	# @jwt_required
	# def get(self):
	# 	""" 
	# 	Method for get all bookings 
	# 	"""
	# 	username = get_jwt_identity()
	# 	curr.execute(" SELECT * FROM booking WHERE username =%s", [username])
	# 	book = curr.fetchall()
	# 	if not book:
	# 		return {"message":"There is no bookings yet"}
	# 	book_list = []
	# 	for row in book:
	# 		book_id = row[0]
	# 		bookingref = row[2]
	# 		car_number = row[4]
	# 		from_location = row[5]
	# 		to_location = row[6]
	# 		price = row[7]
	# 		quality = row[8]
	# 		dates = row[9]
	# 		total = row[10]
	# 		status = row[11]
	# 		created_on = row[12]
	# 		book_list.append({"book_id":book_id, "bookingref":bookingref, "car_number":car_number, "from_location":from_location, "to_location":to_location, "price":price, "quality":quality, "dates":dates, "total":total, "status":status, "created_on":created_on})
	# 	return jsonify({"book": book_list})	


class Get_All_Bookings(Resource):
	@jwt_required
	def get(self):
		
		username = get_jwt_identity()
		# curr.execute(" SELECT * FROM booking WHERE username =%s", [username])
		curr.execute(" SELECT * FROM booking WHERE username =%s ORDER BY book_id DESC LIMIT 1 ", [username])

		book = curr.fetchall()
		if not book:
			return jsonify({"message":"There is no bookings yet"})
		book_list = []
		for row in book:
			book_id = row[0]
			bookingref = row[2]
			username = row[3]
			car_number = row[4]
			from_location = row[5]
			to_location = row[6]
			price = row[7]
			quality = row[8]
			dates = row[9]
			total = row[10]
			status = row[11]
			created_on = row[12]
			book_list.append({"book_id":book_id, "bookingref":bookingref, "car_number":car_number, "username":username, "from_location":from_location, "to_location":to_location, "price":price, "quality":quality, "dates":dates, "total":total, "status":status, "created_on":created_on})
		return jsonify({"book": book_list})	



class BookPostpond(Resource):
	""" 
	Class for postpond bookings 
	"""
	@jwt_required
	def put(self, book_id):
		data = request.get_json(force=True)
		dates = data['dates']
		status = data['status']

		curr.execute("""SELECT * FROM booking WHERE book_id=%s """,(book_id,))
		booker = curr.fetchone()
		# parcel_id = state[0]
		record = booker[11]
		if record in post_pond:
			return {"message":"You can not change this status is already in " + record}, 403


		curr.execute("""UPDATE booking SET dates=%s, status=%s WHERE book_id=%s """,(dates, status,	book_id))
		connection.commit()
		return jsonify({"message": "Successfuly Updated"})
		connection.rollback()
		return {"message": "Failed to change status try again"}


class SearchBooking(Resource):
	""" 
	Methods for searching towns

	"""
	@jwt_required
	def post(self):
		from_location = request.json['from_location']
		to_location = request.json['to_location']

		curr.execute("SELECT * FROM prices WHERE from_location = %s AND to_location =%s",[from_location,to_location])
		data = curr.fetchall()
		if not data:
			return {"message":"There is no Route yet"}
		books = []
		for row in data:
			price_id = row[0]
			car_number = row[1]
			from_location = row[2]
			to_location = row[3]
			period = row[5]
			arrival = row[5]
			price = row[6]
			day_time = row[7]

			books.append({"price_id":price_id, "car_number":car_number, "from_location": from_location, "to_location":to_location, "period":period, "arrival":arrival, "price":price, "day_time":day_time})
		return {"data": books}
		return {"message":"You can book now"}


class Users(Resource):
	""" 
	Get a user account 
	"""
	@jwt_required
	def get(self):
		""" 
		Method for get all Parcel Orders 

		"""
		username = get_jwt_identity()
		curr.execute(" SELECT * FROM users WHERE username =%s", [username,])
		data = curr.fetchall()
		if not data:
			return {"message":"There is no user yet"}
		user = []
		for row in data:
			user_id = row[0]
			first_name = row[1]
			last_name = row[2]
			username = row[3]
			phone = row[4]
			email = row[5]
			user.append({"user_id":user_id, "first_name":first_name, "last_name":last_name, "username":username, "phone":phone, "email":email})
			return jsonify({"data":user})


class UpdateUser(Resource):
	""" 
	Class updates user 
	"""
	@jwt_required
	def put(self, user_id):
		data = request.get_json(force=True)
		first_name = data['first_name']
		last_name = data['last_name']
		username = data['username']
		phone = data['phone']
		email = data['email']
		curr.execute("""UPDATE users SET first_name=%s, last_name=%s, username=%s, phone=%s, email=%s WHERE user_id=%s """,(first_name, last_name, username, phone, email, user_id))
		connection.commit()
		return jsonify({"message": "Successfuly Updated"})
		connection.rollback()
		return {"message": "Failed to update"}


class Mpesa(Resource):
	@jwt_required
	def post(self):
		""" 
			Bookings methods holds lipa na Mpesa
		"""
		data = request.get_json(force=True)
		book_id = data['book_id']
		bookingref = data['bookingref']
		car_number = data['car_number']
		from_location = data['from_location']
		to_location = data['to_location']
		price = data['price']
		quality = data['quality']
		dates  = data['dates']
		# total = data['total']
		amount = data['amount']
		phone  = data['phone']

		current_user = get_jwt_identity()
		username = current_user
		curr.execute(""" INSERT INTO payments(book_id, bookingref, username, car_number,from_location, to_location, price, quality, dates,  amount, phone)
																				VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",\
																				(book_id, bookingref, username, car_number, from_location, to_location,price, quality, dates,  amount, phone))
		connection.commit()
		
		# Lipa na mpesa Functionality 
		consumer_key = "TDWYCw9ChsdHr7QdfcXUS1ddp8gchOC6"
		consumer_secret = "BdYN5qcwGQvJnMGF"

		# api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials" #AUTH URL
		api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

		r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

		data = r.json()
		access_token = "Bearer" + ' ' + data['access_token']

		#GETTING THE PASSWORD
		timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
		passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
		business_short_code = "174379"
		data = business_short_code + passkey + timestamp
		encoded = base64.b64encode(data.encode())
		password = encoded.decode('utf-8')


		# BODY OR PAYLOAD
		payload = {
		    "BusinessShortCode": business_short_code,
		    "Password": password,
		    "Timestamp": timestamp,
		    "TransactionType": "CustomerPayBillOnline",
		    "Amount": amount,
		    "PartyA": phone,
		    "PartyB": business_short_code,
		    "PhoneNumber": phone,
		    "CallBackURL": "https://senditparcel.herokuapp.com/api/v2/callback",
		    "AccountReference": "account",
		    "TransactionDesc": "account"
		}

		#POPULAING THE HTTP HEADER
		headers = {
		    "Authorization": access_token,
		    "Content-Type": "application/json"
		}


		url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest" #C2B URL

		response = requests.post(url, json=payload, headers=headers)

		print (response.text)
		return {"message": 'Wait Response on Your phone'}


	@jwt_required
	def get(self):
		""" 
		Method for query all payments by user

		"""
		username = get_jwt_identity()
		curr.execute(" SELECT * FROM payments WHERE username =%s", [username])
		book = curr.fetchall()
		if not book:
			return jsonify({"message":"There is no Payments yet"})
		book_list = []
		for row in book:
			payment_id = row[0]
			bookingref = row[2]
			car_number = row[4]
			from_location = row[5]
			to_location = row[6]
			price = row[7]
			quality = row[8]
			dates = row[9]
			amount = row[10]
			phone = row[11]
			status = row[12]
			created_on = row[13]
			book_list.append({"payment_id":payment_id, "bookingref":bookingref, "car_number":car_number, "from_location":from_location, "to_location":to_location, "price":price, "quality":quality, "dates":dates, "amount":amount, "phone":phone, "status":status, "created_on":created_on})
		return {"book": book_list}



class PrintData(Resource):

	@jwt_required
	def get(self):
		""" 
		Method for printing reciepts data

		"""
		username = get_jwt_identity()
		curr.execute(" SELECT * FROM payments WHERE username =%s ORDER BY payment_id DESC LIMIT 1", [username])
		book = curr.fetchall()
		if not book:
			return jsonify({"message":"There is no Payments yet"})
		book_list = []
		for row in book:
			payment_id = row[0]
			bookingref = row[2]
			car_number = row[4]
			from_location = row[5]
			to_location = row[6]
			price = row[7]
			quality = row[8]
			dates = row[9]
			amount = row[10]
			phone = row[11]
			status = row[12]
			created_on = row[13]
			book_list.append({"payment_id":payment_id, "bookingref":bookingref, "car_number":car_number, "from_location":from_location, "to_location":to_location, "price":price, "quality":quality, "dates":dates, "amount":amount, "phone":phone, "status":status, "created_on":created_on})
		return {"book": book_list}


class PaymentId(Resource):

	""" 
	Methods Queries all Payments 
	
	"""
	@jwt_required
	def get(self, payment_id):
		curr.execute("SELECT * FROM payments WHERE payment_id = %s",[payment_id])
		# curr.execute("SELECT * FROM payments ORDER BY payment_id = %s, DESC LIMIT 1 WHERE username =%s", [payment_id, username])

		connection.commit()

		data = curr.fetchall()
		if not data:
			return {"message":"There is no Payments yet"}
		booker = []
		for row in data:
			payment_id = row[0]
			bookingref = row[2]
			username = row[3]
			car_number = row[4]
			from_location = row[5]
			to_location = row[6]
			price = row[7]
			quality = row[8]
			dates = row[9]
			amount = row[10]
			phone = row[11]
			status = row[12]
			created_on = row[13]
			booker.append({"payment_id":payment_id, "bookingref":bookingref, "username":username, "car_number":car_number, "from_location":from_location, "to_location":to_location, "price":price, "quality":quality, "dates":dates, "amount":amount, "phone":phone, "status":status, "created_on":created_on})
		return {"data": booker}


class Callback(Resource):
	def post(self):
		"""
		It recieves the response from safaricam
		"""
		requests = request.get_json()
		data = json.dumps(requests)

		json_da = requests.get('Body')

		# mpesa_reciept = (int["Body"]["stkCallback"]["CallbackMetadata"]["Item"][1]["Value"])

		# for item in data["Body"]["stkCallback"]["CallbackMetadata"]["Item"]:
		# 	if item["Name"] == "MpesaReceiptNumber":
		# 		mpesa_reciept = (item["Value"])

		resultcode    = json_da['stkCallback']['ResultCode']
		resultdesc    = json_da['stkCallback']['ResultDesc']

		mpesa_reciept = "MPESA"
		
		# print(mpesa_reciept)
		def pay():
			if resultcode == 0:
				return "Paid"
			elif resultcode == 1:
				return "Faild"
			else:
				return "Badrequest"


		status = pay()
		curr.execute("""UPDATE payments SET mpesa_reciept=%s, resultdesc=%s, status=%s WHERE mpesa_reciept='mpesa' resultdesc='resultdesc' AND status='no' """,(mpesa_reciept, resultdesc, status,))
		connection.commit()


class Cash(Resource):
	# it updates the colomn in payment table to
	# indecate paided cash
	@jwt_required
	def put(self, payment_id):
		mpesa_reciept = "Cash"
		username = get_jwt_identity()

		# curr.execute(" SELECT * FROM booking WHERE username =%s", [username])
		curr.execute(" SELECT * FROM payments WHERE username =%s ORDER BY payment_id DESC LIMIT 1 ", [username])
		pay = curr.fetchall()

		curr.execute("""UPDATE payments SET mpesa_reciept=%s WHERE mpesa_reciept='mpesa'"""(mpesa_reciept, payment_id))
		connection.commit()
		return {"message": "Thanks for Travel with us."}