from flask import Blueprint
from flask import request
from flask_jwt import jwt_required
from type.ModelFridge import ModelFridge

fridge = Blueprint('fridge', __name__, url_prefix='/fridge')

@fridge.get('/')
@jwt_required()
def get_all():
  """
  List all fridges
  ---
  tags:
    - fridge
  security:
  - JWT: ['Authorization']
  responses:
    200:
      description: List of fridges
      schema:
        type: array
        items:
          type: object
          properties:
            id:
              type: integer
              example: 24
            localId:
              type: integer
              example: 1
            capacity:
              type: integer
              example: 22
            rows:
              type: integer
              example: 15
  """
  return ModelFridge.get_all()

@fridge.post('/add')
@jwt_required()
def add():
  """
  Add new fridge
  ---
  tags:
    - fridge
  security:
  - JWT: ['Authorization']
  parameters:
  - in: 'body'
    name: 'body'
    description: 'Accepts local ID, capacity and rows'
    required: true,
    schema:
      type: 'object'
      properties:
        local:
          type: integer
          example: 1
        capacity:
          type: integer
          example: 50
        rows:
          type: integer
          example: 5
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
            example: 'Fridge added succesfully'
  """
  _json = request.json
  return ModelFridge.add(_json)

@fridge.post('/delete')
@jwt_required()
def delete():
  """
  Delete fridge by ID
  ---
  tags:
    - fridge
  security:
  - JWT: ['Authorization']
  parameters:
  - in: 'body'
    name: 'body'
    description: 'Accepts a fridge ID'
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
            example: 'Fridge removed succesfully'
  """
  _json = request.json
  return ModelFridge.delete(_json)