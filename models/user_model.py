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
		sql = "SELECT password FROM users WHERE username = %s"
		return sql

	def get_specific_order(self):
		""" Fetch product by Id """
		sql = "SELECT * FROM orders WHERE parcel_id = %"
		return sql

		
class Users(Usermodel):
	# def get_user_role(self):
	# 	"""Fetch user role"""
	# 	current_user = get_jwt_identity()
	# 	sql = "SELECT is_admin FROM users WHERE username = %s"
	# 	curr.execute(sql,)
	# 	is_admin = curr.fetchone()
	# 	return is_admin
	def fetch_by_username(self, username):
		""" fetch user by username """
		curr.execute("SELECT * FROM users WHERE username=%s", (username,))
		user = curr.fetchone()

	def get_user_role(self, username):
		"""Fetch user role"""
		current_user = get_jwt_identity()
		sql = "SELECT is_admin FROM users WHERE username = %s"
		self.cursor.execute(sql, (current_user,))
		role = self.cursor.fetchone()
		return role