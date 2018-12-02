from flask_restful import abort
from flask import jsonify
from database import init_db
import psycopg2 
from psycopg2.extras import DictCursor
from flask_jwt_extended import create_access_token, get_jwt_identity
from passlib.hash import pbkdf2_sha256 as sha256


connection = psycopg2.connect(dbname='sendit', user='postgres', password='refuge', host='localhost')
curr = connection.cursor()

class Usermodel:
	""" Class create user model """
	def __init__(self):
		self.db = init_db()


	def register_user(self):

		sql = """INSERT INTO users(first_name, last_name, username, phone, email, password)\
					VALUES(%s, %s, %s, %s, %s, %s)"""
		return sql

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

class Users():
	def get_user_role(self):
		"""Fetch user role"""
		curr.execute("SELECT username FROM users WHERE is_admin = 'True'")
		role = curr.fetchone()
		for data in role:
			print (data)
		return data