import unittest 
from __init__ import *

from run import app
import json
import os
import sys
sys.path.insert(0, os.path.abspath(".."))


class UserTestCase(unittest.TestCase):

		# def setUp(self):
		# self.app = app("");
		# self.client = self.app.test_client()

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
		tester = app.test_client(self)
		response = tester.post(
											'/api/v1/auth/signup', data=json.dumps(user),
											content_type="application/json")
		self.assertEqual(response.status_code, 200)

	def test_login_user(self):
		""" Test API User Login credentials """
		user = {
			"username": "refuge",
			"password": "wise@12"
		}
		tester = app.test_client(self)
		response = tester.post(
											'/api/v1/auth/signin', data=json.dumps(user),
											content_type="application/json")
		self.assertEqual(response.status_code, 200)


	def test_login_with_invalid_credentials(self):
		"""Test API User Login with invalid credentials """
		user1 = {
			"username": "refuge",
			"password": "Pass@qee",
		}
		tester = app.test_client(self)
		response = tester.post(
											'/api/v1/auth/signin', data=json.dumps(user1),
											content_type="application/json")
		self.assertEqual(response.status_code, 200)		



	def test_get_user_details(self):
		""" Test API Get user datels """
		user1 = {
    	"firstname": "wagole",
    	"lastname": "musa",
    	"username": "refuge",
			"phone": "0725689065",
			"country": "kenya", 
			"email": "homie@gmail.com",
		}
		tester = app.test_client(self)
		response = tester.get(
											'/api/v1/users', data=json.dumps(user1),
											content_type="application/json")
		self.assertEqual(response.status_code, 200)		


if __name__ =='__main__':
	unittest.main()
