import unittest 
from __init__ import *

from run import app
import json
import os
import sys
sys.path.insert(0, os.path.abspath(".."))


class ParcalOrdersTest(unittest.TestCase):



	def test_home_page(self):
		tester = app.test_client(self)
		response = tester.get('/api/', content_type="application/json")
		self.assertEqual(response.status_code, 200)



	def test_parcel_order(self):
		"""Test API for create parcels order (POST request)"""
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
		"""Test API get a parcels order (GET Request)"""
		# tester = app.test_client(self)
		# response = tester.get(
		# 									'/api/v1/parcels/1', data=json.dumps,
		# 									content_type="application/json")
		# self.assertEqual(response.status_code, 200)
		response = app.test_client().get('/api/v1/parcels/1',content_type="application/json")
		self.assertEqual(response.status_code, 200)


	def test_parcel_order_edit(self):
		""" Test API for parcel update (PUT request)"""
		response = app.test_client().post(
			'api/v1/parcels/',
			data = {'pickup': 'kisumu'})

		self.assertEqual(response.status_code, 201)
		response = app.test_client().put(
			'api/v1/parcels/1',
			data = {'pickup': 'nairobi'})
		self.assertEqual(response.status_code, 200)
	


	def test_show_all_parcel_order(self):
		""" Test API for getting all the parcel orders (GET request)"""

		tester = app.test_client(self)
		response = tester.get(
											'/api/v1/parcels',content_type="application/json")
		self.assertEqual(response.status_code, 200)


	def test_delete__an_parcel_order(self):
		""" Test API for delete an  parcel orders (DELETE request)"""
		response = app.test_client().post(
			'api/v1/parcels/',

			data = {'pickup': 'kisumu'})
		self.assertEqual(response.status_code, 200)

		response = app.test_client().delete(
			'api/v1/parcels/1',
			data = {'pickup': 'nairobi'})
		self.assertEqual(response.status_code, 200)
	










if __name__ =='__main__':
	unittest.main()
