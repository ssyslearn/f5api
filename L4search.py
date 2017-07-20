from flask import request
from flask_restful import Resource
from info.L4info import L4info
import json, requests

class L4search(Resource):
	def __init__(self):
		self.username = L4info.get_id()
		self.password = L4info.get_pw()
		self.l4ip = L4info.get_l4ip()

	def get(self):
		try:
			url = 'https://' + self.l4ip + '/mgmt/tm/ltm/virtual'
			headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8'}
			r = requests.get(url, auth=(self.username, self.password), headers=headers, verify=False)
			json_data = r.json()
			data = []
			for item in json_data['items']:
				data.append(item['name'])
			status = r.status_code
			result = str(status) + ' ' + ' '.join(data)
			return result
		except:
			return 'cannot access L4'
