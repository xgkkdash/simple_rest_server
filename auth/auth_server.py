from flask import Flask
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
   "root": "root"
}


@auth.verify_password
def verify_password(username, password):
    if username in users and password == users.get(username):
        return username


@app.route('/')
@auth.login_required
def index():
    return "Hello, {}!".format(auth.current_user())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

