from flask import Flask,jsonify,request, make_response
from flask_restful import Resource

import datetime
import jwt
from functools import wraps
from __init__ import *


class Home(Resource):
	def get(self):
		response = jsonify({
			'status': 'ok',
			'message': 'SendIT is one of the popular courier services'
		})
		response.status_code = 200
		return response
		
class Parcels(Resource):
	@mustlogin
	def post(self):
		""" Create a parcel order"""
		parcel = {
		len(Orders)+ 1:{
		'pickup':request.get_json()['pickup'],
		'destination':request.get_json()['destination'],
		'weight':request.get_json()['weight']
		}}
		Orders.update(parcel)
		response = jsonify({
			'status': 'ok',
			'message': 'Parcel succesfuly created',
			'parcel' : Orders
		})
		response.status_code = 200
		return response


	@mustlogin
	def get(self):
		"""get all delivery parcels"""
		if Orders is not None:
			response = jsonify({
				'status': 'ok',
				'message': 'parcel found',
      	'parcel': Orders
			})
			response.status_code = 200
			return response


class ParcelID(Resource):
	@mustlogin
	def delete(self, parcel_id):
		""" delete parcel order """
		del Orders[parcel_id]
		response = jsonify({
			'status': 'error',
			'message': "Succesfuly Deleted"
		})
		response.status_code = 200
		return response
	

	@mustlogin
	def get(self, parcel_id):
		""" get a specific parcel"""
		if Orders is not None:
			response = jsonify({
				'status': 'ok',
				'message': 'parcel found',
				'parcel': (Orders[parcel_id])
			})
			response.status_code = 200
			return response
		else:
			response = jsonify({
				'status': 'error',
				'message': "Parcel not found"
			})
			response.status_code = 400
			return response



	""" update parcel order"""
	@mustlogin
	def put(self, parcel_id):

		parcel_data = request.get_json(force=True)
		data = {
			'pickup': parcel_data['pickup'],
			'destination': parcel_data['destination'],
			'weight': parcel_data['weight'],
		}
		Orders.update(parcel_id, data)
		return jsonify({"message": "Succesfuly updated"})


		# update = [parl for parl in Orders if (parl['id'] == parcel_id)]
		# if 'pickup' in request.get_json():
		# 	update[0]['pickup'] = request.get_json()['pickup']
		# if 'destination' in request.get_json():
		# 	update[0]['destination'] = request.get_json()['destination']
		# if 'weight' in request.get_json():
		# 	update[0]['weight'] = rrequest.get_json()['weight']
		# return jsonify({'parl':update[0]})