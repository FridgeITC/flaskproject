from .entities.User import User
from flask import jsonify, request
from db import mysql
from werkzeug.security import generate_password_hash

class ModelUser():
    @classmethod
    def add_user(self, _json):
        db = None
        cursor = None
        try:
          db = mysql.connect()
          _json = request.json
          _email = _json['email']
          _password = _json['password']
          _local = _json['local']

          if _email and _password and _local and request.method == 'POST':
            _hashed_password = generate_password_hash(_password)
            sql = "INSERT INTO user(email, password, localId) VALUES(%s, %s, %s)"
            data = (_email, _hashed_password, _local)
            cursor = db.cursor()
            cursor.execute(sql, data)
            db.commit()
            resp = jsonify({"status": 200, "message": "User added succesfully"})
            resp.status_code = 200
            return resp
        except Exception as e:
          print(e)
        finally:
          cursor.close() 
          db.close()