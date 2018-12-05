import unittest
import json
import os
from __init__ import create_app
from database import create_table, drop_table
from models.user_model import Usermodel
connection = psycopg2.connect(dbname='sendit', user='postgres', password='refuge', host='localhost')
curr = connection.cursor()

class TestUserRegisterLogin(unittest.TestCase):

	def setUp(self):
		""" Define test verialbes """
		self.app = create_app(config_name='testing')
		self.client = self.app.test_client()
		# self.app_context.push()

		with self.app.app_context():
			create_table()
			# drop_table()


		self.users = {
			'first_name':'wagole',
			'last_name' : 'musa',
			'username' : 'same',
			'phone' :  725696042,
			'email' : 'same@gmail.com',
			'confirm_password': 'wise@12',
			'password': 'wise@12'
		}

		self.login = {
			'username': 'refuge',
			'password': 'wise@12'

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

	def test_post_parcels_order(self):
		response_login = self.client.post(
														'/api/v2/auth/signin',
														data=json.dumps(self.login),
														content_type='application/json')
		result_login = json.loads(response_login.data)
		token = result_login['access_token']


		response = self.client.post(
														'/api/v2/parcels',
														headers=dict(
															Authorization='Bearer '+token),
														data=json.dumps(self.parcels),
														content_type='application/json')
		self.assertEqual(response_post.status_code, 201)




if __name__ =='__main__':
	unittest.main()