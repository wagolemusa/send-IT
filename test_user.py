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
			drop_table()
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
			'username': 'refuge',
			'password': 'wise@12'

		}

	def test_register_user(self):
		""" Method register """
		response = self.client.post(
										'/api/v2/auth/signup',
										data=json.dumps(self.users),
										content_type='application/json')
		# result = json.loads(response.data)
		self.assertIn(b'Successfully registered an account',response.data)
		self.assertEqual(response.status_code, 200)


	


if __name__ =='__main__':
	unittest.main()