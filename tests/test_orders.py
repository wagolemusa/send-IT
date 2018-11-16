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
		response = self.client.get('/', content_type="application/json")
		self.assertEqual(response.status_code, 200)

	def test_get_one_order(self):
		order = {
			"parcel_id":1,
			"pickup": "Kisumu",
			"destination": "Nairobi",
			"weight": "45"
		}
		response = self.client.get('/v1/parcels/1',
                              data=json.dumps(order),
                              content_type='application/json')
		self.assertEqual(response.status_code, 200)
	
	def test_post_parcel_order(self):
		"""Test API for create parcels order (POST request)"""
		order = {
			"pickup": "Kisumu",
			"destination": "Nairobi",
			"weight": "45"
		}
		response = self.client.post(
								'/v1/parcels', data=json.dumps(order),
											content_type="application/json")
		self.assertEqual(response.status_code, 200)

	def test_get_all_parcels(self):
		response = self.client.get('/v1/parcels', content_type="application/json")
		self.assertEqual(response.status_code, 405)


	def test_delete_parcels(self):
		order = {
			"parcel_id":1,
			"pickup": "Kisumu",
			"destination": "Nairobi",
			"weight": "45"
		}
		response = self.client.delete('/v1/parcels/1',
                              data=json.dumps(order),
                              content_type='application/json')
		self.assertEqual(response.status_code, 200)


if __name__ =='__main__':
	unittest.main()
