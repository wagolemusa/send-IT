from flask_restful import Resource
from flask import jsonify,request
import datetime
import jwt
from functools import wraps

Orders = []

def mustlogin(d):
	@wraps(d)
	def decorated(*args, **kwargs):
		if request.headers.get('	')=='':
			return jsonify({"message": "You need to first login"})
		try:
			jwt.decode(request.headers.get('x-access-token'), "djrefuge")
		except:
			return jsonify({"message": 'please sigin '})
		return d(*args, **kwargs)
	return decorated 

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
	# @mustlogin
	def post(self):
		""" Method for create a parcel order"""
		if request.method == 'POST':
			if not Orders:
				parcel = 	{ 'parcel_id': 1,
										'pickup':request.json['pickup'],
										'destination':request.json['destination'],
										'weight':request.json['weight'],
										'status':'new order'}
			else:
				parcel = 	{ 'parcel_id': Orders[-1]['parcel_id'] + 1,
										'pickup':request.json['pickup'],
										'destination':request.json['destination'],
										'weight':request.json['weight'],
										'status':'new order'}	

			Orders.append(parcel)
			if not Orders:
				return jsonify({"message": "No parcels yet"})
			return jsonify({"orders":Orders})	

class ParcelID(Resource):
	@mustlogin
	def get(self, parcelId):
		""" Method to get a specific parcel"""
		parl = [order for order in Orders if order["parcel_id"] == parcelId]
		if not parl:
			return jsonify({"message": "No order found"})
		return jsonify({'parcel': parl})

	@mustlogin
	def delete(self, parcelId):
		""" delete parcel order """
		order = [ parcel for parcel in Orders if (parcel['parcel_id'] == parcelId) ]
		if len(order) == 0:
			return jsonify({"message": "No order to be Canceled"})
		Orders.remove(order[0])
		return jsonify({'message':'Successfully Canceled'})


	@mustlogin
	def put(self, parcelId):
		""" update parcel order"""
		order = [parcel for parcel in Orders if (parcel['parcel_id'] == parcelId)]
		if 'pickup' in request.json :
			order[0]['pickup'] = request.json['pickup']
		if 'destination' in request.json:
			order[0]['destination'] = request.json['destination']
		if 'weight' in request.json:
			order[0]['weight'] = request.json['weight']
		return jsonify({'parcel':order[0]})