import unittest 
import json
import os
import sys
from run import create_app

class UserTestCase(unittest.TestCase):

	def setUp(self):
		# from app import create_app
		self.app = create_app('testing')
		self.client = self.app.test_client()
		self.app_context = self.app.app_context()
		self.app_context.push()

	def test_register_user(self):
		""" Test API for create a user """
		user = {
    		"firstname": "wagole",
    		"lastname": "musa",
    		"username": "refuge",
			"phone": "0725689065",
			"country": "kenya", 
			"email": "homie@gmail.com",
			"password": "wise@12",
			"confirm_password": "wise@12"
    	}
		
		response = self.client.post(
									'/v1/auth/signup', data=json.dumps(user),
											content_type="application/json")
		self.assertEqual(response.status_code, 200)

	def test_login_user(self):
		""" Test API User Login credentials """
		user = {
			"username": "refuge",
			"password": "wise@12"
		}

		response = self.client.post(
											'/v1/auth/signin', data=json.dumps(user),
											content_type="application/json")
		self.assertEqual(response.status_code, 200)


	def test_login_with_invalid_credentials(self):
		"""Test API User Login with invalid credentials """
		user1 = {
			"username": "refuge",
			"password": "Pass@qee",
		}

		response = self.client.post(
											'/v1/auth/signin', data=json.dumps(user1),
											content_type="application/json")
		self.assertEqual(response.status_code, 200)		



if __name__ =='__main__':
	unittest.main()
