from flask import Flask,jsonify,request, make_response
from flask_restful import Resource

import datetime
import jwt
from functools import wraps
from __init__ import *


class Home(Resource):
	def get(self):
		return {"message": "SendIT is one of the popular courier services"}


class Parcels(Resource):
	@mustlogin
	def post(self):
		parcel = {
		len(Orders)+ 1:{
		'pickup':request.get_json()['pickup'],
		'destination':request.get_json()['destination'],
		'weight':request.get_json()['weight']
		}}
		Orders.update(parcel)
		return jsonify(Orders)

	"""get all delivery parcels"""
	@mustlogin
	def get(self):
		return make_response(jsonify(
			{
			'Status': "Ok",
      'Message': "Success",
      'parcel': Orders
      }), 200)

class ParcelID(Resource):
	""" delete parcel order """
	@mustlogin
	def delete(self, parcel_id):
		del Orders[parcel_id]
		return jsonify({"message": "Succesfuly Deleted"})
		

	""" get a specific parcel"""
	@mustlogin
	def get(self, parcel_id):
		return make_response(jsonify(
			{
			'Status': "Ok",
      'Message': "Success",
      'parcel': (Orders[parcel_id])
      }), 200)


	""" update parcel order"""
	@mustlogin
	def put(self, parcel_id):
		upd = [dics for dics in Orders if (dics['id'] == parcel_id)]
		if 'pickup' in request.get_json():
			upd[0]['pickup'] = request.get_json()['pickup']
		if 'destination' in request.get_json():
			upd[0]['destination'] = request.get_json()['destination']
		if 'weight' in request.get_json():
			upd[0]['weight'] = rrequest.get_json()['weight']
		return jsonify({'dics':upd[0]})