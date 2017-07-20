from flask import request
from flask_restful import Resource
from info.L4info import L4info
from curlset.command import command
import json, requests

class Pools(Resource):
	def __init__(self):
		self.username = L4info.get_id()
		self.password = L4info.get_pw()
		self.url = 'https://' + L4info.get_l4ip()
		self.headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8'}

	def get(self):
		try:
			r = requests.get(self.url+command.pools, auth=(self.username, self.password), headers=self.headers, verify=False)
			json_data = r.json()
			data = []
			for item in json_data['items']:
				data.append(item['name'])
			status = r.status_code
			result = str(status) + ' ' + ' '.join(data)
			return result
		except:
			return 'cannot get pools info from L4'

