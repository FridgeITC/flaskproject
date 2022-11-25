from flask import jsonify, request
from db import mysql

class ModelZone():
    @classmethod
    def get_all(self):
        db = None
        cursor = None
        try:
          db = mysql.connect()
          if request.method == 'GET':
            sql = "SELECT * FROM zone"
            cursor = db.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()

            json_response = []

            for f in data:
              json_response.append({
                'id': f[0],
                'name': f[1]
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

          if _name and request.method == 'POST':
            sql = "INSERT INTO zone(name) VALUES(%s)"
            data = (_name)
            cursor = db.cursor()
            cursor.execute(sql, data)
            db.commit()
            resp = jsonify({"status": 200, "message": "Zone added succesfully"})
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
            sql = "DELETE FROM zone WHERE id=%s"
            data = (_id)
            cursor = db.cursor()
            cursor.execute(sql, data)
            db.commit()
            resp = jsonify({"status": 200, "message": "Zone removed succesfully"})
            resp.status_code = 200
            return resp
        except Exception as e:
          print(e)
        finally:
          cursor.close() 
          db.close()