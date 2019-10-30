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

class Admin(Resource):
	""" Class and Method endpoint it queries all parcels """
	@jwt_required
	def get(self):
		current_user = get_jwt_identity()
		U = Users().get_user_role()
		if current_user != U:
			return {"message": "Access allowed only to admin"}, 403
		
		curr.execute("SELECT * FROM orders WHERE status = 'In Transit' ORDER BY parcel_id DESC")
		connection.commit()

		data = curr.fetchall()
		if not data:
			return {"message": "No parcel orders found"}, 401
		parcel = []
		for row in data:
			parcel_id = row[0]
			title = row[2]
			username = row[3]
			pickup = row[4]
			rec_id = row[5]
			rec_phone = row[6]
			rec_name = row[7]
			destination = row[8]
			weight = row[9]
			status = row[10]
			created_on = row[11].strftime("%Y-%m-%d %H:%M:%S")

			parcel.append({"parcel_id":parcel_id, "title":title, "username":username, "pickup":pickup, "rec_id":rec_id, "rec_phone":rec_phone, "rec_name":rec_name, "destination":destination, "weight":weight, "status":status, "created_on":created_on})
		return jsonify({"data": parcel})	

class Challenge(Resource):
	""" Class and Method endpoint it changes the presentLocation """
	@jwt_required
	def put(self, parcel_id):
		# this code it identify the normal user and admin
		current_user = get_jwt_identity()
		U = Users().get_user_role()
		if current_user != U:
			return {"message": "Access allowed only to admin"}, 403
		pickup = request.json['pickup']
		
		curr.execute("""UPDATE orders SET pickup=%s WHERE parcel_id=%s """,(pickup, parcel_id))
		connection.commit()
		return jsonify({"message": "Successfuly Updated"})


class GetAllUser(Resource):
	""" 
	Class and Method endpoint it queries all users
	"""
	@jwt_required
	def get(self):
		"""
		this code it identify the normal user and admin
		"""
		current_user = get_jwt_identity()
		U = Users().get_user_role()
		if current_user != U:
			return {"message": "Access allowed only to admin"}, 403	

		user = Usermodel()
		U = user.all_users()
		curr.execute(U,)
		connection.commit()
		x = curr.fetchall()
		if not x:
			return {"message": "No users Yet"}, 401
		users = []
		for data in x:
			user_id = data[0]
			first_name = data[1]
			last_name = data[2]
			username = data[3]
			phone = data[4]
			email = data[5]

			users.append({"user_id":user_id, "first_name":first_name, "last_name":last_name, "username":username, "phone":phone , "email":email})
		return jsonify({"all_users": users})


class Status(Resource):

	def odrer_fetch(self):
		sql = "SELECT * FROM orders WHERE parcel_id=%s;"
		return sql

	def check_user(self, username):
		curr.execute("""SELECT * FROM users WHERE username=%s """,(username,))
		connection.commit()
		user = curr.fetchone()
		return user
	""" Class and Method endpoint it puts the status for a specific parcels """
	@jwt_required
	def put(self, parcel_id):
		# this code it identify the normal user and admin
		current_user = get_jwt_identity()
		U = Users().get_user_role()
		if current_user != U:
			return {"message": "Access allowed only to admin"}, 403
		data = request.get_json(force=True)
		status = data['status']
		curr.execute("""SELECT * FROM orders WHERE parcel_id=%s """,(parcel_id,))
		state = curr.fetchone()
		# parcel_id = state[0]
		record = state[10]

		if record in types_status:
			return {"message":"You can not change this status is already in " + record}, 403

		# Check the username in Orders
		sql = self.odrer_fetch()
		curr.execute(sql,(parcel_id,))
		parcel_data = curr.fetchone()
		creator = parcel_data[3]

		owner_data = self.check_user(creator)
		phone_owner = owner_data[4]
		email_owner = owner_data[5]

		#  it extract from int
		phone = str(phone_owner)
		print (phone)
		print (email_owner)
		
		# It updates in database
		curr.execute("""UPDATE orders SET status=%s WHERE parcel_id=%s """,(status, parcel_id))
		connection.commit()

		# Sends sms to mobile phone
		message = "Your Parcel is now {}".format(status)
		username = "refuge"    # use 'sandbox' for development in the test environment
		api_key = "c8eaa30fbcd30ba08b166411894c13b5b3c99fcc407991a6019ee918e52ce8f2"      # use your sandbox app API key for development in the test environment
		africastalking.initialize(username, api_key)

		# Initialize a service e.g. SMS
		sms = africastalking.SMS
		# Use the service synchronously
		response = sms.send(message, ['+254' + phone ])

		# Sent to email Address
		# FROM = "homiemusa@gmail.com"
		# TO = email_owner
		# SUBJECT = "Parcel Status Changed"
		# MESSAGE = "Your Parcel is now {}".format(status)
		
		# mail = smtplib.SMTP('smtp.gmail.com', 587)
		# mail.starttls()
		# mail.login("homiemusa@gmail.com", "djrefuge@12")
		# msg = """From: %s\nTo: %s\nSubject: %s\n\n%s
		# """ % (FROM, ", ".join(TO), SUBJECT, MESSAGE)
		# mail.sendmail(FROM, TO, msg)
		# mail.quit()
		return {"message":"status {} sent a notification on mobile number".format(status)}
		# return jsonify({"message": "Successfuly Status Changed"})	



