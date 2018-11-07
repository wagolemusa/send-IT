import unittest 
from __init__ import *

from run import app
import json
import os
import sys
sys.path.insert(0, os.path.abspath(".."))


class ParcalOrdersTest(unittest.TestCase):


	def test_parcel_order(self):
		"""Test for create parcels order"""
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




if __name__ =='__main__':
	unittest.main()
