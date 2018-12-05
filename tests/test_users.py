import unittest
import json
import os

import create_app
from models.user_model import Usermodel

class TestUserRegisterLogin(unittest.TestCase):

	def setUp(self):
		""" Define test verialbes """
		self.app = create_app(config_name='testing')
		self.client = self.app.test_client()
		self.app_context.push()

		with self.app.app_context():
			create_table()
			drop_table()


		self.register = {
			'first_name':'wagole',
			'last_name' : 'musa',
			'username' : 'refuge',
			'phone' :  '0725696042',
			'email' : 'homiemusa@gmail.com',
			'password': 'wise@12'
		}

		self.login = {
			'username': 'refuge',
			'password': 'wise@12'

		}

	def test_register(self):
		""" Method register """
		response = self.client.post(
										'api/v2/auth/signup',
										header=dict(Authorization='Bearer '+token),
										data=json.dumps(self.register),
										content_type='application/json')
		result = json.loads(response.register)
		self.assertEqual(result['message'], 'Successfully registered an account')
		self.assertEqual(response.status_code, 201)







	if __name__ =='__main__':
		unittest.main()