class Canceled(Resource):
	""" Class and Method endpoint it queries parcels in Canceled """
	@jwt_required
	def get(self):

		# this code it identify the normal user and admin
		current_user = get_jwt_identity()
		U = Users().get_user_role()
		if current_user != U:
			return {"message": "Access allowed only to admin"}, 403

		curr.execute("SELECT * FROM orders WHERE status = 'cancled' ORDER BY parcel_id DESC ")
		connection.commit()

		data = curr.fetchall()
		if not data:
			return jsonify({"message":"No Cancled Order"})
		par = []
		for row in data:
			parcel_id = row[0]
			title = row[2]
			username = row[3]
			pickup = row[4]
			rec_id = row[5]
			rec_phone = row[6]
			rec_name = row[7]
			destination = row[8]
			weight = row[9]
			status = row[10]
			created_on = row[11].strftime("%Y-%m-%d %H:%M:%S")

			par.append({"parcel_id":parcel_id, "title":title, "username":username, "pickup":pickup, "rec_id":rec_id, "rec_phone":rec_phone, "rec_name":rec_name, "destination":destination, "weight":weight, "status":status, "created_on":created_on})
		return jsonify({"data": par})	

class Delivered(Resource):
	""" Class and Method endpoint it queries parcels in Delivered """
	@jwt_required
	def get(self):

		# this code it identify the normal user and admin
		current_user = get_jwt_identity()
		U = Users().get_user_role()
		if current_user != U:
			return {"message": "Access allowed only to admin"}, 403

		curr.execute("SELECT * FROM orders WHERE status = 'delivered' ORDER BY parcel_id DESC ")
		data = curr.fetchall()
		connection.commit()

		if not data:
			return jsonify({"message":"No Deliverd Order"})
		par = []
		for row in data:
			parcel_id = row[0]
			title = row[2]
			username = row[3]
			pickup = row[4]
			rec_id = row[5]
			rec_phone = row[6]
			rec_name = row[7]
			destination = row[8]
			weight = row[9]
			status = row[10]
			created_on = row[11].strftime("%Y-%m-%d %H:%M:%S")
			par.append({"parcel_id":parcel_id, "title":title, "username":username, "pickup":pickup, "rec_id":rec_id, "rec_phone":rec_phone, "rec_name":rec_name, "destination":destination, "weight":weight, "status":status, "created_on":created_on})
		return jsonify({"data": par})	

class InTransit(Resource):
	""" Class and Method endpoint it queries parcels in InTransit """
	@jwt_required
	def get(self):

		# this code it identify the normal user and admin
		current_user = get_jwt_identity()
		U = Users().get_user_role()
		if current_user != U:
			return {"message": "Access allowed only to admin"}, 403

		curr.execute("SELECT * FROM orders WHERE status = 'In Transit' ORDER BY parcel_id DESC")
		connection.commit()

		data = curr.fetchall()
		if not data:
			return jsonify({"message":"No In Transit Order"})		
		par = []
		for row in data:
			parcel_id = row[0]
			title = row[2]
			username = row[3]
			pickup = row[4]
			rec_id = row[5]
			rec_phone = row[6]
			rec_name = row[7]
			destination = row[8]
			weight = row[9]
			status = row[10]
			created_on = row[11].strftime("%Y-%m-%d %H:%M:%S")
			par.append({"parcel_id":parcel_id, "title":title, "username":username, "pickup":pickup, "rec_id":rec_id, "rec_phone":rec_phone, "rec_name":rec_name, "destination":destination, "weight":weight, "status":status, "created_on":created_on})
		return jsonify({"data": par})	


