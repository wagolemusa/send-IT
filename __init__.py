from flask import Flask, jsonify, request, Blueprint
from flask_restful import Api
import json
from models import *

from app.order  import Home

v1 = Blueprint('api', __name__)
api = Api(v1)


api.add_resource(Home, '/')
