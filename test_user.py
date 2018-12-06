import unittest
import json
import psycopg2
import os
from __init__ import create_app
from database import create_table, drop_table, admin, init_db

class TestUserRegisterLogin(unittest.TestCase):

	def setUp(self):
		""" Define test verialbes """
		self.app = create_app('testing')
		self.client = self.app.test_client()
		with self.app.app_context():

			# drop_table()
			create_table()
			# admin()


		self.users = {
			'first_name':'wagole',
			'last_name' : 'musa',
			'username' : 'jemo',
			'phone' :  725696042,
			'email' : 'same@gmail.com',
			'confirm_password': 'wise@12',
			'password': 'wise@12'
		}

		self.login = {
			'username': 'muae',
			'password': 'wise@12'

		}

		self.wrong_password = {
			'username': 'jemo',
			'password': 'wise@12xxxx'
		}

		self.empty_field = {
			'username': '',
			'password': ''
		}
		self.exist_username = {
			'first_name':'wagole',
			'last_name' : 'musa',
			'username' : 'jemo',
			'phone' :  725696042,
			'email' : 'same@gmail.com',
			'confirm_password': 'wise@12',
			'password': 'wise@12'
		}

		self.short_password = {
			'first_name':'wagole',
			'last_name' : 'musa',
			'username' : 'jemo',
			'phone' :  725696042,
			'email' : 'same@gmail.com',
			'confirm_password': 'wi2',
			'password': 'wi2'
		}

		
		self.Invalid_email = {
			'first_name':'wagole',
			'last_name' : 'musa',
			'username' : 'jemo',
			'phone' :  725696042,
			'email' : 'samegmail.com',
			'confirm_password': 'wise@12',
			'password': 'wise@12'
		}


	def test_register_user(self):
		""" Method  tests for user registration """
		response = self.client.post(
										'/api/v2/auth/signup',
										data=json.dumps(self.users),
										content_type='application/json')
		self.assertIn(b'Successfully registered an account',response.data)
		self.assertEqual(response.status_code, 201)


	def test_user_login(self):
		""" Methods tests for user Login """
		response = self.client.post(
										'/api/v2/auth/signin',
										data=json.dumps(self.login),
										content_type='application/json')
		# self.assertIn(b'Login in sucessful', response.data)
		self.assertEqual(response.status_code, 200)

	def test_wrong_password(self):
		""" Method tests for wrong password """
		response = self.client.post(
										'/api/v2/auth/signin',
										data=json.dumps(self.wrong_password),
										content_type='application/json')
		self.assertIn(b'Invalid password', response.data)
		self.assertEqual(response.status_code, 400)

	def test_empty_field(self):
		""" Method tests login with empty strings """
		response = self.client.post(
									'/api/v2/auth/signin',
									data=json.dumps(self.empty_field),
									content_type='application/json')
		self.assertIn(b'Username or Password cannot be blank', response.data)
		self.assertEqual(response.status_code, 400)


	def test_username_taken(self):
		""" Method tests if username is taken"""
		response = self.client.post(
							'/api/v2/auth/signup',
							data=json.dumps(self.exist_username),
							content_type='application/json')
		self.assertIn(b'Username is already taken', response.data)
		self.assertEqual(response.status_code, 400)


	def test_short_password(self):
		""" Method test short password """
		response = self.client.post(
							'/api/v2/auth/signup',
							data=json.dumps(self.short_password),
							content_type='application/json')
		self.assertIn(b'Password too short', response.data)

	def test_invalid_email(self):
		""" Method test short password """
		response = self.client.post(
							'/api/v2/auth/signup',
							data=json.dumps(self.Invalid_email),
							content_type='application/json')
		self.assertIn(b'Invalid email', response.data)

	def tearDown(self):
		"""
		Tear Down
		"""
		with self.app.app_context():
			drop_table()

if __name__ =='__main__':
	unittest.main()