from flask_restful import abort
from flask import jsonify
from database import Database
import psycopg2 
from psycopg2.extras import DictCursor
from flask_jwt_extended import create_access_token, get_jwt_identity
from passlib.hash import pbkdf2_sha256 as sha256


# connection = psycopg2.connect(dbname='d92a0rb0j8rphh', user='gaijmyignhvtkw', password='7e0acadc7013645d81437d922b7030782cdee4006cadf7f54501aa291b29d3e6', host='ec2-23-21-65-173.compute-1.amazonaws.com')
# curr = connection.cursor()

class Usermodel:
	""" Class create user model """
	def __init__(self):
		self.db = Database.init_db()


	def register_user(self):

		sql = """INSERT INTO users(first_name, last_name, username, phone, email, password)\
					VALUES(%s, %s, %s, %s, %s, %s)"""
		return sql

	def data_price(self):
		data = """ INSERT INTO prices(car_number, from_location, to_location,period, arrival, price, day_time)
					VALUES(%s, %s, %s, %s, %s, %s, %s)"""
		return data

	def check_username(self):
		sql = "SELECT * FROM users WHERE username = %s"
		return sql

	def check_email(self):
		sql = "SELECT * FROM users WHERE email = %s"
		return sql

	def get_user_by_username(self):
		""" Method fetch user by username """
		sql = "SELECT password FROM users WHERE username = %s", [parcel_id]
		return sql

	def get_specific_order(self, parcel_id):
		""" Fetch product by Id """
		sql = "SELECT * FROM orders WHERE parcel_id = %s"
		return sql

	def all_users(self):
		sql = "SELECT * FROM users"
		return sql

	def check_status(self):
		sql = "SELECT status FROM orders WHERE parcel_id = %s"
		return sql


	def found_by_Id(self, parcel_id):
		sql = "SELECT * FROM orders WHERE parcel_id = %s"
		curr.execute(sql, (parcel_id,)) 
		data = curr.fetchone()
		return data
		

	def delete(self, parcel_id):
		curr.execute("DELETE FROM orders WHERE parcel_id = %s", (parcel_id,))
		connection.commit()


	def senddata(self):
		sql = "SELECT phone FROM users"
		return sql

class Users():
	def get_user_role(self):
		"""Fetch user role"""
		curr.execute("SELECT username FROM users WHERE is_admin = 'True'")
		role = curr.fetchone()
		for data in role:
			print (data)
		return data

