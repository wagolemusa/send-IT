import datetime
import psycopg2
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

class Home(Resource):
	def get(self):
		return {"message": "Hello, World!"}

class CreateParcel(Resource):
	""" Class for create parcel methods """
	@jwt_required
	def post(self):
		title = request.json['title']
		pickup = request.json['pickup']
		rec_id = request.json['rec_id']
		rec_phone = request.json['rec_phone']
		rec_name  = request.json['rec_name']
		destination = request.json['destination']
		weight = request.json['weight']

		if title.strip() == '':
			return jsonify({"message":"Title cannot be blank"})
		elif pickup.strip() == '':
			return jsonify({"message":"Pickup cannot be blank"})
		elif type(rec_id) != int:
			return jsonify({"meassge":"ID Number can only be numbers"})
		elif type(rec_phone) != int:
			return jsonify({"message":"Phone can only be numbers"})
		elif destination.strip() == '':
			return jsonify({"message":"Destination cannot be black"})
		elif type(weight) != int:
			return jsonify({"message": "Weight can only be numbers"})

		current_user = get_jwt_identity()
		username = current_user

		curr.execute(""" INSERT INTO orders(title, username, pickup,rec_id, rec_phone, rec_name, destination, weight)
																				VALUES(%s, %s, %s, %s, %s, %s, %s, %s)""",\
																				(title, username, pickup, rec_id, rec_phone,rec_name, destination, weight))
		connection.commit()
		return jsonify({"message": 'Successfuly Created an Order'})




	
