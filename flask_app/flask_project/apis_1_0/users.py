from flask_restful import Resource
from flask_restful.reqparse import RequestParser

register_parser = RequestParser()

login_parser = register_parser.copy()


class RegisterUsersResource(Resource):
	
	def post(self):
		pass 