from flask import jsonify, request
from db import mysql
from typing import List, Dict


class ModelInferenceInsertion:
    def __init__(self, fridge_id, products: List[Dict]):
        self.id = fridge_id
        self.resource = 'someurl' # TODO ADD HERE THE INSERTION URL OF THE OBJECT
        self.products = products

    def insert(self):
        try:
            db = mysql.connect()
            if self.id is not None and self.resource is not None:
                cursor = db.cursor()
                cursor.execute("INSERT INTO nds.imageRecord(fridgeId, resource, at) VALUES (%s, %s, DEFAULT);",
                               (self.id, self.resource))
                image_id = cursor.lastrowid
                product_query, attr = self.prepare_product_insertion(image_id=image_id)
                cursor.execute(product_query, tuple(attr))
                db.commit()
        except Exception as e:
            print( e)
            # TODO: RETURN BAD REQUEST HTTP STATUS
        finally:
            cursor.close()
            db.close()
    def prepare_floats(self, val):
        return float('{:4.5f}'.format(val))
    def prepare_product_insertion(self, image_id):
        products_inference = [[product['class'], self.prepare_floats(product['xmax']), self.prepare_floats(product['ymax']),
                               self.prepare_floats(product['xmin']), self.prepare_floats(product['ymin']),\
                                    self.prepare_floats(product['confidence']), image_id]
                              for product in self.products]

        flatten = sum(products_inference, [])  # Flatten the 2d list of products into 1d
        # --- Making the query to match dynamically the products
        product_query = '(%s, %s, %s, %s, %s, %s, %s), '.format(imageId=image_id)
        products_val_list = product_query * len(self.products)
        products_val_list = products_val_list[:-2] + ';'  # Removing the last comma with ;
        return """INSERT INTO nds.product (productId, xmax, ymax, xmin, ymin, confidence, imageId) VALUES {products}"""\
                   .format(products=products_val_list), flatten
