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



class CreateParcel(Resource):
	""" Class for create parcel methods """
	@jwt_required
	def post(self):
		data = request.get_json(force=True)
		title = data['title']
		pickup = data['pickup']
		rec_id = data['rec_id']
		rec_phone = data['rec_phone']
		rec_name  = data['rec_name']
		destination = data['destination']
		weight = data['weight']
	
		if title.strip() == '' or pickup.strip() =='' or destination.strip() =='':
			return jsonify({"message":"Feilds  cannot be blank"})
		# elif type(rec_id) != int or type(rec_phone) != int or type(weight) != int:
			# return jsonify({"meassge":"ID, Phone and weight master be numbers"})

		current_user = get_jwt_identity()
		username = current_user
		# try:
		curr.execute(""" INSERT INTO orders(title, username, pickup,rec_id, rec_phone, rec_name, destination, weight)
																	VALUES(%s, %s, %s, %s, %s, %s, %s, %s)""",\
																		(title, username, pickup, rec_id, rec_phone,rec_name, destination, weight))
		connection.commit()
		return jsonify({"message": 'Successfuly Created an Order'})

		# # except:
		# # 	connection.rollback()
		# # 	return {"message": "Failed to post location"}
		
		# # Lipa na mpesa Functionality 
		# consumer_key = "TDWYCw9ChsdHr7QdfcXUS1ddp8gchOC6"
		# consumer_secret = "BdYN5qcwGQvJnMGF"

		# api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

		# r = requests.get('api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret)', verify=False)

		# data = r.json()
		# access_token = "Bearer" + ' ' + data['access_token']

		# #GETTING THE PASSWORD
		# timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
		# passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
		# business_short_code = "174379"
		# data = business_short_code + passkey + timestamp
		# encoded = base64.b64encode(data.encode())
		# password = encoded.decode('utf-8')


		# # BODY OR PAYLOAD
		# payload = {
		#     "BusinessShortCode": business_short_code,
		#     "Password": password,
		#     "Timestamp": timestamp,
		#     "TransactionType": "CustomerPayBillOnline",
		#     "Amount": cash,
		#     "PartyA": phone,
		#     "PartyB": business_short_code,
		#     "PhoneNumber": phone,
		#     "CallBackURL": "https://senditparcel.herokuapp.com/api/v2/parcel/callbackurl",
		#     "AccountReference": "account",
		#     "TransactionDesc": "account"
		# }

		# #POPULAING THE HTTP HEADER
		# headers = {
		#     "Authorization": access_token,
		#     "Content-Type": "application/json"
		# }

		# url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest" #C2B URL

		# response = requests.post(url, json=payload, headers=headers)
		# print (response.text)
		# return jsonify({"message": 'Thanks for paying'})


	@jwt_required
	def get(self):
		""" Method for get all Parcel Orders """
		username = get_jwt_identity()
		curr.execute(" SELECT * FROM orders WHERE username =%s", [username])
		connection.commit()
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
			created_on = row[11].strftime("%Y-%m-%d %H:%M:%S")
			data_list.append({"parcel_id":parcel_id, "title":title, "pickup":pickup, "rec_id":rec_id, "rec_phone":rec_phone, "rec_name":rec_name, "destination":destination, "weight":weight, "status":status, "created_on":created_on})
		return jsonify({"data": data_list})	




# class ParcelCallbackUrl(Resource):
# 	""" Class And Methods creates Callback url for sending parcel"""
# 	def post(self):
# 		requests = request.get_json()
# 		data = json.dumps(requests)
# 		json_da = requests.get('Body')
# 		resultcode = json_da['stkCallback']['ResultCode']

# 		def pay():
# 			if resultcode == 0:
# 				return "Paid"
# 			elif resultcode == 1:
# 				return "Faild"
# 			else:
# 				return "Badrequest"

# 		payments = pay()
# 		print(payments)

# 		curr.execute("""UPDATE orders SET payments=%s WHERE payments = 'NotPaid' """,(payments,))
# 		connection.commit()
