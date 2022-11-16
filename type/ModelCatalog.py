from flask import jsonify, request
from db import mysql

class ModelCatalog():
    @classmethod
    def get_all(self):
        db = None
        cursor = None
        try:
          db = mysql.connect()
          if request.method == 'GET':
            sql = "SELECT * FROM catalog"
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
          _name = _json['name']
          _price = _json['price']

          if _name and _price and request.method == 'POST':
            sql = "INSERT INTO catalog(name, price) VALUES(%s, %s)"
            data = (_name, _price)
            cursor = db.cursor()
            cursor.execute(sql, data)
            db.commit()
            resp = jsonify({"status": 200, "message": "Product added succesfully"})
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
            sql = "DELETE FROM catalog WHERE id=%s"
            data = (_id)
            cursor = db.cursor()
            cursor.execute(sql, data)
            db.commit()
            resp = jsonify({"status": 200, "message": "Product removed succesfully"})
            resp.status_code = 200
            return resp
        except Exception as e:
          print(e)
        finally:
          cursor.close() 
          db.close()