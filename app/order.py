from flask_restful import Resource
from flask import jsonify,request
import datetime
import jwt
from functools import wraps
# from .order_models import Parcel
Orders = []

class Home(Resource):
		""" Class for home endpoint """
		def get(self):
			"""Method for home endpoint """
			response = jsonify({
					'message': 'SendIT is one of the popular courier services'
			})
			return response

class Parcels(Resource):
	""" Class for create parcels and get all parcels"""
	def post(self):
		""" Method for create a parcel order"""
		parcel_id = len(Orders)+1
		user_id = request.json['user_id']
		username = request.json['username']
		pickup = request.json['pickup']
		destination = request.json['destination']
		weight = request.json['weight']
		status = request.json['status']

		orders ={ "parcel_id":parcel_id,
							"user_id":user_id,
							"username":username,
							"pickup":pickup,
							"destination":destination,
							"weight":weight,
							"status" :status
						}

		if username.strip() == '':
			return jsonify({"message": "username should not be empty"})
		if pickup.strip() == '':
			return jsonify({"message": "Pickup should not be empty"})
		elif destination.strip() == '':
			return jsonify({"message": "Destination should not be empty"})
		elif type(weight) != int:
			return jsonify({"message": "It should be only numbers and can not be empty"})
		Orders.append(orders)
		return jsonify({"message": "Successfully Ordered"})


	def get(self):
		""" Method to get all Orders """
		if not Orders:
			return jsonify({"message": "No parcels yet"})
		return jsonify({"orders":Orders})   


class ParcelID(Resource):
	def get(self, parcelId):
		""" Method to get a specific parcel"""
		parl = [order for order in Orders if order["parcel_id"] == parcelId]
		if not parl:
			return jsonify({"message": "No order found"})
		return jsonify({'parcel': parl})

	def delete(self, parcelId):
		""" delete parcel order """
		order = [ parcel for parcel in Orders if (parcel['parcel_id'] == parcelId) ]
		if len(order) == 0:
			return jsonify({"message": "No order to be Canceled"})
		Orders.remove(order[0])
		return jsonify({'message':'Successfully Canceled'})


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


class SpecificUser(Resource):
	""" Method to get a specific user"""
	def get(self, user_id):
		Parcel = []
		for parl in Orders:
			if parl["user_id"] == user_id:
				Parcel.append(Orders)
				return Parcel
			return ({"message": "User Has no orders"})

class Cancel(Resource):
	""" Method to Cancel """
	def put(self, parcel_id):
		order = [ parcel for parcel in Orders if (parcel['parcel_id'] == parcel_id)]
		for order in Orders:
			if order["parcel_id"] == parcel_id:
				order['status'] = 'Cancelled'
			return jsonify({"parcl":order})
