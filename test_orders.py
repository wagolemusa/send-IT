import unittest 
from __init__ import *

from run import app
import json
import os
import sys
sys.path.insert(0, os.path.abspath(".."))


class ParcalOrdersTest(unittest.TestCase):


	def test_parcel_order(self):
		"""Test API for create parcels order"""
		order = {
			"pickup": "pickup",
			"destination": "destination",
			"weight": "weight"
		}
		tester = app.test_client(self)
		response = tester.post(
											'/api/v1/parcels', data=json.dumps(order),
											content_type="application/json")
		self.assertEqual(response.status_code, 200)


	def test_get_parcel_order(self):
		"""Test API get a parcels order"""
		# tester = app.test_client(self)
		# response = tester.get(
		# 									'/api/v1/parcels/1', data=json.dumps,
		# 									content_type="application/json")
		# self.assertEqual(response.status_code, 200)
		tester = app.test_client(self)
		response = tester.get('/api/v1/parcels/1',content_type="application/json")
		self.assertEqual(response.status_code, 200)


	def test_parcel_order_edit(self):
		""" Test API for parcel update """
		order = app.test_client().post(
			'api/v1/parcels/',
			data = {'pickup': 'kisumu'})
		self.assertEqual(order.status_code, 201)

		order = app.test_client().put(
			'api/v1/parcels/1',
			data = {'pickup': 'nairobi'})
		self.assertEqual(order.status_code, 200)
		results = self.client().get('api/v1/parcels/1')
		self.assertIn('Dont just eat', str(results.data))






if __name__ =='__main__':
	unittest.main()
