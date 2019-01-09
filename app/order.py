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

connection = psycopg2.connect(dbname='d92a0rb0j8rphh', user='gaijmyignhvtkw', password='7e0acadc7013645d81437d922b7030782cdee4006cadf7f54501aa291b29d3e6', host='ec2-23-21-65-173.compute-1.amazonaws.com')
curr = connection.cursor()

class Home(Resource):
	def get(self):
		return {"message": "SendIT is one of the popular courier services"}

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

		if title.strip() == '' or pickup.strip() =='' or destination.strip() =='':
			return jsonify({"message":"Feilds  cannot be blank"})
		# elif type(rec_id) != int or type(rec_phone) != int or type(weight) != int:
			# return jsonify({"meassge":"ID, Phone and weight master be numbers"})

		current_user = get_jwt_identity()
		username = current_user

		curr.execute(""" INSERT INTO orders(title, username, pickup,rec_id, rec_phone, rec_name, destination, weight)
																				VALUES(%s, %s, %s, %s, %s, %s, %s, %s)""",\
																				(title, username, pickup, rec_id, rec_phone,rec_name, destination, weight))
		connection.commit()
		return jsonify({"message": 'Successfuly Created an Order'})

	@jwt_required
	def get(self):
		""" Method for get all Parcel Orders """
		username = get_jwt_identity()
		curr.execute(" SELECT * FROM orders WHERE username =%s", [username])
		data = curr.fetchall()
		if not data:
			return jsonify({"message":"There is no orders yet"})
		data_list = []
		for row in data:
			parcel_id = row[0]
			title = row[2]
			pickup = row[4]
			rec_id = row[5]
			rec_phone = row[6]
			rec_name = row[7]
			destination = row[8]
			weight = [9]
			data_list.append({"parcel_id":parcel_id, "title":title, "pickup":pickup, "rec_id":rec_id, "rec_name":rec_name, "destination":destination, "weight":weight})
		return jsonify({"data": data_list})	

class ModifyOrder(Resource):
	""" Class for put an order """
	@jwt_required
	def put(self, parcel_id):
		""" Method to update an order """		
		
		parcel_order = Usermodel().found_by_Id(parcel_id)

		if not parcel_order:
			return {"message":"There is no order ID {} found".format(parcel_id)}, 403	

		title = request.json['title']
		pickup = request.json['pickup']
		rec_id = request.json['rec_id']
		rec_phone = request.json['rec_phone']
		rec_name  = request.json['rec_name']
		destination = request.json['destination']
		weight = request.json['weight']

		curr.execute("""UPDATE orders SET title= %s, pickup=%s, rec_id=%s, rec_phone=%s, rec_name=%s, destination=%s, weight=%s
																														WHERE parcel_id=%s """,(title, pickup, rec_id, rec_phone, rec_name, destination, weight, parcel_id))
		connection.commit()
		return jsonify({"message": "Successfuly Updated"})

	@jwt_required
	def delete(self, parcel_id):
		username = get_jwt_identity()
		""" Method for deleting a specific order """
		parcel_order = Usermodel().found_by_Id(parcel_id)

		if not parcel_order:
			return {"message":"There is no order ID {} found".format(parcel_id)}, 403	
		curr.execute("""DELETE FROM orders WHERE parcel_id = %s AND username = %s""",(parcel_id, username))
		connection.commit()
		return jsonify({"message":"Post Deleted"})

class AnOrder(Resource):
	@jwt_required
	def put(self, parcel_id):
		destination = request.json['destination']

		curr.execute("""UPDATE orders SET destination=%s WHERE parcel_id=%s """,(destination, parcel_id))
		connection.commit()
		return jsonify({"message": "Successfuly Updated"})

