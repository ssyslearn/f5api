#-*- coding: utf-8 -*-
from flask import request, jsonify
from flask_restful import Resource, reqparse, abort
import json, requests
from info.L4info import L4info
from curlset.command import command
from VirtualServerList import VirtualServerList
from VirtualServer import VirtualServer
from PoolList import PoolList
from Pool import Pool
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
        #return jsonify(self.map)
        return 'get'

    def post(self):
        # class variable test
        args = request.get_json(force=True)

        if args['method'] == 'show_vs':
            virtuals = VirtualServerList(args['l4ip'])
            return virtuals.get()
        elif args['method'] == 'create_lb':
            result = {}
            try:
                # ping...
                pass
            except:
                pass

            try:
                try:
                    pools = PoolList(args['l4ip'])
                    result['pool_result'] = pools.post(args['pool'])
                except:
                    result['pool_result'] = 'Fail to create Pool, 404'
                try:
                    virtuals = VirtualServerList(args['l4ip'])
                    result['virtual_result'] = virtuals.post(args['virtual'])
                except:
                    result['virtual_result'] = 'Fail to create Virtual Server, 404'
            except:
                return 'Fail to create L4, 404'
           
            flag = True
            for k in result.keys():
                if result[k].split(',')[-1].strip() != '200':
                    flag = False
                    break
            
            create_result = {}
            if flag:
                create_result['message'] = 'success in creating L4'
                create_result['status'] = '200'
                create_result['result'] = result
                return create_result
            else:
                create_result['message'] = 'fail to create l4'
                create_result['status'] = '404'
                create_result['result'] = result
                return create_result
        elif args['method'] == 'modify_lb':
            result = {}
            if args['target'] == 'enable':
                pass
            elif args['target'] == 'disable':
                pass
            elif args['target'] == 'lb_mode':
                pass
            elif args['target'] == 'change_pool':
                pass
            elif args['target'] == 'change_member':
                pass
            elif args['target'] == 'sticky':
                pass
            elif args['target'] == 'monitor':
                pass
            else:
                pass
            

        else:
            return 'Error create L4 !!!!'


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

