import re
import datetime
import psycopg2
from passlib.hash import sha256_crypt
import hashlib
import base64
from flask import Flask,jsonify,request, make_response
from flask_restful import Resource
from functools import wraps
from flask_jwt_extended import (
  	jwt_required, create_access_token, get_current_user, 
    get_jwt_identity 
)
from models.user_model import Usermodel

connection = psycopg2.connect(dbname='sendit', user='postgres', password='refuge', host='localhost')
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
			password = sha256_crypt.encrypt(str(request.get_json()['password']))

		elif password != confirm_password:
			return jsonify({"message": "password does not match"})
		if not username or len(username.strip()) == 0:
			return jsonify({"message": "Username cannot be blank"})
		elif first_name.strip() == '':
			return jsonify({"message": "Firstname cannot be blank"})
		elif last_name.strip() == '':
			return jsonify({"message": "Lastname cannot be blant"})
		elif type(phone) != int:
			return jsonify({"message": "Field can only except Numbers"})
		elif not email:
			return jsonify({"message": "Email cannot be blank"})
		elif not password:
			return jsonify({"message": "Password cannot be black"})

		elif not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
			return jsonify({"message": "Invalid email"})
		elif len(password) < 5:
			return jsonify({"message": "Password too short"})
		user = Usermodel()
		u = user.check_username()
		curr.execute(u, (username,))
		x = curr.fetchone()
		if x is not None:
			return jsonify({"message": "Username is already taken"})

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
		return {"message": "Successfully registered an account"}

class Login(Resource):
	""" Class for user login """
	def post(self):
		username = request.json['username']
		password =  request.json['password']

		# hashlib.sha256(base64.b64encode\
								# (bytes(request.get_json()['password'], 'utf-8'))).hexdigest()
		if username.strip() == '':
			return jsonify({"message": "Username cannot be blank"})
		elif password.strip() == '':
			return jsonify({"message":"Password cannot be blank"})
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
		return jsonify({"message":"Invalid password"})