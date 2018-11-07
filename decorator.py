from flask import Flask,jsonify,request, make_response
from flask_restful import Resource
import datetime
import jwt
from functools import wraps
def mustlogin(d):
	@wraps(d)
	def decorated(*args, **kwargs):
		if request.headers.get('	')=='':
			return make_response(("You need to first login "), 201)
		try:
			jwt.decode(request.headers.get('x-access-token'), "djrefuge")
		except:
			return jsonify({"message": 'please sigin '})
		return d(*args, **kwargs)
	return decorated 