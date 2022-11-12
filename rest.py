import pymysql
from app import app
from db import mysql
from flask import jsonify, request
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import generate_password_hash, check_password_hash

class User(object):	
	def __init__(self, id, username):
		self.id = id
		self.username = username

	def __str__(self):
		return "User(id='%s')" % self.id

@app.route('/rest-auth')
@jwt_required()
def get_response():
	return jsonify('You are an authenticate person to see this message')

def authenticate(username, password):	
	if username and password:
		conn = None;
		cursor = None;
		try:
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT id, username, password FROM user WHERE username=%s", username)
			row = cursor.fetchone()
			
			if row:
				if check_password_hash(row['password'], password):
					return User(row['id'], row['username'])
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
			cursor.execute("SELECT id, username FROM user WHERE id=%s", payload['identity'])
			row = cursor.fetchone()
			
			if row:
				return (row['id'], row['username'])
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
	conn = None
	cursor = None
	try:
		_json = request.json
		_username = _json['username']
		_password = _json['password']

		if _username and _password and request.method == 'POST':

			_hashed_password = generate_password_hash(_password)
			sql = "INSERT INTO user(username, password) VALUES(%s, %s)"
			data = (_username, _hashed_password)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('User added successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
        
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

jwt = JWT(app, authenticate, identity)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False, threaded=True)