import jwt
from datetime import datetime, timedelta
from flask import Flask, jsonify, request

app = Flask(__name__)

# set secret key for generate token
app.config['SECRET_KEY'] = 'xgtest'

users = {"root": "root"}

# user login and get a token
@app.route('/login', methods=['POST'])
def login():
    if not request.authorization:
        return jsonify({"message": "Post request must have auth"}), 401

    username = request.authorization.get('username', None)
    password = request.authorization.get('password', None)
    if not username:
        return jsonify({"message": "Missing username"}), 400
    if not password:
        return jsonify({"message": "Missing password"}), 400

    if username not in users or password != users.get(username, None):
        return jsonify({"message": "Wrong username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = generate_token_by_user_id(username)
    return access_token, 200


def generate_token_by_user_id(user_id):
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=5),
            'iat': datetime.utcnow(),
            'user': user_id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e

# user use token to access
@app.route('/protected', methods=['GET'])
def access_by_token():
    token = request.headers.get('Authorization', None)
    if not token:
        return jsonify({"message": "token required"}), 401
    current_user = decode_token_to_user(token)
    if current_user and current_user in users:
        return "Welcome {}".format(current_user), 200
    else:
        return jsonify({"message": "Invalid token"}), 401


def decode_token_to_user(token):
    result = jwt.decode(token, app.config.get('SECRET_KEY'), algorithms="HS256")
    return result['user'] if result else None


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True, ssl_context='adhoc')
    app.run(host='0.0.0.0', port=5000, debug=True)
