import serverless_wsgi
from flask import Flask, jsonify, make_response

from connector import connector
from sqlapi import sqlapi
from utils import api_response
from json import JSONEncoder

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

class JsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return JSONEncoder.default(self, obj)

app.json_encoder = JsonEncoder

def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)