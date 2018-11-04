import unittest 
from flask import app
import json
import os
import sys
sys.path.insert(0, os.path.abspath(".."))


class UserTestCase(unittest.TestCase):



	def test_register_user(self):
		tester = app.test_client(self)
		response = tester.post(
											'/api/v1/auth/signup',
											data=dict(firstname="wagole", lastname="musa",username="refuge",\
												phone="0725689065", country="kenya", email="homie@gmail.com", password="wise@12"),
											follow_redirects=True
		)
		self.assertIn(b'success ! you can now login to continue', response.data)



if __name__ =='__main__':
	unittest.main()
