import unittest 
from __init__ import *

# from ...run import app
import json
import os
import sys
sys.path.insert(0, os.path.abspath(".."))


class UserTestCase(unittest.TestCase):




	# def setUp(self):
	# 	self.app = create_app('testing')
 #    self.client = self.app.test_client()

	def test_register_user(self):
		tester = app.test_client(self)
		response = tester.post(
											'/api/v1/auth/signup',data=json.dumps(
											dict(firstname="wagole", lastname="musa",username="refuge",\
												phone="0725689065", country="kenya", email="homie@gmail.com", password="wise@12")),
											content_type="application/json")
		self.assertEqual(response.status_code, 200)



if __name__ =='__main__':
	unittest.main()
