import re
import datetime
import jwt
import psycopg2
from passlib.hash import sha256_crypt
import hashlib
import base64
from flask import Flask,jsonify,request, make_response
from flask_restful import Resource
# from flask_jwt_extended import create_access_token
from flask_jwt_extended import (create_access_token, jwt_required, 
                                get_jwt_identity, get_current_user, get_raw_jwt)

from models.user_model import Usermodel

connection = psycopg2.connect(dbname='d92a0rb0j8rphh', user='gaijmyignhvtkw', password='7e0acadc7013645d81437d922b7030782cdee4006cadf7f54501aa291b29d3e6', host='ec2-23-21-65-173.compute-1.amazonaws.com')
curr = connection.cursor()

class Register(Resource):

	def post(self):
		first_name = request.json['first_name']
		last_name = request.json['last_name']
		username = request.json['username']
		phone = request.json['phone']
		email  = request.json['email']
		password = request.json['password']
		confirm_password = request.json['confirm_password']
		if password == confirm_password:
			password = request.json['password']
		elif password != confirm_password:
			return {"message": "password does not match"}, 400

		if username.strip() == '' or first_name.strip() == '' or last_name.strip() =='' \
		or email.strip() == '':
			return {"message": "You must fill all the fields"}, 400
		elif type(phone) != int:
			return jsonify({"message": "Field can only except Numbers"})
		elif not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
			return jsonify({"message": "Invalid email"})
		elif len(password) < 5:
			return {"message":"Password too short"}, 400
		user = Usermodel()
		u = user.check_username()
		curr.execute(u, (username,))
		x = curr.fetchone()
		if x is not None:
			return {"message": "Username is already taken"}, 400

		user = Usermodel()
		E = user.check_email()
		curr.execute(E, (email,))
		y = curr.fetchone()
		if y is not None:
			return jsonify({"message": "Email is already taken"})		
		else:
			new_user = Usermodel()
			sql = new_user.register_user()
			curr.execute(sql,(first_name, last_name, username, phone, email, password))
			connection.commit()
		return {"message": "Successfully registered an account"}, 200

class Login(Resource):
	""" Class for user login """
	def post(self):
		username = request.json['username']
		password =  request.json['password']

		# hashlib.sha256(base64.b64encode\
								# (bytes(request.get_json()['password'], 'utf-8'))).hexdigest()
		if username.strip() == '' or password.strip() == '':
			return {"message": "Username or Password cannot be blank"}, 400
		user = Usermodel()
		u = user.check_username()
		curr.execute(u, (username,))
		data = curr.fetchone()
		if not data:
			return jsonify({"message":"User named {} not found".format(username)})
		if password in data:
			expire_time  = datetime.timedelta(minutes=30)
			access_token = create_access_token(identity=username, expires_delta=expire_time)
			return jsonify({"message":"Login in sucessful  as {}".format(username),
											'access_token':access_token})
		return {"message":"Invalid password"}, 400