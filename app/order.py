from flask_restful import Resource
from flask import jsonify,request
from __init__ import *

class Home(Resource):
		""" Class for home endpoint """
		def get(self):
			"""Method for home endpoint """
			response = jsonify({
					'status': 'ok',
					'message': 'SendIT is one of the popular courier services'
			})
			return response

class Parcels(Resource):
	""" Class for create parcels and get all parcels"""
	@mustlogin
	def post(self):
		""" Method for create a parcel order"""
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
		return response

	@mustlogin
	def get(self):
		""" Method to get all delivery parcels"""
		if Orders is not None:
			response = jsonify({
				'status': 'ok',
				'message': 'parcel found',
      	'parcel': Orders
			})
			return response

class ParcelID(Resource):
	""" Class for detele, get an parcel, put parcel by ID """
	@mustlogin
	def delete(self, parcel_id):
		""" delete parcel order """
		del Orders[parcel_id]
		response = jsonify({
			'status': 'error',
			'message': "Succesfuly Deleted"
		})
		return response
	

	@mustlogin
	def get(self, parcel_id):
		""" Method to get a specific parcel"""
		if Orders is not None:
			response = jsonify({
				'status': 'ok',
				'message': 'parcel found',
				'parcel': (Orders[parcel_id])
			})
			return response
		response = jsonify({
				'status': 'error',
				'message': "Parcel not found"
		})
		return response

	@mustlogin
	def put(self, parcel_id):
		""" update parcel order"""
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