class DeleteParcels(Resource):
	""" Class and Method deletes all parcel orders """
	@jwt_required
	def delete(self, parcel_id):
		""" Method for deleting a specific order """
		current_user = get_jwt_identity()
		U = Users().get_user_role()
		if current_user != U:
			return {"message": "Access allowed only to admin"}, 403

		curr.execute("DELETE FROM orders WHERE parcel_id = %s",(parcel_id,))
		return jsonify({"message":"Post Deleted"})

class PostPrice(Resource):
	""" Class and Method post price form location """
	@jwt_required
	def post(self):
		current_user = get_jwt_identity()
		U = Users().get_user_role()
		if current_user != U:
			return {"message": "Access allowed only to admin"}, 403

		data = request.get_json(force=True)
		car_number = data['car_number']
		from_location = data['from_location']
		to_location = data['to_location']
		period = data['period']
		arrival = data['arrival']
		price  = data['price']
		day_time = data['day_time']

		if car_number.strip() == '' or from_location.strip() == '' or to_location.strip() == ''\
		or period.strip() == '' or arrival.strip() == '' or price.strip() == '' or day_time.strip() == '':
			return {"message": "Fields cannot be empty"}, 403
				
		try:

			curr.execute(""" INSERT INTO prices(car_number, from_location, to_location, period, arrival, price, day_time)
																				VALUES(%s, %s, %s, %s, %s, %s, %s)""",\
																				(car_number, from_location, to_location, period, arrival, price, day_time))
			connection.commit()
			return  {"message": "Location and Price are Successfully submited"}, 201
		except:
			connection.rollback()
			return {"message": "Failed to post location"}

	@jwt_required
	def get(self):
		current_user = get_jwt_identity()
		U = Users().get_user_role()
		if current_user != U:
			return {"message": "Access allowed only to admin"}, 403

		curr.execute("SELECT * FROM prices")
		connection.commit()

		data = curr.fetchall()

		if not data:
			return {"message": "There is no location"}, 403
		location = []

		for row in data:
			price_id = row[0]
			car_number = row[1]
			from_location = row[2]
			to_location =row[3]
			period = row[4]
			arrival = row[5]
			price = row[6]
			day_time = row[7]

			location.append({"price_id":price_id, "car_number":car_number, "from_location": from_location, "to_location":to_location,  "period": period, "arrival": arrival, "price":price, "day_time":day_time})
		return jsonify({"collection": location})

class EditPrices(Resource):
	""" Class and Method updates the locations and price """
	@jwt_required
	def put(self, price_id):

		current_user = get_jwt_identity()
		U = Users().get_user_role()
		if current_user != U:
			return {"message": "Access allowed only to admin"}, 403
			
		data = request.get_json(force=True)
		car_number = data['car_number']
		from_location = data['from_location']
		to_location = data['to_location']
		period = data['period']
		arrival = ['arrival']
		price = data['price']
		day_time = data['day_time']
		curr.execute("""UPDATE prices SET car_number =%s, from_location =%s, to_location =%s, period=%s, arrival=%s, price =%s, day_time =%s
															WHERE price_id =%s """, (car_number, from_location, to_location, period, arrival, price, day_time, price_id))
		connection.commit()
		return {"message": "Successfuly updated"}, 201


class GetPrice_by_id(Resource):
	"""
	Class method get all locations by ID
	"""
	@jwt_required
	def get(self, price_id):	
		current_user = get_jwt_identity()
		U = Users().get_user_role()
		if current_user != U:
			return {"message": "Access allowed only to admin"}, 403

		curr.execute("SELECT * FROM prices WHERE price_id = %s", [price_id])
		connection.commit()
		data = curr.fetchall()
		if not data:
			return {"message":"There is No Locations yet"}
		places = []
		for row in data:
			price_id = row[0]
			car_number = row[1]
			from_location = row[2]
			to_location =row[3]
			period = row[4]
			arrival = row[5]
			price = row[6]
			day_time = row[7]
			places.append({"price_id":price_id, "car_number":car_number, "from_location": from_location, "to_location":to_location,  "period": period, "arrival": arrival, "price":price, "day_time":day_time})
			return jsonify({"data": places})


