from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
import os
import socket

# create flask app
app = Flask(__name__)
api = Api(app)

# define parser for POST
parser = reqparse.RequestParser()
parser.add_argument('key')
parser.add_argument('value')

# dict for record key-value pair
kv_pair = {}


class GetHandler(Resource):
    def get(self, key):
        # return value if key is in kv_pair, else return 404 Not Found
        if key in kv_pair:
            return kv_pair[key], 200
        else:
            return abort(404, message="Key {} doesn't exist".format(key))
            # return 'Key Not Exist', 404


class PostHandler(Resource):
    def post(self):
        # add kv-pair to dict to args are valid, else return 400 Bad Request
        args = parser.parse_args()
        key = args['key']
        value = args['value']
        if not key or not value:
            return abort(400, message="POST request must contains both key and value")
        kv_pair[key] = value
        return {key: value}, 200


# add handler to api
api.add_resource(PostHandler, '/')
api.add_resource(GetHandler, '/<string:key>')

if __name__ == '__main__':
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    print("Hostname :  ", host_name)
    print("IP : ", host_ip)
    serverPort = int(os.environ.get('PORT', 5000))

    app.run(host='0.0.0.0', port=serverPort, debug=True)
