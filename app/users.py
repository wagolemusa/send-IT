from flask import Flask,jsonify,request, make_response
from flask_restful import Resource
import datetime
from functools import wraps
import jwt
import re

users = []

class Register(Resource):
	def post(self):
		user_id  = len(users)+1
		firstname = request.json['firstname']
		lastname = request.json['lastname']
		username = request.json['username']
		phone = request.json['phone']
		country = request.json['country']
		email  = request.json['email']
		password = request.json['password']
		confirm_password = request.json['confirm_password']

		User = {"user_id":user_id,
						"firstname":firstname,
						"lastname" :lastname,
						"username":username,
						"phone": phone,
						"country":country,
						"email":email,
						"password":password,
						"confirm_password":confirm_password
		}

		if not username or len(username.strip()) == 0:
			return jsonify({"message": "Username cannot be blank"})
		if firstname.strip() == '':
			return jsonify({"message": "Firstname cannot be blank"})
		elif lastname.strip() == '':
			return jsonify({"message": "Lastname cannot be blant"})
		elif country.strip() == '':
			return jsonify({"message": "Country cannot be black"})
		elif type(phone) != int:
			return jsonify({"message": "Field can only except Numbers"})
		elif not email:
			return jsonify({"message": "Email cannot be blank"})
		elif not password:
			return jsonify({"message": "Password cannot be black"})
		elif password != confirm_password:
			return jsonify({"message": "Password does not match"})
		elif not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
			return jsonify({"message": "Invalid email"})
		elif len(password) < 5:
			return jsonify({"message": "Password too short"})
		elif [u for u in users if u['username']== username]:
			return jsonify({"message": "Username already exists"})
		elif [u for u in users if u['email']== email]:
			return jsonify({"message": "Email already exists"})
		users.append(User)
		return jsonify({"message": "Registration successful"})


class Login(Resource):
	""" Sigin  user"""
	def post(self):
		username = request.get_json()['username']
		password = request.get_json()['password']
		if username.strip() == '' or password.strip() == '':
			return jsonify({"message":"username or password con't be empty"})

		user = [u for u in users if username == u['username'] and password == u['password']]
		if not user:
			return jsonify({"message": "Invalid username and password"})
		payload = {"username":username, "password":password,\
																"exp":datetime.datetime.utcnow()+datetime.timedelta(minutes=20)}
		token = jwt.encode(payload, 'djrefuge')
		return jsonify({"token":token.decode('utf-8')})
	
class Profile(Resource):
	"""Show user's profile"""
	def get(self):
		if not users:
			return jsonify({"message": "There is no user"})
		return jsonify({"Users": users})

class UserID(Resource):
	def get(self, userId):
		Users = [user for user in users if user['user_id'] == userId]
		if not Users:
			return jsonify({"message":"There is no user yet"})
		return jsonify({"user": Users})

class Logout(Resource):
	def post(self):
		"""User logout"""
		token = request.headers.get('x-access-token')
		# token.clear()
		return jsonify({"message":"succesfuly Logout"})