class SearchPaymentsReciept(Resource):
	""" Methods for searching serial number """
	@jwt_required
	def post(self):
		connection.commit()
		current_user = get_jwt_identity()
		U = Users().get_user_role()
		if current_user != U:
			return {"message": "Access allowed only to admin"}, 403

		bookingref = request.json['bookingref']

		# if type(bookingref) != int:
			# return jsonify({"message": "Search Number must be only integer"})

		curr.execute("SELECT * FROM payments WHERE bookingref = %s AND booK_id = booK_id ",[bookingref])
		connection.commit()
		data = curr.fetchall()
		if not data:
			return {"message":"There is no Data"}
		book_list = []
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
			amount = row[13]
			status = row[16]
			created_on = row[17].strftime("%Y-%m-%d %H:%M:%S")
			book_list.append({"payment_id":payment_id, "bookingref":bookingref, "username":username, "car_number":car_number, "from_location":from_location, "to_location":to_location, "price":price, "quality":quality, "dates":dates, "amount":amount, "status":status, "created_on":created_on})
		return jsonify({"data": book_list})	

class SearchSerial(Resource):
	""" Methods for searching serial number """
	@jwt_required
	def post(self):
		connection.commit()
		current_user = get_jwt_identity()
		U = Users().get_user_role()
		if current_user != U:
			return {"message": "Access allowed only to admin"}, 403

		bookingref = request.json['bookingref']

		# if type(bookingref) != int:
			# return jsonify({"message": "Search Number must be only integer"})

		curr.execute("SELECT * FROM booking WHERE bookingref = %s AND payments = 'Cash' ",[bookingref])
		connection.commit()
		data = curr.fetchall()
		if not data:
			return {"message":"There is no root yet"}
		books = []
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
			status = row[11]
			created_on = row[12]
			books.append({"book_id":book_id, "bookingref":bookingref, "username":username, "car_number":car_number, "from_location":from_location, "to_location":to_location, "price":price, "quality":quality, "dates":dates, "total":total, "status":status, "created_on":created_on})
		return jsonify({"data": books})	

class Booking_By_Id(Resource):
	""" 
	Class Method get a specific book by ID 
	"""
	@jwt_required
	def get(self, book_id):
		current_user = get_jwt_identity()
		U = Users().get_user_role()
		if current_user != U:
			return {"message": "Access allowed only to admin"}, 403
			
		curr.execute("SELECT * FROM booking WHERE book_id = %s",[book_id])
		connection.commit()

		data = curr.fetchall()
		if not data:
			return jsonify({"message":"There is no root yet"})
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
			status = row[11]
			created_on = row[13].strftime("%Y-%m-%d %H:%M:%S")
			booker.append({"book_id":book_id, "bookingref":bookingref, "username":username, "car_number":car_number, "from_location":from_location, "to_location":to_location, "price":price, "quality":quality, "dates":dates, "total":total, "status":status, "created_on":created_on})
		return jsonify({"data": booker})	


class SearchDates(Resource):
	""" Methods for searching dates """
	@jwt_required
	def post(self):
		current_user = get_jwt_identity()
		U = Users().get_user_role()
		if current_user != U:
			return {"message": "Access allowed only to admin"}, 403
		dates = request.json['dates']
		curr.execute("SELECT * FROM booking WHERE dates = %s",[dates])
		connection.commit()

		data = curr.fetchall()
		if not data:
			return jsonify({"message":"There is no root yet"})
		books = []
		for row in data:
			book_id = row[0]
			bookingref = row[2]
			car_number = row[4]
			from_location = row[5]
			to_location = row[6]
			price = row[7]
			quality = row[8]
			dates = row[9]
			total = row[10]
			status = row[11]
			created_on = row[12].strftime("%Y-%m-%d %H:%M:%S")
			books.append({"book_id":book_id, "bookingref":bookingref, "car_number":car_number, "from_location":from_location, "to_location":to_location, "price":price, "quality":quality, "dates":dates, "total":total, "status":status, "created_on":created_on})
		return jsonify({"data": books})	


class GetNumbers(Resource):
	""" Class Counts Numbers of users"""
	def get(self):
		curr.execute("SELECT COUNT(*) FROM users")
		connection.commit()

		data = curr.fetchall()
		return {"number": data}

class BookingNumber(Resource):
	""" Class Counts Numbers of bookings"""

	def get(self):
		curr.execute("SELECT COUNT(*) FROM booking")
		connection.commit()

		y = curr.fetchall()
		return {"nums": y}


