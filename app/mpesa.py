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
 
connmpesa = psycopg2.connect(dbname='d92a0rb0j8rphh', user='gaijmyignhvtkw', password='7e0acadc7013645d81437d922b7030782cdee4006cadf7f54501aa291b29d3e6', host='ec2-23-21-65-173.compute-1.amazonaws.com')
dbmpesa = connmpesa.cursor()


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
		dbmpesa.execute(""" INSERT INTO payments(book_id,bookingref, username, car_number,from_location, to_location, price, quality, dates,  amount, phone)
																				VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",\
																				(book_id, bookingref, username, car_number, from_location, to_location,price, quality, dates,  amount, phone))
		connmpesa.commit()
		
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


class Mpesadesk(Resource):
	@jwt_required
	def post(self):
		""" 
			Bookings methods holds lipa na Mpesa
		"""
		data = request.get_json(force=True)
		desk_id = data['desk_id']
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
		dbmpesa.execute(""" INSERT INTO payments(desk_id, bookingref, username, car_number,from_location, to_location, price, quality, dates,  amount, phone)
																				VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",\
																				(desk_id, bookingref, username, car_number, from_location, to_location,price, quality, dates,  amount, phone))
		connmpesa.commit()
		
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


class Callback(Resource):
	def post(self):
		"""
		It recieves the response from safaricam
		"""
		requests = request.get_json()
		data = json.dumps(requests)

		json_da = requests.get('Body')

		print (json_da)

		# mpesa_reciept = (int["Body"]["stkCallback"]["CallbackMetadata"]["Item"][1]["Value"])

		# for item in data["Body"]["stkCallback"]["CallbackMetadata"]["Item"]:
		# 	if item["Name"] == "MpesaReceiptNumber":
		# 		mpesa_reciept = (item["Value"])

		resultcode    = json_da['stkCallback']['ResultCode']
		resultdesc    = json_da['stkCallback']['ResultDesc']
		# phone = json_da["stkCallback"]["CallbackMetadata"]["Item"][4]["Value"]

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
		dbmpesa.execute("""UPDATE payments SET mpesa_reciept=%s, resultdesc=%s, status=%s WHERE mpesa_reciept='mpesa' AND resultdesc='resultdesc' AND status='no' """,(mpesa_reciept, resultdesc, status,))
		connmpesa.commit()

		dbmpesa.execute("SELECT * FROM payments ORDER BY payment_id DESC LIMIT 1")
		connmpesa.commit()
		owner = dbmpesa.fetchall()
		for row in owner:

			phone = str(row[12])
			resultdesc = row[15]
			from_location = row[7]
			to_location = row[8]
			status = row[16]

			desc = resultdesc[12:]

			# Sends sms to mobile phone
			message = "%s From:.. %s To:.. %s, Payment Status:.. %s" %(desc, from_location, to_location, status)
			username = "refuge"    # use 'sandbox' for development in the test environment
			api_key = "c8eaa30fbcd30ba08b166411894c13b5b3c99fcc407991a6019ee918e52ce8f2"      # use your sandbox app API key for development in the test environment
			africastalking.initialize(username, api_key)

			# Initialize a service e.g. SMS
			sms = africastalking.SMS
			# Use the service synchronously
			response = sms.send(message, ['+' + phone ])


class PrintMpesa(Resource):
	# @jwt_required
	def get(self):
		""" 
		Method for query all payments by user
		"""
		username = get_jwt_identity()
		dbmpesa.execute(" SELECT * FROM payments WHERE username =%s ORDER BY payment_id DESC ", [username])
		bookpesa = dbmpesa.fetchall()
		if not bookpesa:
			return jsonify({"message":"There is no Payments yet"})
		listpesa = []
		for row in bookpesa:
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
			listpesa.append({"payment_id":payment_id, "bookingref":bookingref, "car_number":car_number, "from_location":from_location, "to_location":to_location, "price":price, "quality":quality, "dates":dates, "amount":amount, "phone":phone, "status":status, "created_on":created_on})
		return {"bookpesa": listpesa}



class PrintData(Resource):

	@jwt_required
	def get(self):
		""" 
		Method for printing reciepts data

		"""
		username = get_jwt_identity()
		dbmpesa.execute(" SELECT * FROM payments WHERE username =%s ORDER BY payment_id DESC LIMIT 1", [username])
		book = dbmpesa.fetchall()
		if not book:
			return jsonify({"message":"There is no Payments yet"})
		book_list = []
		for row in book:
			payment_id = row[0]
			bookingref = row[4]
			username = row[5]
			car_number = row[6]
			from_location = row[7]
			to_location = row[8]
			price = row[9]
			quality = row[10]
			dates = row[11]
			phone = row[12]
			amount = row[13]
			mpesa_reciept = row[14]
			resultdesc = row[15]
			status = row[16]
			created_on = row[17].strftime("%Y-%m-%d %H:%M:%S")
			book_list.append({"payment_id":payment_id, "bookingref":bookingref, "car_number":car_number, "from_location":from_location, "to_location":to_location, "price":price, "quality":quality, "dates":dates, "phone":phone, "amount":amount, "mpesa_reciept":mpesa_reciept, "resultdesc":resultdesc, "status":status, "created_on":created_on})
		return {"book": book_list}


class PaymentId(Resource):

	""" 
	Methods Queries all Payments 
	
	"""
	@jwt_required
	def get(self, payment_id):
		dbmpesa.execute("SELECT * FROM payments WHERE payment_id = %s",[payment_id])
		# curr.execute("SELECT * FROM payments ORDER BY payment_id = %s, DESC LIMIT 1 WHERE username =%s", [payment_id, username])

		connmpesa.commit()

		data = dbmpesa.fetchall()
		if not data:
			return {"message":"There is no Payments yet"}
		booker = []
		for row in data:
			payment_id = row[0]
			bookingref = row[4]
			username = row[5]
			car_number = row[6]
			from_location = row[7]
			to_location = row[8]
			price = row[9]
			quality = row[10]
			dates = row[11]
			phone = row[12]
			amount = row[13]
			mpesa_reciept = row[14]
			resultdesc = row[15]
			status = row[16]
			created_on = row[17].strftime("%Y-%m-%d %H:%M:%S")
			booker.append({"payment_id":payment_id, "bookingref":bookingref, "username":username, "car_number":car_number, "from_location":from_location, "to_location":to_location, "price":price, "quality":quality, "dates":dates, "phone":phone, "amount":amount,  "mpesa_reciept":mpesa_reciept, "resultdesc":resultdesc, "status":status, "created_on":created_on})
		return {"data": booker}

class Cash(Resource):
	# it updates the colomn in payment table to
	# indecate paid with cash
	@jwt_required
	def put(self, book_id):

		payment = "Cash"
		payments = payment

		print(payments)
		dbmpesa.execute("""UPDATE booking SET payments =%s WHERE  payments='mpesa' AND book_id=%s""",(payments, book_id,))
		connmpesa.commit()

		current_user = get_jwt_identity()
		name_user = current_user
		print(name_user)
	
		dbmpesa.execute("SELECT phone FROM users WHERE username = %s ", [name_user])
		connmpesa.commit()
		numbers = dbmpesa.fetchone()
		for number in numbers:
			num = str(number)
		phone = num
		print(phone)

		dbmpesa.execute("SELECT * FROM booking ORDER BY book_id DESC LIMIT 1")
		connmpesa.commit()
		owner = dbmpesa.fetchall()
		for row in owner:
			bookingref = row[2]
			from_location = row[5]
			to_location = row[6]
			dates = row[9]

			# Sends sms to mobile phone
			message = "Receipt number:..%s From:..%s To:.. %s On:...%s" %(bookingref, from_location, to_location, dates)
			username = "refuge"    # use 'sandbox' for development in the test environment
			api_key = "c8eaa30fbcd30ba08b166411894c13b5b3c99fcc407991a6019ee918e52ce8f2"      # use your sandbox app API key for development in the test environment
			africastalking.initialize(username, api_key)

			# Initialize a service e.g. SMS
			sms = africastalking.SMS
			# Use the service synchronously
			response = sms.send(message, ['+254' + phone ])
		return {"message": "Thanks for booking with us, Wait Message on your Phone"}
		