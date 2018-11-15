import unittest 
import json
import os
import sys
from .. import create_app
sys.path.insert(0, os.path.abspath(".."))

class ParcalOrdersTest(unittest.TestCase):

	def setUp(self):
		self.app = create_app('testing')
		self.client = self.app.test_client()
		self.app_context = self.app.app_context()
		self.app_context.push()

		self.parcel = {
			"pickup":"Kisumu",
			"destination": "Nairobi",
			"weight": "56"	
		}

	def test_home_page(self):
		response = self.client.get('/api/', content_type="application/json")
		self.assertEqual(response.status_code, 200)

	def test_get_one_order(self):
		response = self.client.get('/api/v1/parcels/1',
                              data=json.dumps(self.parcel),
                              content_type='application/json'),
		self.assertEqual(response.status_code, 200)
	
	def test_post_parcel_order(self):
		"""Test API for create parcels order (POST request)"""
		order = {
			"pickup": "Kisumu",
			"destination": "Nairobi",
			"weight": "45"
		}
		response = self.client.post(
								'/api/v1/parcels', data=json.dumps(order),
											content_type="application/json")
		self.assertEqual(response.status_code, 200)

	def test_get_all_parcels(self):
		res = self.client.get('/api/v1/parcels')
		self.assertEqual(res.status_code, 200)

if __name__ =='__main__':
	unittest.main()
