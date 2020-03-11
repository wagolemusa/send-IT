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
 
connOrder = psycopg2.connect(dbname='d92a0rb0j8rphh', user='gaijmyignhvtkw', password='7e0acadc7013645d81437d922b7030782cdee4006cadf7f54501aa291b29d3e6', host='ec2-23-21-65-173.compute-1.amazonaws.com')
currBook = connOrder.cursor()

class Home(Resource):
	def get(self):
		return {"message": "SendIT is one of the popular courier services"}


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

		currBook.execute("""UPDATE orders SET title= %s, pickup=%s, rec_id=%s, rec_phone=%s, rec_name=%s, destination=%s, weight=%s
																														WHERE parcel_id=%s """,(title, pickup, rec_id, rec_phone, rec_name, destination, weight, parcel_id))
		connOrder.commit()
		return {"message": "Successfuly Updated"}

	@jwt_required
	def delete(self, parcel_id):
		username = get_jwt_identity()
		""" Method for deleting a specific order """
		parcel_order = Usermodel().found_by_Id(parcel_id)

		if not parcel_order:
			return {"message":"There is no order ID {} found".format(parcel_id)}, 403	
		currBook.execute("""DELETE FROM orders WHERE parcel_id = %s AND username = %s""",(parcel_id, username))
		connOrder.commit()
		return {"message":"Post Deleted"}


class AnOrder(Resource):
	"""
	This class it enables the user to change the destination
	"""
	def check_user(self):
		currBook.execute("SELECT phone FROM users WHERE is_admin = 'True'")
		connOrder.commit()
		user = currBook.fetchone()
		return user

	@jwt_required
	def put(self, parcel_id):
		data = request.get_json(force=True)
		
		destination = data['destination']
		currBook.execute("""UPDATE orders SET destination=%s WHERE parcel_id=%s """,(destination,	parcel_id))
		connOrder.commit()

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
		currBook.execute(" SELECT * FROM orders WHERE parcel_id =%s", [parcel_id])
		data = currBook.fetchall()
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
		connOrder.commit()
		return jsonify({"message": 'Thanks for booking make sure that you came with number'})
	

	@jwt_required
	def get(self):
		connOrder.commit()
		""" 
		Method for get all bookings 
		"""
		username = get_jwt_identity()
		currBook.execute("SELECT * FROM booking WHERE payments = 'Cash' ORDER BY book_id DESC")
		connOrder.commit()
		book = currBook.fetchall()
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


class Get_All_Bookings(Resource):
	@jwt_required
	def get(self):
		
		username = get_jwt_identity()
		# curr.execute(" SELECT * FROM booking WHERE username =%s", [username])
		currBook.execute(" SELECT * FROM booking WHERE username =%s ORDER BY book_id DESC LIMIT 1 ", [username])
		connOrder.commit()
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


class BookingtId(Resource):
	""" 
	Methods Queries all  bookings by ID
	"""
	@jwt_required
	def get(self, book_id):
		currBook.execute("SELECT * FROM booking WHERE book_id = %s",[book_id])
		connOrder.commit()
		data = curr.fetchall()
		if not data:
			return {"message":"There is no bookings yet"}
		booker = []
		for row in data:
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
			payments = row[11]
			created_on = row[13].strftime("%Y-%m-%d %H:%M:%S")
			booker.append({"book_id":book_id, "bookingref":bookingref, "username":username, "car_number":car_number, "from_location":from_location, "to_location":to_location, "price":price, "quality":quality, "dates":dates,  "total":total, "payments":payments, "created_on":created_on})
		return {"data": booker}



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
		currBook.execute("""UPDATE booking SET dates=%s, status=%s WHERE book_id=%s """,(dates, status,	book_id))
		connOrder.commit()
		return jsonify({"message": "Successfuly Updated"})
		connOrder.rollback()
		return {"message": "Failed to change status try again"}


class SearchBooking(Resource):
	""" 
	Methods for searching towns
	"""
	# @jwt_required
	def post(self):
		from_location = request.json['from_location']
		to_location = request.json['to_location']
		dates = request.json['dates']

		currBook.execute("SELECT * FROM prices WHERE from_location = %s, to_location =%s AND dates =%s",[from_location,to_location,dates])
		data = currBook.fetchall()
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
		currBook.execute(" SELECT * FROM users WHERE username =%s", [username,])
		data = currBook.fetchall()
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
		currBook.execute("""UPDATE users SET first_name=%s, last_name=%s, username=%s, phone=%s, email=%s WHERE user_id=%s """,(first_name, last_name, username, phone, email, user_id))
		connOrder.commit()
		return jsonify({"message": "Successfuly Updated"})
		connOrder.rollback()
		return {"message": "Failed to update"}



	