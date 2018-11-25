from flask_restful import abort
from flask import jsonify
from database import init_db
from psycopg2 import Error
from psycopg2.extras import DictCursor
from flask_jwt_extended import create_access_token
from passlib.hash import pbkdf2_sha256 as sha256

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

	def generate_hash(password):
		return sha256.hash(password)

	def verify_hash(password, hash):
		return sha256.verify(password, hash)
