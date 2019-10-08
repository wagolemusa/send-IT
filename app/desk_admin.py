import datetime
import psycopg2
import smtplib
import random
import base64
from flask import Flask,jsonify,request, make_response
from flask_restful import Resource
from functools import wraps
from flask_jwt_extended import (
  	jwt_required, create_access_token, get_current_user, 
    get_jwt_identity 
)
from models.user_model import Usermodel, Users
import africastalking

types_status = ["delivered", "cancled"]

connection = psycopg2.connect(dbname='d92a0rb0j8rphh', user='gaijmyignhvtkw', password='7e0acadc7013645d81437d922b7030782cdee4006cadf7f54501aa291b29d3e6', host='ec2-23-21-65-173.compute-1.amazonaws.com')
curr = connection.cursor()

class Deskbooking(Resource):
	@jwt_required

	def post(self):

		"""
		This methods helps a user to book the transport service
		"""
		current_user = get_jwt_identity()
		U = Users().get_user_role()
		if current_user != U:
			return {"message": "Access allowed only to admin"}, 403

		data = request.get_json(force=True)
		bookingref = random.randint(1, 100000)
		bookingref = str(bookingref)
		car_number = data['car_number']
		from_location = data['from_location']
		to_location = data['to_location']
		price = data['price']
		customer_name = data['customer_numberomer_name']
		customer_number = data['customer_number']
		quantiy = data['quantiy']
		date_when = data['date_when']
		time_at = data['time_at']
		amount = data['amount']
		username = current_user
		curr.execute(""" INSERT INTO desk(bookingref, username, car_number,from_location, to_location, price, customer_name, customer_number,\
																			 quantiy, date_when, time_at, amount)
																			VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",\
																			(bookingref, username, car_number, from_location, to_location, price, customer_name, customer_number, quantiy, date_when, time_at, amount))
		connection.commit()
		return {"message": "Succussfully Created"}







