from flask import request
from flask_restful import Resource
import json

class Hello(Resource):
	def __init__(self):
		pass

	def get(self):
		return 'Hello world!'
