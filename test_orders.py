import unittest 
import json
import os
import sys
from run  import create_app

class ParcalOrdersTest(unittest.TestCase):

	def setUp(self):
		# from app import create_app
		self.app = create_app('testing')
		self.client = self.app.test_client()
		self.app_context = self.app.app_context()
		self.app_context.push()


	def test_home_page(self):
		response = self.client.get('/api/', content_type="application/json")
		self.assertEqual(response.status_code, 200)

	def test_get_one_order(self):
		response = self.client.get('/api/v1/parcels/1')
		self.assertEqual(response.status_code, 200)
	
	def test_post_parcel_order(self):
		"""Test API for create parcels order (POST request)"""
		order = {
			"user_id":1,
			"username":"refuge",
			"pickup": "Kisumu",
			"destination": "Nairobi",
			"weight": 45,
			"status":"active"
		}
		response = self.client.post(
								'/api/v1/parcels', data=json.dumps(order),
											content_type="application/json")
		self.assertEqual(response.status_code, 200)


	def test_if_one_field_empty(self):
		"""Test API for create parcels order (POST request)"""
		order = {
			"user_id":1,
			"username":"refuge",
			"pickup": "",
			"destination": "Nairobi",
			"weight": 45,
			"status":"active"
		}
		response = self.client.post(
								'/api/v1/parcels', data=json.dumps(order),
											content_type="application/json")
		self.assertIn(b'Pickup should not be empty', response.data)

	def test_only_numbers(self):
		"""Test API for create parcels order (POST request)"""
		order = {
			"user_id":1,
			"username":"refuge",
			"pickup": "Nairobi",
			"destination": "Nairobi",
			"weight": "eess",
			"status":"active"
		}
		response = self.client.post(
								'/api/v1/parcels', data=json.dumps(order),
											content_type="application/json")
		self.assertIn(b'It should be only numbers and can not be empty', response.data)

	def test_get_all_parcels(self):
		response = self.client.get('/api/v1/parcels')
		self.assertEqual(response.status_code, 200)

	def test_get_user_parcel(self):
		"""Test API for create parcels order (POST request)"""
		order = {
			"user_id":1,
			"username":"refuge",
			"pickup": "Kisumu",
			"destination": "Nairobi",
			"weight": 45,
			"status":"active"
		}
		response = self.client.get('/api/v1/user/1/parcels')
		self.assertEqual(response.status_code, 200)

	def test_delete_parcels(self):
		response = self.client.delete('/api/v1/parcels/1')
		self.assertEqual(response.status_code, 200)

	def test_cancel_order(self):
		"""Test API for create parcels order (POST request)"""
		order = {
			"user_id":1,
			"username":"refuge",
			"pickup": "Kisumu",
			"destination": "Nairobi",
			"weight": 45,
			"status":"Cancelled"
		}
		response = self.client.put(
								'/api/v1/parcels/1/cancel', data=json.dumps(order),
											content_type="application/json")
		self.assertEqual(response.status_code, 200)



	def test_specific_user_order(self):
		response = self.client.get('api/v1/user/1/parcels')
		self.assertEqual(response.status_code, 200)

if __name__ =='__main__':
	unittest.main()
