from flask import Flask,jsonify,request, make_response
from flask_restful import Resource
import datetime
from functools import wraps
import jwt
import re
from .models import User


class Register(Resource):
	def post(self):
		user = User()
		firstname = request.json['firstname']
		lastname = request.json['lastname']
		username = request.json['username']
		phone = request.json['phone']
		country = request.json['country']
		email  = request.json['email']
		password = request.json['password']

		if not username or len(username.strip()) == 0:
			return jsonify({"message": "Username cannot be blank"})
		elif not email:
			return jsonify({"message": "Email cannot be blank"})
		elif not password:
			return jsonify({"message": "Password cannot be blank"})
		elif not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
			return jsonify({"message": "Input a valid email"})
		elif len(password) < 5:
			return jsonify({"message": "Password too short"})
		elif [u for u in user.users if u['email']== email]:
			return jsonify({"message": "User already exists"})	
		user.register_user(firstname, lastname, username, phone, country, email, password)
		return jsonify({"message": "registerd"})


class Login(Resource):
	""" Sigin  user"""
	def post(self):
		user_obj = User()
		username = request.json['username']
		password = request.json['password']
		user = [u for u in user_obj.users if username == u['username'] and password == u['password']]
		if  not user:
			return jsonify({"message": "Invalid username/password combination"})
		user_obj.login_user(username, password)
		return jsonify({"message": "Login successful"})


class Profile(Resource):
	"""Show user's profile"""
	# @mustlogin
	def get(self):
		user = User()
		return jsonify({'users': user.users})
	
	def get(self, userId):
		user_obj = User()
		user = [u for u in user_obj.users if u["user_id"] == userId]
		if not user:
			return jsonify({"message": "No user"})
		return jsonify({'users': user})

class Logout(Resource):
	def post(self):
		"""User logout"""
		token = request.headers.get('x-access-token')
		# token.clear()
		return jsonify({"message":"succesfuly Logout"})