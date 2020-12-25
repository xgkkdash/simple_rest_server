import os
import socket
import redis
from flask import Flask
from flask_restful import Resource, Api, reqparse, abort

from database.db import init_db
from model.kvpair import KvPair


# create a flask app with default redis/db configuration
def init_app():
    # create flask app
    flask_app = Flask(__name__)
    api = Api(flask_app)

    # redis cache
    REDIS_HOST = os.environ.get('REDIS_HOST', '127.0.0.1')
    cache = redis.Redis(host=REDIS_HOST, port=6379)

    # TODO: set db_name const here, later change it to docker_file
    db_name = "test_rest_server"
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    db_url = "mongodb://" + DB_HOST + ":27017/"

    # init db
    with flask_app.app_context():
        db = init_db(db_name, db_url)

    # define parser for POST/PUT
    parser = reqparse.RequestParser()
    parser.add_argument('key')
    parser.add_argument('value')

    # match CRUD operations with get/post/put/delete request, according to standard rules:
    # post -- create, get -- read, put -- update, delete -- delete

    class GetDelHandler(Resource):
        def get(self, key):
            # if element exists in DB, return it with 200, else return 404 Not Found
            # first looking for element from cache, if not success, goto DB
            cache_result = cache.get(key)
            if cache_result:  # can find from cache, do not need DB operation
                result_v = cache_result.decode("utf-8")  # redis use bytes to save, use decode to convert it to string
                return {'key': key, 'value': result_v}, 200
            else:  # cache didn't save this data, search from DB
                result = db.get_kvpair(key=key)
                if result:
                    result_k, result_v = result.key, result.value
                    cache.set(result_k, result_v)  # found from DB, add to cache first before return
                    return {'key': result_k, 'value': result_v}, 200
                else:
                    return abort(404, message="element with Key {} doesn't exist".format(key))
                # return 'Key Not Exist', 404

        def delete(self, key):
            # update both cache and db
            cache.delete(key)
            db.remove_kvpair(key=key)
            return "Delete Done", 200

    class PostPutHandler(Resource):
        # first check if args are valid, else return 400 Bad Request
        def put(self):
            key, value = self._params_from_request()
            if not key or not value:
                return abort(400, message="PUT request must contains both key and value")

            if self._key_exist(key):
                # can do DB update, return 200 after db update done
                # update both cache and db
                cache.set(key, value)
                db.update_kvpair(key, value)
                return "Update {} Success".format((key, value)), 200
            else:
                return abort(400, message="primary key does not exist, cannot update")

        def post(self):
            key, value = self._params_from_request()
            if not key or not value:
                return abort(400, message="POST request must contains both key and value")

            if self._key_exist(key):
                return abort(400, message="primary key already exist, cannot insert")
            else:
                # can do DB insert, return 201 created after db insert done
                # update both cache and db
                cache.set(key, value)
                kvpair = KvPair(key, value)
                db.save_kvpair(kvpair)
                return "Insert {} Success".format((key, value)), 201

        def _params_from_request(self):
            args = parser.parse_args()
            key = args['key']
            value = args['value']
            return key, value

        def _key_exist(self, key):
            # search both cache and DB
            if cache.get(key) or db.get_kvpair(key=key):
                return True
            else:
                return False

    # add handler to api
    api.add_resource(PostPutHandler, '/')
    api.add_resource(GetDelHandler, '/<string:key>')
    return flask_app


# give a default app by init_app
app = init_app()


if __name__ == '__main__':
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    print("Hostname :  ", host_name)
    print("IP : ", host_ip)
    serverPort = int(os.environ.get('PORT', 5000))

    app.run(host='0.0.0.0', port=serverPort, debug=True)
