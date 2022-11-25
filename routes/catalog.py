from flask import Blueprint
from flask import request
from flask_jwt import jwt_required
from type.ModelCatalog import ModelCatalog

catalog = Blueprint('catalog', __name__, url_prefix='/catalog')

@catalog.get('/')
@jwt_required()
def get_all():
  """
  List all products
  ---
  tags:
    - catalog
  security:
  - JWT: ['Authorization']
  responses:
    200:
      description: List of products
      schema:
        type: array
        items:
          type: object
          properties:
            id:
              type: integer
              example: 1
            name:
              type: string
              example: 'Coca-cola Zero Lata 355ml'
            price:
              type: float
              example: 17.50
  """
  return ModelCatalog.get_all()

@catalog.post('/add')
@jwt_required()
def add():
  """
  Add new product
  ---
  tags:
    - catalog
  security:
  - JWT: ['Authorization']
  parameters:
  - in: 'body'
    name: 'body'
    description: 'Accepts name and price'
    required: true,
    schema:
      type: 'object'
      properties:
        name:
          type: string
          example: 'Fanta 355ml'
        price:
          type: float
          example: 17.50
  responses:
    200:
      schema:
        type: object
        properties:
          status:
            type: integer
            example: 200
          message:
            type: string
            example: 'Product added succesfully'
  """
  _json = request.json
  return ModelCatalog.add(_json)

@catalog.post('/delete')
@jwt_required()
def delete():
  """
  Delete product by ID
  ---
  tags:
    - catalog
  security:
  - JWT: ['Authorization']
  parameters:
  - in: 'body'
    name: 'body'
    description: 'Accepts a product ID'
    required: true,
    schema:
      type: 'object'
      properties:
        id:
          type: integer
          example: 1
  responses:
    200:
      schema:
        type: object
        properties:
          status:
            type: integer
            example: 200
          message:
            type: string
            example: 'Product removed succesfully'
  """
  _json = request.json
  return ModelCatalog.delete(_json)