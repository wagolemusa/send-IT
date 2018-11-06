from flask import Flask,jsonify,request, make_response
from flask_restful import Resource

import datetime
import jwt
from functools import wraps
from __init__ import *


class Home(Resource):
	def get(self):
		return {"message": "SendIT is one of popular courier services"}
