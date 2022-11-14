import pymysql
from flask import jsonify, request
from flask_jwt import JWT, jwt_required
from werkzeug.security import check_password_hash

# Models:
from models.ModelUser import ModelUser
# Entities:
from models.entities.User import User
from app import app
from db import mysql
@app.route('/rest-auth')
@jwt_required()
def get_response():
    return jsonify('You are an authenticate person to see this message')


def authenticate(email, password):
    if email and password:
        conn = None;
        cursor = None;
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT id, email, password FROM user WHERE email=%s", email)
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


jwt = JWT(app, authenticate, identity)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False, threaded=True)
