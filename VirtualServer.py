from flask import request, jsonify
from flask_restful import Resource
from info.L4info import L4info
from curlset.command import command
import json, requests

class VirtualServer(Resource):
	def __init__(self):
		self.username = L4info.get_id()
		self.password = L4info.get_pw()
		self.url = 'https://' + L4info.get_l4ip()
		self.headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8'}

	def get(self, virtual_server_name):
		try:
			r = requests.get(self.url+command.virtuals+'/'+virtual_server_name, auth=(self.username, self.password), headers=self.headers, verify=False)
			json_data = r.json()
			ret_data = {}
			ret_data['status'] = r.status_code
			ret_data['virtual_server'] = json_data
			return jsonify(ret_data)
		except:
			return 'cannot get virtual server info from L4'

