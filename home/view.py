from flask_restful import Resource


class Home(Resource):
    def get(self):
        return {"message": "SendIT is one of popular courier services"}