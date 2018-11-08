from flask import Flask,jsonify,request, make_response
from flask_restful import Resource
import datetime
from functools import wraps
from __init__ import *
import jwt


class Register(Resource):
	def post(self):
		""" User Signup """
		data = request.get_json()
		firstname = data["firstname"]
		lastname  = data["lastname"]
		username  = data["username"]
		phone     = data["phone"]
		country   = data["country"]
		email     = data["email"]
		password  = data["password"]
		confirm_password = data["confirm_password"]
		if Validation.valid_email(email):
			if Validation.password_verify(password, confirm_password):
				if firstname.strip() == '' or lastname.strip() == '' \
					or username.strip() == '' or phone.strip() == '' \
					or country.strip() == '' or email.strip() == '' \
					or password.strip() == '' or confirm_password.strip() =='':
					response = jsonify({
						'status': 'error',
						'message': 'fields cont be empty'
					})
					return response

				else:
					if username not in users:
						users.update({username:{"firstname":firstname, "lastname":lastname,\
						"username":username, "phone":phone, "country":country, "email":email,\
						"password":password, "confirm_password":confirm_password}})
					else:
						response = jsonify({
							'status': 'error',
							'message': 'User aleady exists'
						})
						return response
			else:
				response = jsonify({
					'status': 'error',
					'message': 'password and confirm password do not match'
				})
				return response
			response = jsonify({
				'status': 'ok',
				'message': 'success ! you can now login to continue'
			})
			return response

class Login(Resource):
	""" Sigin  user"""
	def post(self):
		username = request.get_json()['username']
		password = request.get_json()['password']
		payload = {}

		if username.strip() == '' or password.strip() == '':
			return jsonify({"message":"username or password con't be empty"})
		else:
			if username in users:
				payload = {"username":username, "password":password,\
																"exp":datetime.datetime.utcnow()+datetime.timedelta(minutes=45)}
				token = jwt.encode(payload, 'djrefuge')
				response = jsonify({
					'status':'ok',
					'message': ({"token":token.decode('utf-8')})
				})
				return response
			else:
				response = jsonify({
					'status':'error',
					'message':'Invalid credentials'
				})
				return response

class Profile(Resource):
	"""Show user's profile"""
	@mustlogin
	def get(self):
		if users is not None:
			response = jsonify({
				'status': 'ok',
				'message': 'user found',
      	'reg': users
			})
			return response
		else:
			response = jsonify({
				'status': 'error',
				'message': "user not found"
			})
			return response



class Logout(Resource):
	@mustlogin
	def post(self):
		"""User logout"""
		token = request.headers.get('x-access-token')
		# token.clear()
		return jsonify({"message":"succesfuly Logout"})