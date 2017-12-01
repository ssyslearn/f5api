#-*- coding: utf-8 -*-
from flask import request, jsonify, render_template, make_response
from flask_restful import Resource, reqparse, abort
import json, requests
from info.L4info import L4info
from curlset.command import command
import sys

class Index(Resource):
    def __init__(self):
        pass

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('form-layouts-one-column.html'), 200, headers)

