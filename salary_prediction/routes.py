from salary_prediction import salary_prediction_app
import socket
import json
from flask import Flask, jsonify, request

ip_address = socket.gethostbyname(socket.gethostname())
ip_address

@salary_prediction_app.route('/')
@salary_prediction_app.route('/index')
def index():
    return ("<H1>Hello, World!</H1> <H2>API IP Address: {} </H2>".format(ip_address))
