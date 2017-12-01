#-*- coding: utf-8 -*-
from flask import request, jsonify
from flask_restful import Resource, reqparse, abort
import json, requests
from info.L4info import L4info
from curlset.command import command
import MySQLdb
import _mysql_exceptions
import sys
from contextlib import contextmanager

class InvalidApiCall(Exception):
    """ 잘못된 API 요청 """
    def __init__(self):
        abort(404, message="invalid api call")

class Valid:
    @staticmethod
    def valid_args(args, cmd):
        default_key_list = [ k for k in cmd ]
        for k in args:
            cmd[k] = args[k]
            try:
                cmd[k] = args[k]
            except:
                # if arguments don't have a key , raise error
                raise InvalidApiCall

        # Empty value of command should get arguments from request
        for k in default_key_list:
            if cmd[k] == "":
                return None
        return 'OK'

class VirtualServer(Resource):
    def __init__(self, l4ip):
        self.username = L4info.get_id()
        self.password = L4info.get_pw()
        self.url = 'https://' + l4ip
        self.payload = {'expandSubcollections':'true'}
        self.headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8'}
        self.db_id= L4info.get_db_id()
        self.db_pw= L4info.get_db_pw()
        self.db_ip= L4info.get_db_ip()

    @contextmanager
    def db_connect(self):
        conn = MySQLdb.connect(host=self.db_ip, user=self.db_id, passwd=self.db_pw, db='TEST')
        cur = conn.cursor()

        try:
            yield (conn, cur)
        finally:
            cur.close()
            conn.close()

    def apicall_with_insertdb(self, uri, cmd, method):
        try:
            r = requests.patch(self.url+uri, auth=(self.username, self.password), \
                        data = json.dumps(cmd), \
                        headers=self.headers, verify=False)

                #
                # have to implement error handling of requests.post
                # if apiError in json.loads(r.text).keys(), then error handling
                #

            with self.db_connect() as (conn, cur):
                s = """ INSERT INTO API (method, api_uri, api_data, username, date) VALUES ('%s', '%s', '%s', '%s', now() ) """ % (method, uri, json.dumps(cmd), request.remote_user)
                cur.execute(s)
                conn.commit()
            return jsonify(r.text)
        except:
            return 'cannot change virtual server'

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
        args = request.get_json(force=True)

        if args['method'] == 'enable':
            uri = command.virtuals + '/' + virtual_server_name
            cmd = {"enabled": True}
            return self.apicall_with_insertdb(uri, cmd, 'PATCH')
        elif args['method'] == 'disable':
            uri = command.virtuals + '/' + virtual_server_name
            cmd = {"disabled": True}
            return self.apicall_with_insertdb(uri, cmd, 'PATCH')
        elif args['method'] == 'change_pool':
            cmd = command.virtuals + '/' + virtual_server_name + command.change_pool
            uri = cmd.split("-d")[0].strip()
            cmd = json.loads(cmd.split("-d")[-1].split("'")[1])
            
            if Valid.valid_args(args['data'], cmd):
                return self.apicall_with_insertdb(uri, cmd, 'PATCH')
            else:
                return 'You must request with pool name'
        else:
            return 'please correct method'
    
