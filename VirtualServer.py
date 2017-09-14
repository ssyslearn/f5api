from flask import request, jsonify
from flask_restful import Resource, reqparse, abort
from info.L4info import L4info
from curlset.command import command
import json, requests

class VirtualServer(Resource):
    def __init__(self):
        self.username = L4info.get_id()
        self.password = L4info.get_pw()
        self.url = 'https://' + L4info.get_l4ip()
        self.payload = {'expandSubcollections':'true'}
        self.headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8'}

    def get(self, virtual_server_name):
        try:
            r = requests.get(self.url+command.virtuals+'/'+virtual_server_name, auth=(self.username, self.password), headers=self.headers, params=self.payload, verify=False)
            json_data = r.json()
            ret_data = {}
            ret_data['status'] = r.status_code
            ret_data['virtual_server'] = json_data
            return jsonify(ret_data)
        except:
            return 'cannot get virtual server info from L4'

    def post(self, virtual_server_name):
        #cmd = command.virtuals + '/' + virtual_server_name + command.enable_virtual_server
        #uri = cmd.split("-d")[0].strip()
        #cmd = json.loads(cmd.split("-d")[-1].split("'")[1])
        #default_key_list = [ k for k in cmd ]

        #for k in args['data']:
        #    cmd[k] = args['data'][k]
        #    try:
        #        cmd[k] = args['data'][k]
        #    except:
        #        raise InvalidApiCall
        #for k in default_key_list:
        #    if cmd[k] == "":
        #        return 'You must request ...'

        args = request.get_json(force=True)
        #return args['data']['pool']

        if args['method'] == 'enable':
            cmd = command.virtuals + '/' + virtual_server_name + command.enable_virtual_server
            uri = cmd.split("-d")[0].strip()
            cmd = json.loads(cmd.split("-d")[-1].split("'")[1])
            cmd['enabled'] = True
        elif args['method'] == 'disable':
            cmd = command.virtuals + '/' + virtual_server_name + command.disable_virtual_server
            uri = cmd.split("-d")[0].strip()
            cmd = json.loads(cmd.split("-d")[-1].split("'")[1])
            cmd['disabled'] = True
        elif args['method'] == 'edit_pool':
            cmd = command.virtuals + '/' + virtual_server_name + command.editpool_virtual_server
            uri = cmd.split("-d")[0].strip()
            cmd = json.loads(cmd.split("-d")[-1].split("'")[1])
            default_key_list = [ k for k in cmd ]
            #try:

            for k in args['data']:
                cmd[k] = args['data'][k]
                try:
                    cmd[k] = args['data'][k]
                except:
                    raise InvalidApiCall
            for k in default_key_list:
                if cmd[k] == "":
                    return 'You must request ...'
            #except:
            #    return 'please input data field'

        try:
            r = requests.patch(self.url+uri, auth=(self.username, self.password), \
                    data = json.dumps(cmd), \
                    headers=self.headers, verify=False)
            json_data = r.json()
            ret_data = {}
            ret_data['status'] = r.status_code
            ret_data['virtual_server'] = json_data
            return jsonify(ret_data) 
        except:
            return 'cannot handle patch api'
    
