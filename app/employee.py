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

connection = psycopg2.connect(dbname='d92a0rb0j8rphh', user='gaijmyignhvtkw', password='7e0acadc7013645d81437d922b7030782cdee4006cadf7f54501aa291b29d3e6', host='ec2-23-21-65-173.compute-1.amazonaws.com')
curr = connection.cursor()

class Employee(Resource):
	"""
	Class Create employee
	"""
	@jwt_required
	def post(self):
		current_user = get_jwt_identity()
		U = Users().get_user_role()
		if current_user != U:
			return {"message": "Access allowed only to Admin"}, 403

		data = request.get_json(force=True)
		first_name = data['first_name']
		last_name = data['last_name']
		username = first_name + last_name
		username = data['username']
		email  = data['email']
		permit_number = data['permit_number']
		city = data['city']
		age = data['age']
		salary = data['salary']
		nation_id = data['nation_id']
		sex = data['sex']
		phone_number = data['phone_number']
		image = data['image']

		if first_name.strip() == '' or last_name.strip() == '' or email.strip() == ''\
		or permit_number.strip() == '' or salary.strip() == '' or nation_id.strip() == ''\
		or phone_number.strip() == '' :
			return {"message": "Fields cannot be empty"}, 403

		curr.execute(""" INSERT INTO employee(first_name, last_name, username, email, permit_number, city, age, salary, nation_id, sex, phone_number, image)
																	VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",\
																	(first_name, last_name, username, email, permit_number, city, age, salary, nation_id, sex, phone_number, image))
		connection.commit()
		return {"message": "Employee Successfully Registered"}

	@jwt_required
	def get(self):
		# Get all employee form DB
		current_user = get_jwt_identity()
		U = Users().get_user_role()
		if current_user != U:
			return {"message": "Access allowed only to admin"}, 403

		curr.execute("SELECT * FROM employee ORDER BY empl_id DESC")
		connection.commit()
		dataemploy = curr.fetchall()
		if not dataemploy:
			return {"message": "There is no employee"}, 403

		employee = []
		for row in dataemploy:
			empl_id = row[0]
			first_name = row[1]
			last_name = row[2]
			username = row[3]
			email = row[4]
			permit_number = row[5]
			city = row[6]
			age = row[7]
			salary = row[8]
			nation_id = row[9]
			sex = row[10]
			phone_number = row[11]
			image = row[12]

			employee.append({"empl_id": empl_id, "first_name":first_name, "last_name":last_name, "username":username, "email":email, "permit_number":permit_number, "city": city, "age": age, "salary":salary, "nation_id": nation_id, "sex":sex, "phone_number":phone_number, "image":image})
		return jsonify({"employ": employee})


class Editemployee(Resource):
	"""
	Class Edit employee
	"""
	@jwt_required
	def put(self, empl_id):
		current_user = get_jwt_identity()
		U = Users().get_user_role()
		if current_user != U:
			return {"message": "Access allowed only to Admin"}, 403

		data = request.get_json(force=True)
		first_name = data['first_name']
		last_name = data['last_name']
		username = first_name + last_name
		username = data['username']
		email  = data['email']
		permit_number = data['permit_number']
		city = data['city']
		age = data['age']
		salary = data['salary']
		nation_id = data['nation_id']
		sex = data['sex']
		phone_number = data['phone_number']

		curr.execute("""UPDATE employee SET first_name=%s, last_name=%s, username=%s, email=%s, permit_number=%s, city=%s, age=%s, salary=%s, nation_id=%s, sex=%s, phone_number=%s
									WHERE empl_id =%s """,(first_name, last_name, username, email, permit_number, city, age, salary, nation_id, sex, phone_number))
		connection.commit()
		return {"message": "Employee's data Successfuly updated"}


class Deleteemployee(Resource):
	"""
	class Delete Employee
	"""
	@jwt_required
	def delete(self, empl_id):
		current_user = get_jwt_identity()
		U = Users().get_user_role()
		if current_user != U:
			return {"message": "Access allowed only to admin"}, 403

		curr.execute("DELETE FROM employee WHERE empl_id = %s", (empl_id,))
		return {"message":"Employee Deleted"}