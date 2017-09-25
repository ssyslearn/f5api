from flask import request, jsonify
from flask_restful import Resource
from info.L4info import L4info
from curlset.command import command
import json, requests

class Monitor(Resource):
    def __init__(self):
        self.username = L4info.get_id()
        self.password = L4info.get_pw()
        self.url = 'https://' + L4info.get_l4ip()
        self.payload = {'expandSubcollections':'true'}
        self.headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8'}

    def get(self):
        try:
            r = requests.get(self.url+command.monitor, auth=(self.username, self.password), headers=self.headers, params=self.payload, verify=False)
            json_data = r.json()
            ret_data = {}
            ret_data['status'] = r.status_code
            ret_data['pool'] = json_data
            return jsonify(ret_data)
        except:
            return 'cannot get pool info from L4'

#    def post(self):
#        try:
#            r = requests.post(self.url+command.monitor+'/'+pool_name, auth=(self.username, self.password), headers=self.headers, params=self.payload, verify=False)
#            json_data = r.json()
#            ret_data = {}
#            ret_data['status'] = r.status_code
#            ret_data['pool'] = json_data
#            return jsonify(ret_data)
#        except:
#            return 'cannot get pool info from L4'
