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
            sql = "SELECT fridge.id, company.name, fridge.localId, fridge.capacity, fridge.numRows FROM fridge INNER JOIN company ON fridge.companyId = company.id"
            cursor = db.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()
            
            json_response = []

            for f in data:
              json_response.append({
                'id': f[0],
                'company': f[1],
                'localId': f[2],
                'capacity': f[3],
                'rows': f[4]
              })

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

    @classmethod
    def get_by_id(self, _json):
        db = None
        cursor = None
        try:
          db = mysql.connect()
          _json = request.json
          _id = _json['id']

          if _id and request.method == 'POST':
            sql = "SELECT fridge.id, fridge.localId, fridge.capacity, fridge.numRows, imageRecord.id, imageRecord.resource, imageRecord.at FROM fridge INNER JOIN imageRecord ON fridge.id = imageRecord.fridgeId WHERE fridge.id=%s ORDER BY at DESC LIMIT 1"
            data = (_id)
            cursor = db.cursor()
            cursor.execute(sql, data)
            data = cursor.fetchone()
            db.commit()

            response = {
              'id': data[0],
              'local': data[1],
              'capacity': data[2],
              'rows': data[3],
              'imageId': data[4],
              'resource': data[5],
              'at': data[6],
              'products': []
            }

            sql = "SELECT product.id, catalog.name, product.xmax, product.ymax, product.ymin, product.xmin, product.confidence FROM product INNER JOIN catalog ON product.productId = catalog.id WHERE imageId=%s"
            data = (response['imageId'])
            cursor = db.cursor()
            cursor.execute(sql, data)
            data = cursor.fetchall()
            db.commit()

            for f in data:
              response['products'].append({
                'id': f[0],
                'name': f[1],
                'xmax': f[2],
                'ymax': f[3],
                'ymin': f[4],
                'xmin': f[5],
                'confidence': f[6]
              })

            resp = jsonify(response)
            resp.status_code = 200
            return resp
        except Exception as e:
          print(e)
        finally:
          cursor.close() 
          db.close()