import datetime
import psycopg2
from flask import Flask,jsonify,request, make_response
from flask_restful import Resource
from functools import wraps
from flask_jwt_extended import (
  	jwt_required, create_access_token, get_current_user, 
    get_jwt_identity 
)
from models.user_model import Usermodel, Users

connection = psycopg2.connect(dbname='sendit', user='postgres', password='refuge', host='localhost')
curr = connection.cursor()

# class Users():
	# def get_user_role(self):
	# 	"""Fetch user role"""
	# 	current_user = get_jwt_identity()
	# 	sql = "SELECT is_admin FROM users WHERE username = %s"
	# 	curr.execute(sql,)
	# 	is_admin = curr.fetchone()
	# 	return is_admin
# def fetch_by_username(self, username):
# 	""" fetch user by username """
# 	curr.execute("""SELECT * FROM users WHERE username=%s""", (username,))
# 	user = curr.fetchone()

# def admin_only(f):
# 	''' Restrict access if not admin '''
# 	@wraps(f)
# 	def wrapper_function(*args, **kwargs):
# 		# user = get_jwt_identity()
#  		user = Users().fetch_by_username(get_jwt_identity()["username"])
#  		if not user.is_admin:
#  			return {'message': 'Anauthorized access, you must be an admin to access this level'}, 401
#  		return f(*args, **kwargs)
# 	return wrapper_function


class Admin(Resource):
	# @jwt_required
	# @admin_only
	def get(self):
		""" Method for get all Parcel Orders """
		# role = Users().fetch_by_username()

		# if role != "True":
		# 	return {"message": "Access allowed only to admin"}, 403

		curr.execute(" SELECT * FROM orders")
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
			parcel.append({"parcel_id":parcel_id, "title":title, "username":username, "pickup":pickup, "rec_id":rec_id, "rec_name":rec_name, "destination":destination, "weight":weight})
		return jsonify({"data": parcel})	

class Challenge(Resource):
	def put(self, parcel_id):
		pickup = request.json['pickup']
		curr.execute("""UPDATE orders SET pickup=%s WHERE parcel_id=%s """,(pickup, parcel_id))
		connection.commit()
		return jsonify({"message": "Successfuly Updated"})

class GetAllUser(Resource):
	def get(self):
		user = Usermodel()
		U = user.all_users()
		curr.execute(U,)
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