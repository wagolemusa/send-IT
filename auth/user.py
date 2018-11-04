from flask_restful import Resource

class Register(Resource):
	def get(self):
		return {"message": "Whats up Refuge wise"}