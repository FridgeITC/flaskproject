from flask import jsonify, request
from db import mysql

class ModelFridge():
    @classmethod
    def get_all(self):
        db = None
        cursor = None
        try:
          db = mysql.connect()
          if request.method == 'GET':
            sql = "SELECT * FROM fridge"
            cursor = db.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()
            print(data)
            db.commit()
            resp = jsonify(data)
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
          _local = _json['local']
          _capacity = _json['capacity']
          _rows = _json['rows']

          if _local and _capacity and _rows and request.method == 'POST':
            sql = "INSERT INTO fridge(localId, capacity, rows) VALUES(%s, %s, %s)"
            data = (_local, _capacity, _rows)
            cursor = db.cursor()
            cursor.execute(sql, data)
            db.commit()
            resp = jsonify({"status": 200, "message": "Fridge added succesfully"})
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
            sql = "DELETE FROM fridge WHERE id=%s"
            data = (_id)
            cursor = db.cursor()
            cursor.execute(sql, data)
            db.commit()
            resp = jsonify({"status": 200, "message": "Fridge removed succesfully"})
            resp.status_code = 200
            return resp
        except Exception as e:
          print(e)
        finally:
          cursor.close() 
          db.close()