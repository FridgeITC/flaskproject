import pymysql
from app import app
from db import mysql
from flask import jsonify, request
from flask_jwt import JWT
from werkzeug.security import check_password_hash
from flasgger.utils import swag_from

from routes.fridge import fridge
# Models:
from type.ModelUser import ModelUser
# Entities:
from type.entities.User import User
import argparse
@app.route('/rest-auth')

def get_response():
    return jsonify('You are an authenticate person to see this message')

from type.entities.User import User

def authenticate(username, password):
	if username and password:
		conn = None;
		cursor = None
		try:
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT id, email, password FROM user WHERE email=%s", username)
			row = cursor.fetchone()
			
			if row:
				if check_password_hash(row['password'], password):
					return User(row['id'], row['email'])
			else:
				return None
		except Exception as e:
			print(e)
		finally:
			cursor.close() 
			conn.close()
	return None


def identity(payload):
    if payload['identity']:
        conn = None;
        cursor = None;
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT id, email FROM user WHERE id=%s", payload['identity'])
            row = cursor.fetchone()

            if row:
                return (row['id'], row['email'])
            else:
                return None
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
    else:
        return None


@app.route('/add-user', methods=['POST'])
def add_user():
    db = mysql.connect()
    _json = request.json
    return ModelUser.add_user(db, _json)

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.route("/login", methods=["POST"])
def login():
    """
    User authenticate method.
    ---
    description: Authenticate user with supplied credentials.
    tags:
    - Auth
    parameters:
    - in: 'body'
      name: 'body'
      description: 'Accepts username and password'
      required: true,
      schema:
        type: 'object'
        properties:
          username:
            type: string
            example: 'alejandro@hernandez.dev'
          password:
            type: string
            example: 'B230916'
    responses:
      200:
        description: User successfully logged in.
      400:
        description: User login failed.
    """
    try:
        _json = request.json
        username = _json['username']
        password = _json['password']
        print(username, password)
        user = authenticate(username, password)
        if not user:
            raise Exception("User not found!")

        access_token = jwt.jwt_encode_callback(user)
        resp = jsonify({"message": "User authenticated", 'jwt-token': "JWT "+access_token.decode()})
        resp.status_code = 200

    except Exception as e:
        print(e)
        resp = jsonify({"message": "Bad username and/or password"})
        resp.status_code = 401

    return resp

jwt = JWT(app, authenticate, identity)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask api exposing yolov5 model")
    parser.add_argument("--port", default=8080, type=int, help="port number")
    args = parser.parse_args()
    app.run(host='0.0.0.0', port=args.port, debug=False, use_reloader=False)
