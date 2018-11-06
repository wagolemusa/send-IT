from flask import Flask, jsonify, request, Blueprint
from flask_restful import Api
import json
from models import *

from app.order  import Home
from auth.users import Register


v1 = Blueprint('api', __name__)
api = Api(v1)


api.add_resource(Home, '/')
api.add_resource(Register, '/v1/auth/signup')

