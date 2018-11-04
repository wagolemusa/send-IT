from flask import Flask,jsonify,request, make_response
from flask_restful import Resource

import datetime
import jwt
users = dict()

class Register(Resource):
	""" User Signup """
	def post(self):
		data = request.get_json()
		firstname = data["firstname"]
		lastname  = data["lastname"]
		username  = data["username"]
		phone     = data["phone"]
		country   = data["country"]
		email     = data["email"]
		password  = data["password"]
		confirm_password = data["confirm_password"]

		if firstname.strip() == '' or lastname.strip() == '' \
				or username.strip() == '' or phone.strip() == '' \
				or country.strip() == '' or email.strip() == '' \
				or password.strip() == '' or confirm_password.strip() =='':
				return jsonify({"message":"fields con't be empty"})
		else:
			if username not in users:
				users.update({username:{"firstname":firstname, "lastname":lastname,\
					"username":username, "phone":phone, "country":country, "email":email,\
					"password":password, "confirm_password":confirm_password}})
			else:
				return jsonify({"message":"User aleady exists"})
			return jsonify({"message":"success ! you can now login to continue"})




class Profile(Resource):
	"""Show user's profile"""
	def get(self):
		Users = users
		return jsonify({'reg': Users})


class Login(Resource):
	""" Sigin  user"""
	def post(self):
		username = request.get_json()['username']
		password = request.get_json()['password']
		if username.strip() == '' or password.strip() == '':
			return jsonify({"message":"username or password con't be empty"})
		else:
			if username in users:
				return jsonify({"message":"you are successfully logged in "})
			else:
				return jsonify({"message":"Invalid credentials"})


