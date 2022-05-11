from flask import Flask, jsonify, make_response

from connector import connector
from sqlapi import sqlapi
from utils import api_response

app = Flask(__name__)
app.register_blueprint(connector)
app.register_blueprint(sqlapi)

@app.route("/")
@api_response
def default():
    return 'Nothing to see here'


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)

