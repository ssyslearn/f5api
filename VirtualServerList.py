from flask import request, jsonify
from flask_restful import Resource, reqparse
from info.L4info import L4info
from curlset.command import command
import json, requests

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('destination')

class VirtualServerList(Resource):
	def __init__(self):
		self.username = L4info.get_id()
		self.password = L4info.get_pw()
		self.url = 'https://' + L4info.get_l4ip()
		self.headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8'}

	def get(self):
		try:
			r = requests.get(self.url+command.virtuals, auth=(self.username, self.password), headers=self.headers, verify=False)
			json_data = r.json()
			ret_data = {}
			ret_data['status'] = r.status_code
			ret_data['virtuals'] = json_data
			return jsonify(ret_data)
		except:
			return 'cannot get virtuals info from L4'

	def post(self):
		args = parser.parse_args()
		cmd = command.create_virtual_server
		cmd = json.loads(cmd.split("-d")[-1].split("'")[1])

		# Empty value of command should have arguments
		for k in cmd:
			if cmd[k] == "":
				try:
					cmd[k] = args[k]
				except:
					# if arguments is empty, raise error
					raise

		try:
			r = requests.post(self.url+command.virtuals, auth=(self.username, self.password), \
					 data = json.dumps(cmd), \
					 headers=self.headers, verify=False)
			return jsonify(r.text)
		except:
			return 'cannot create virtual server'
