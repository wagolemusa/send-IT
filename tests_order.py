import unittest
import json
import os
from __init__ import create_app
from database import create_table, drop_table
from models.user_model import Usermodel
from flask_jwt_extended import (
  	jwt_required, create_access_token, get_current_user, 
    get_jwt_identity 
)

class TestUserRegisterLogin(unittest.TestCase):

	def setUp(self):
		""" Define test verialbes """
		self.app = create_app(config_name='testing')
		self.client = self.app.test_client()
		# self.app_context.push()

		with self.app.app_context():
			create_table()
			# drop_table()


		self.signup_user = {
			'first_name':'wagole',
			'last_name' : 'musa',
			'username' : 'same',
			'phone' :  725696042,
			'email' : 'same@gmail.com',
			'confirm_password': 'wise@12',
			'password': 'wise@12'
		}

		self.login_user = {
			'username': 'musa',
			'password': 'wise@12'

		}

		self.admin_login ={
			'username': 'admin',
			'password': 'admin@wise'
		}

		self.parcels = {
			'title' : 'phones',
			'username': 'refuge',
			'pickup' : 'kisumu',
			'rec_id' : 4456777,
			'rec_phone': 725678945,
			'rec_name' : 'musa',
			'destination':'nairobi',
			'weight' : 56,
			'status' : 'In Transit'

		}

	def signup(self):
		""" user signup function """
		response = self.client.post(
							'/api/v2/auth/signup',
							data=json.dumps(self.signup_user),
							headers={'content-type': 'application/json'}
		)
		return response

	def login(self):
		""" user login """
		response = self.client.post(
							"/api/v2/auth/signin",
							data=json.dumps(self.login_user),
							headers={'content-type': 'application/json'}
		)
		return response

	def login_admin(self):
		""" user login """
		response = self.client.post(
							"/api/v2/auth/signin",
							data=json.dumps(self.admin_login),
							headers={'content-type': 'application/json'}
		)
		return response

	def get_user_token(self):
		""" get token """
		self.signup()
		response = self.login()
		token = json.loads(response.data.decode('utf-8')).get("token", None)
		return token

	def get_admin_token(self):
		response = self.login_admin()
		token = json.loads(response.data.decode('utf-8')).get("token", None)
		return token

	# def test_post_parcels_order(self):
	# 	token = self.get_user_token()
	# 	response = self.client.post(
	# 													"api/v2/parcels",
	# 													# headers={'content_type': 'application/json',
	# 													# 				'Authorization': f'Bearer {token}'}

	# 													# )
	# 													# data=json.dumps(self.parcels),							
	# 													# data=json.dumps(self.parcels),
	# 													headers=dict(
	# 													Authorization='Bearer '+token),
	# 													data=json.dumps(self.parcels),							
	# 													content_type='application/json')
	# 	self.assertEqual(b'Successfuly Created an Order', response.data)
	# 	self.assertEqual(response_post.status_code, 200)


	def test_user_post(self):
		# self.signup()
		response_login = self.client.post(
												'/api/v2/auth/signin',
												data=json.dumps(self.admin_login),
												content_type='application/json')
		result_login = json.loads(response_login.data.decode('utf-8'))
		token = result_login

		response = self.client.post(
    													'/api/v2/parcels', 
    													data=json.dumps(self.parcels),
    													headers={'content_type': 'application/json',
																				'Authorization':'Bearer {token}'})     
		# result = json.loads(response.data.decode('utf-8'))
		# self.assertIn(b'Successfuly Created an Order', response.data)
		self.assertEqual(response.status_code, 200)


	def test_admin_get_all_parcel(self):
		token = self.get_admin_token()
		response = self.client.get(
												"/api/admin/v2/parcels",
	            					headers={'content-type': 'application/json',
												'Authorization': 'Bearer {token}'}
												)
		self.assertEqual(response.status_code, 200)




	# def tearDown(self):
	# 	"""
	# 	Tear Down
	# 	"""
	# 	with self.app.app_context():
	# 		drop_table()

if __name__ =='__main__':
	unittest.main()