from flask import Flask, jsonify, request, Blueprint
from flask_restful import Api
import json
from models import *

from app.order  import Home

api_bp = Blueprint('api', __name__)
api = Api(api_bp)


api.add_resource(Home, '/')
