from flask import Flask,jsonify,request, make_response
from flask_restful import Resource

import datetime
import jwt
from functools import wraps
from __init__ import *
Orders ={}


def mustlogin(d):
	@wraps(d)
	def decorated(*args, **kwargs):
		if request.headers.get('x-access-token')=='':
			return make_response(("You need to first login "), 201)
		try:
			jwt.decode(request.headers.get('x-access-token'), "djrefuge")
		except:
			return jsonify({"message": 'please sigin '})
		return d(*args, **kwargs)
	return decorated 


class Home(Resource):
    def get(self):
        return {"message": "SendIT is one of popular courier services"}


class Parcels(Resource):
	@mustlogin
	def post(self):
		parl = {
		len(Orders)+ 1:{
		'pickup':request.get_json()['pickup'],
		'destination':request.get_json()['destination'],
		'weight':request.get_json()['weight']
		}}
		Orders.update(parl)
		return jsonify(Orders)

		# parl = {
		# len(Orders)+ 1:{
		# # order = request.get_json()
		# 'pickup'["pickup"]
		# destination	 = order["destination"]
		# weight  = order["weight"]
		# }}
		# if pickup.strip() == '' or destination == '' or weight == '':
		# 	return jsonify({"message":"fields con't be empty"})
		# else:
		# 	# Orders.update({"pickup": pickup, "destination":destination, "weight":weight})
		# 	Orders.update(parl)
		# return jsonify({"message":"success!"})
		
	# get all  parcel orders
	@mustlogin
	def get(self):
		return make_response(jsonify(
			{
			'Status': "Ok",
      'Message': "Success",
      'parcel': Orders
      }), 200)


class ParcelID(Resource):

	# show one parcel 
	@mustlogin
	def get(self, parcel_id):
		return make_response(jsonify(
			{
			'Status': "Ok",
      'Message': "Success",
      'parcel': (Orders[parcel_id])
      }), 200)

	# delete parcel
	@mustlogin
	def delete(self, parcel_id):
		del Orders[parcel_id]
		return jsonify({"message": "Succesfuly Deleted"})


	# Update parcel
	@mustlogin
	def put(self, parcel_id):
		upd = [dics for dics in Orders if (dics['parcel_id'] == parcel_id)]
		if 'pickup' in request.json:
			upd[0]['pickup'] = request.json['pickup']
		if 'destination' in request.json:
			upd[0]['destination'] = request.json['destination']
		if 'weight' in request.json:
			upd[0]['weight'] = request.json['weight']
		return jsonify({'dics':upd[0]})



