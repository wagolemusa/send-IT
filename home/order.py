from flask import Flask,jsonify,request, make_response
from flask_restful import Resource

import datetime
import jwt
Orders ={}

class Home(Resource):
    def get(self):
        return {"message": "SendIT is one of popular courier services"}


class Parcels(Resource):
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

	def get(self):
		par = Orders
		return make_response(jsonify(
			{
			'Status': "Ok",
      'Message': "Success",
      'reg': Orders
      }), 200)

	




