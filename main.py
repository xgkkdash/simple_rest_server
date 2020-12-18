from flask import Flask
from flask_restful import Resource, Api
import os
import socket

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    print("Hostname :  ", host_name)
    print("IP : ", host_ip)
    # hostName = host_name or "localhost"
    serverPort = int(os.environ.get('PORT', 5000))

    app.run(host='0.0.0.0', port=serverPort, debug=True)
