from flask import jsonify, request
from db import mysql

class ModelFridge():
    @classmethod
    def get_all(self, _json):
        db = None
        cursor = None
        try:
          db = mysql.connect()
          _json = request.json
          _local = _json['local']
          if _local and request.method == 'POST':
            sql = "SELECT fridge.id, company.name, imageRecord.emptyLines, imageRecord.taggedLines, imageRecord.untaggedLines, imageRecord.thirdPartyProducts, imageRecord.at FROM imageRecord INNER JOIN (SELECT fridgeId, MAX(at) AS MaxDateTime FROM imageRecord GROUP BY fridgeId) groupedtt  ON imageRecord.fridgeId = groupedtt.fridgeId AND imageRecord.at = groupedtt.MaxDateTime INNER JOIN fridge ON imageRecord.fridgeId = fridge.id INNER JOIN company ON fridge.companyId = company.id WHERE fridge.localId=%s"
            data = (_local)
            cursor = db.cursor()
            cursor.execute(sql, data)
            data = cursor.fetchall()
            
            json_response = []

            for f in data:
              json_response.append({
                'id': f[0],
                'name': f[1],
                'emptyLines': f[2],
                'taggedLines': f[3],
                'untaggedLines': f[4],
                'thirdPartyProducts': f[5],
                'at': f[6]
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
          _company = _json['company']
          _capacity = _json['capacity']
          _rows = _json['rows']

          if _local and _company and _capacity and _rows and request.method == 'POST':
            sql = "INSERT INTO fridge(localId, companyId, capacity, rows) VALUES(%s, %s, %s, %s)"
            data = (_local, _company, _capacity, _rows)
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
    def get(self, _json):
        db = None
        cursor = None
        try:
          db = mysql.connect()
          _json = request.json
          _id = _json['id']

          if _id and request.method == 'POST':
            sql = "SELECT fridge.id, fridge.localId, fridge.capacity, fridge.numRows, imageRecord.id, imageRecord.resource, imageRecord.emptyLines, imageRecord.taggedLines, imageRecord.untaggedLines, imageRecord.thirdPartyProducts, imageRecord.at FROM fridge INNER JOIN imageRecord ON fridge.id = imageRecord.fridgeId WHERE fridge.id=%s ORDER BY at DESC LIMIT 1"
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
              'imageRecord': data[4],
              'resource': data[5],
              'emptyLines': data[6],
              'taggedLines': data[7],
              'untaggedLines': data[8],
              'thirdPartyProducts': data[9],
              'at': data[10],
              'products': []
            }

            sql = "SELECT product.id, catalog.name, product.xmax, product.ymax, product.ymin, product.xmin, product.confidence FROM product INNER JOIN catalog ON product.productId = catalog.id WHERE imageId=%s"
            data = (response['imageRecord'])
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