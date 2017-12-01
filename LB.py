#-*- coding: utf-8 -*-
from flask import request, jsonify
from flask_restful import Resource, reqparse, abort
import json, requests
from info.L4info import L4info
from curlset.command import command
import sys

class LB(Resource):
    def get_virtual_pool_map(self):
        try:
            r = requests.get(self.url+command.virtuals, auth=(self.username, self.password), headers=self.headers, params=self.payload, verify=False)
            json_data = r.json()
            ret_data = {}
            for x in json_data['items']:
                ret_data[x['name']] = {}
                if 'pool' in x:
                    ret_data[x['name']]['pool'] = x['pool']
                    ret_data[x['name']]['vip'] = x['destination'].split('/')[-1]
                else:
                    ret_data[x['name']]['pool'] = ''
                    ret_data[x['name']]['vip'] = x['destination'].split('/')[-1]

            #ret_data['pool'] = [ x['name'] for x in json_data['items'] ]
            self.map['data'] = ret_data
            #return jsonify(ret_data)
        except:
            return 'cannot get virtual server info from L4'

    def get(self):
        return jsonify(self.map)

    def post(self):
		# class variable test
		args = request.get_json(force=True)

		if args['method'] == 'set_ip':
			L4info.set_l4ip(args['data'])

		return L4info.get_l4ip()

        # create virtual-pool map
        #return 'please correct method'

    def __init__(self):
        self.username = L4info.get_id()
        self.password = L4info.get_pw()
        self.url = 'https://' + L4info.get_l4ip()
        self.payload = {'expandSubcollections':'true'}
        self.headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8'}
        #self.map = {}

        #self.get_virtual_pool_map()

        # create virtual-pool map