class ParcelNumber(Resource):
	""" Class Counts Numbers of Orders"""
	def get(self):
		curr.execute("SELECT COUNT(*) FROM orders")
		connection.commit()

		x = curr.fetchall()
		return {"num": x}


class PaymentAdmin(Resource):
	""" Method Query all payments """
	@jwt_required
	def get(self):
		""" Method for query all payments"""
		current_user = get_jwt_identity()
		U = Users().get_user_role()
		if current_user != U:
			return {"message": "Access allowed only to admin"}, 403
		curr.execute(" SELECT * FROM payments ")
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
		return jsonify({"book": book_list})			


class PrintPayment(Resource):
	@jwt_required
	def get(self, payment_id):
		current_user = get_jwt_identity()
		U = Users().get_user_role()
		if current_user != U:
			return {"message": "Access allowed only to admin"}, 403

		curr.execute("SELECT * FROM payments WHERE payment_id = %s",[payment_id])
		connection.commit()

		data = curr.fetchall()
		if not data:
			return jsonify({"message":"There is no Payments yet"})
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
			booker.append({"payment_id":payment_id, "bookingref":bookingref, "username":username, "car_number":car_number, "from_location":from_location, "to_location":to_location, "price":price, "quality":quality, "dates":dates, "amount":amount, "phone":phone, "mpesa_reciept":mpesa_reciept, "resultdesc":resultdesc, "status":status, "created_on":created_on})
		return jsonify({"data": booker})	

# class Desk(Resource):
# 	@jwt_required
# 	def post(self):
# 		current_user = get_jwt_identity()
# 		U = Users().get_user_role()
# 		if current_user != U:
# 			return {"message": "Access allowed only to admin"}, 403

# 		data = request.get_json(force=True)
# 		bookingref = random.randint(1, 100000)
# 		bookingref = str(bookingref)
# 		customer_name = data['customer_name']
# 		customer_number = data['customer_number']
# 		from_location = data['from_location']
# 		to_location  = data['to_location']
# 		quantiy = data['quantiy']
# 		price = data['price']
# 		date_when = data['date_when']
# 		time_at  = data['time_at']
# 		username = current_user

# 		curr.execute(""" INSERT INTO desk(bookingref, username, customer_name, customer_number,\
# 																			from_location, to_location, quantiy, price, date_when, time_at)
# 																			VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",\
# 																			(bookingref, username, customer_name, customer_number, from_location, to_location, quantiy, price, date_when, time_at))
# 		connection.commit()
# 		return {"message": "Succussfully Created"}


class Sendsms(Resource):
	"""
	Class methods sends messages to all numbers which is registerd

	"""
	def post(self):
		data = request.get_json(force=True)
		message = data['message']
		if message.strip() == '':
			return {"message": "You must type in message"}
		curr.execute("SELECT phone FROM users")
		connection.commit()

		data = curr.fetchall()
		print (data)
		num = data
		list1 = []
		for nums in num:
			list1.append(nums[0])
		print (list1)

		call = list1

		for m in call:
			sendsms = str(m)
			print ('+254' + sendsms)
			username = "refuge"    # use 'sandbox' for development in the test environment
			api_key = "c8eaa30fbcd30ba08b166411894c13b5b3c99fcc407991a6019ee918e52ce8f2"      # use your sandbox app API key for development in the test environment
			africastalking.initialize(username, api_key)

			# Initialize a service e.g. SMS
			sms = africastalking.SMS
			# Use the service synchronously
			response = sms.send(message, ['+254' + sendsms ])
		print(response)

class Emailsms(Resource):
	def post(self):
		"""
		This Method it emails message to all users who have registered
		""" 
		data = request.get_json(force=True)
		message = data['message']
		curr.execute("SELECT email FROM users")
		connection.commit()
		data = curr.fetchall()
		print (data)
		sms = data
		email = []
		for send in sms:
			email.append(send[0])

		for notication in email:
			emailx = notication
		
			FROM = "homiemusa@gmail.com"
			TO = emailx
			SUBJECT = "Noticatications"
			MESSAGE = message
		
			mail = smtplib.SMTP(host='https://senditparcel.herokuapp.com/', port=5432)
			mail.starttls()
			mail.login("homiemusa@gmail.com", "djrefuge@12")
			msg = """From: %s\nTo: %s\nSubject: %s\n\n%s
			""" % (FROM, ", ".join(TO), SUBJECT, MESSAGE)
			mail.sendmail(FROM, TO, msg)
			mail.quit()
		return {"message":"Successful sent"}

