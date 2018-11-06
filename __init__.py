from flask import Flask, jsonify, request, Blueprint
from flask_restful import Api
import json
from models import *

from app.order  import Home
from auth.users import Register


api_bp = Blueprint('api', __name__)
api = Api(api_bp)


api.add_resource(Home, '/')
api.add_resource(Register, '/v1/auth/signup')

