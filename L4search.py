from flask import request
from flask_restful import Resource
import json

class L4search(Resource):
	def __init__(self):
		pass

	def get(self):
		return 'L4search !'
