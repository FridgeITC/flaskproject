from flask import jsonify, request
from db import mysql
import math

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
            sql = "SELECT * FROM fridge INNER JOIN company ON fridge.companyId = company.id WHERE localId=%s"
            data = (_local)
            cursor = db.cursor()
            cursor.execute(sql, data)
            data = cursor.fetchall()
            
            json_response = []
            
            for f in data:
              json_response.append({
                'id': f[0],
                'localId': f[1],
                'companyId': f[2],
                'capacity': f[3],
                'rows': f[4],
                'company': f[6],
                'emptyLines': 0,
                'taggedLines': 0,
                'untaggedLines': 0,
                'thirdPartyProducts': 0
              })

            db.commit()

            #####

            sql = "SELECT fridgeId, emptyLines, taggedLines, untaggedLines, thirdPartyProducts, MAX(at) AS MaxDateTime FROM imageRecord GROUP BY fridgeId"
            cursor = db.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()

            #for f in json_response:
            #  print(f['id'])
            for f in json_response:
              for g in data:
                if f['id'] == g[0]:
                  f['emptyLines'] = g[1]
                  f['taggedLines'] = g[2]
                  f['untaggedLines'] = g[3]
                  f['thirdPartyProducts'] = g[4]

            #####
            
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
            sql = "INSERT INTO fridge(localId, companyId, capacity, numRows) VALUES (%s, %s, %s, %s)"
            print(sql)
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
            sql = "DELETE FROM fridge WHERE id=%s;"
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

            sql = "SELECT product.id, catalog.name, count(name), SUM(CASE WHEN product.labeled = '1' THEN 1 ELSE 0 END) AS labeled FROM product INNER JOIN catalog ON product.productId = catalog.id WHERE imageId=%s GROUP BY name"
            data = (response['imageRecord'])
            cursor = db.cursor()
            cursor.execute(sql, data)
            data = cursor.fetchall()
            db.commit()

            for f in data:
              response['products'].append({
                'id': f[0],
                'name': f[1],
                'count': f[2],
                'labeled': f[3],
                'unlabeled': f[2] - f[3]
              })

            resp = jsonify(response)
            resp.status_code = 200
            return resp
        except Exception as e:
          print(e)
        finally:
          cursor.close() 
          db.close()