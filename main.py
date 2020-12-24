from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
import os
import socket

from database.db import init_db
from model.kvpair import KvPair

# create flask app
app = Flask(__name__)
api = Api(app)

# TODO: set db_name and url here, later change it to docker_file
db_name = "test_rest_server"
db_url = "mongodb://localhost:27017/"

# init db
with app.app_context():
    db = init_db(db_name, db_url)

# define parser for POST/PUT
parser = reqparse.RequestParser()
parser.add_argument('key')
parser.add_argument('value')

# match CRUD operations with get/post/put/delete request, rules:
# get -- read, put -- create, post -- update, delete -- delete


class GetDelHandler(Resource):
    def get(self, key):
        # if element exists in DB, return it with 200, else return 404 Not Found
        result = db.get_kvpair(key=key)
        if result:
            result_k, result_v = result.key, result.value
            return {'key': result_k, 'value': result_v}, 200
        else:
            return abort(404, message="element with Key {} doesn't exist".format(key))
            # return 'Key Not Exist', 404

    def delete(self, key):
        db.remove_kvpair(key=key)
        return "Delete Done", 200


class PostPutHandler(Resource):
    # first check if args are valid, else return 400 Bad Request
    def post(self):
        key, value = self._params_from_request()
        if not key or not value:
            return abort(400, message="POST request must contains both key and value")

        if self._key_exist(key):
            # can do DB update, return 200 after db update done
            db.update_kvpair(key, value)
            return "Update {} Success".format((key, value)), 200
        else:
            return abort(400, message="primary key does not exist, cannot update")

    def put(self):
        key, value = self._params_from_request()
        if not key or not value:
            return abort(400, message="PUT request must contains both key and value")

        if self._key_exist(key):
            return abort(400, message="primary key already exist, cannot insert")
        else:
            # can do DB insert, return 201 created after db insert done
            kvpair = KvPair(key, value)
            db.save_kvpair(kvpair)
            return "Insert {} Success".format((key, value)), 201

    def _params_from_request(self):
        args = parser.parse_args()
        key = args['key']
        value = args['value']
        return key, value

    def _key_exist(self, key):
        result = db.get_kvpair(key=key)
        return True if result else False


# add handler to api
api.add_resource(PostPutHandler, '/')
api.add_resource(GetDelHandler, '/<string:key>')

if __name__ == '__main__':
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    print("Hostname :  ", host_name)
    print("IP : ", host_ip)
    serverPort = int(os.environ.get('PORT', 5000))

    app.run(host='0.0.0.0', port=serverPort, debug=True)
