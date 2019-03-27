import datetime
import psycopg2
import smtplib

from flask import Flask,jsonify,request, make_response
from flask_restful import Resource
from functools import wraps
from flask_jwt_extended import (
  	jwt_required, create_access_token, get_current_user, 
    get_jwt_identity 
)
from models.user_model import Usermodel, Users

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
		
		curr.execute(" SELECT * FROM orders")
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
			created_on = row[11]

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
	""" Class and Method endpoint it queries all users """
	@jwt_required
	def get(self):

		# this code it identify the normal user and admin
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

		if status.strip() == '':
			return {"message": "Status cannot be empty"}, 403
 
		curr.execute("""SELECT * FROM orders WHERE parcel_id=%s """,(parcel_id,))
		state = curr.fetchone()
		# parcel_id = state[0]
		record = state[10]

		if record in types_status:
			return {"message":"You can not change this status is already in " + record}, 403

		sql = self.odrer_fetch()
		curr.execute(sql,(parcel_id,))

		parcel_data = curr.fetchone()
		creator = parcel_data[3]

		owner_data = self.check_user(creator)
		email_owner = owner_data[5]
		print (email_owner)

		curr.execute("""UPDATE orders SET status=%s WHERE parcel_id=%s """,(status, parcel_id))
		connection.commit()
		FROM = "homiemusa@gmail.com"
		TO = email_owner
		SUBJECT = "Parcel Status Changed"
		MESSAGE = "You Parcel is now {}".format(status)
		
		mail = smtplib.SMTP('smtp.gmail.com', 587)
		mail.starttls()
		mail.login("homiemusa@gmail.com", "djrefuge@12")
		msg = """From: %s\nTo: %s\nSubject: %s\n\n%s
		""" % (FROM, ", ".join(TO), SUBJECT, MESSAGE)
		mail.sendmail(FROM, TO, msg)
		mail.quit()
		return {"message":"status set to {} could not send email".format(status)}
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

		curr.execute("SELECT * FROM orders WHERE status = 'cancled'")
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
			created_on = row[11]

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

		curr.execute("SELECT * FROM orders WHERE status = 'delivered'")
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
			created_on = row[11]
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

		curr.execute("SELECT * FROM orders WHERE status = 'In Transit'")
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
			created_on = row[11]
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

		car_number = request.json['car_number']
		from_location = request.json['from_location']
		to_location = request.json['to_location']
		period = request.json['period']
		arrival = request.json['arrival']
		price  = request.json['price']
		day_time = request.json['day_time']

		if from_location.strip() == '' or to_location.strip() == '' or car_number.strip() == '' or price.strip() == '' or day_time.strip() == ''\
		or period.strip() == '' or arrival.strip() == '':
			return {"message": "Fields cannot be empty"}, 403
		# elif type(price) != int:
		# 	return {"message": "Price should be only Numbers"}, 403
		loc = Usermodel()
		data = loc.data_price()
		try:
			curr.execute(data, (car_number, from_location, to_location, period, arrival, price, day_time,))
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
			price = row[4]
			day_time = row[5]

			location.append({"price_id":price_id, "car_number":car_number, "from_location": from_location, "to_location":to_location, "price":price, "day_time":day_time})
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
		price = data['price']
		day_time = data['day_time']
		curr.execute("""UPDATE prices SET car_number =%s, from_location =%s, to_location =%s, price =%s, day_time =%s
															WHERE price_id =%s """, (car_number, from_location, to_location, price, day_time, price_id))
		connection.commit()
		return {"message": "Successfuly updated"}, 403

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

		curr.execute("SELECT * FROM booking WHERE bookingref = %s",[bookingref])
		data = curr.fetchall()
		connection.commit()

		if not data:
			return jsonify({"message":"There is no root yet"})
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
			created_on = row[12]
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
		connection.commit()
		curr.execute("SELECT * FROM booking WHERE dates = %s",[dates])
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
			created_on = row[12]
			books.append({"book_id":book_id, "bookingref":bookingref, "car_number":car_number, "from_location":from_location, "to_location":to_location, "price":price, "quality":quality, "dates":dates, "total":total, "status":status, "created_on":created_on})
		return jsonify({"data": books})	


class GetNumbers(Resource):
	""" Class Counts Numbers of users"""
	def get(self):
		curr.execute("SELECT COUNT(*) FROM users")
		data = curr.fetchall()
		return {"number": data}

class BookingNumber(Resource):
	""" Class Counts Numbers of bookings"""

	def get(self):
		curr.execute("SELECT COUNT(*) FROM booking")
		y = curr.fetchall()
		return {"nums": y}


class ParcelNumber(Resource):
	""" Class Counts Numbers of Orders"""
	def get(self):
		curr.execute("SELECT COUNT(*) FROM orders")
		x = curr.fetchall()
		return {"num": x}


class Get_All_Bookings(Resource):
	@jwt_required
	def get(self):
		""" Method for get all bookings """
		# current_user = get_jwt_identity()
		# U = Users().get_user_role()
		# if current_user != U:
		# 	return {"message": "Access allowed only to admin"}, 403

		curr.execute(" SELECT * FROM booking ")
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
		return jsonify({"data": booker})	