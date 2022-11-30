from flask import jsonify, request
from db import mysql
from typing import List, Dict
from type.ModelLabels import ModelLabels


class ModelInferenceInsertion:
    def __init__(self, fridge_id, products: List[Dict]):
        self.id = fridge_id
        self.resource = 'someurl'  # TODO ADD HERE THE INSERTION URL OF THE OBJECT IN AWS S3
        self.ModelLabels = ModelLabels(products)

    def insert(self):
        try:
            db = mysql.connect()
            if self.id is not None and self.resource is not None:
                cursor = db.cursor()
                labeled, unlabeled = len(self.ModelLabels.labeled), len(self.ModelLabels.unlabeled)
                empties = self.ModelLabels.getEmpties()
                cursor.execute("INSERT INTO nds.imageRecord(fridgeId, resource, at, emptyLines, untaggedLines, taggedLines, thirdPartyProducts) VALUES (%s, %s, DEFAULT, %s, %s, %s, %s);",
                               (self.id, self.resource, empties, unlabeled, labeled, 0)) # TODO DETECT THE COMPANIES THAT DOESNT BELONG
                image_id = cursor.lastrowid
                product_query, attr = self.prepare_product_insertion(image_id=image_id)
                cursor.execute(product_query, tuple(attr))
                db.commit()
        except Exception as e:
            print(e)
            # TODO: RETURN BAD REQUEST HTTP STATUS
        finally:
            cursor.close()
            db.close()

    def prepare_floats(self, val):
        return float('{:4.5f}'.format(val))

    def prepare_product_insertion(self, image_id):
        products_inference = [
            [product['class'], self.prepare_floats(product['xmax']), self.prepare_floats(product['ymax']),
             self.prepare_floats(product['xmin']), self.prepare_floats(product['ymin']), \
             self.prepare_floats(product['confidence']), image_id, product['labeled']]
            for product in self.ModelLabels.products]

        flatten = sum(products_inference, [])  # Flatten the 2d list of products into 1d
        # --- Making the query to match dynamically the products
        product_query = '(%s, %s, %s, %s, %s, %s, %s, %s), '
        products_val_list = product_query * len(products_inference)
        products_val_list = products_val_list[:-2] + ';'  # Removing the last comma with ;
        return """INSERT INTO nds.product (productId, xmax, ymax, xmin, ymin, confidence, imageId, labeled) VALUES {products}""" \
                   .format(products=products_val_list), flatten
