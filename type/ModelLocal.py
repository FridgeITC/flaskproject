from flask import jsonify, request
from db import mysql

class ModelLocal():
    @classmethod
    def get_all(self):
        db = None
        cursor = None
        try:
          db = mysql.connect()
          if request.method == 'GET':
            sql = "SELECT * FROM local"
            cursor = db.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()

            json_response = []

            for f in data:
              json_response.append({
                'id': f[0],
                'name': f[1],
                'zoneId': f[2]
              })

            print(data)
            db.commit()
            resp = jsonify(json_response)
            resp.status_code = 200
            return resp
        except Exception as e:
          print(e)
        finally:
          cursor.close() 
          db.close()

    @classmethod
    def add(self, _json):
        db = None
        cursor = None
        try:
          db = mysql.connect()
          _json = request.json
          _name = _json['name']
          _zone = _json['zone']

          if _name and request.method == 'POST':
            sql = "INSERT INTO local(name, zoneId) VALUES(%s, %s)"
            data = (_name, _zone)
            cursor = db.cursor()
            cursor.execute(sql, data)
            db.commit()
            resp = jsonify({"status": 200, "message": "Local added succesfully"})
            resp.status_code = 200
            return resp
        except Exception as e:
          print(e)
        finally:
          cursor.close() 
          db.close()

    @classmethod
    def delete(self, _json):
        db = None
        cursor = None
        try:
          db = mysql.connect()
          _json = request.json
          _id = _json['id']

          if _id and request.method == 'POST':
            sql = "DELETE FROM local WHERE id=%s"
            data = (_id)
            cursor = db.cursor()
            cursor.execute(sql, data)
            db.commit()
            resp = jsonify({"status": 200, "message": "Local removed succesfully"})
            resp.status_code = 200
            return resp
        except Exception as e:
          print(e)
        finally:
          cursor.close() 
          db.close()