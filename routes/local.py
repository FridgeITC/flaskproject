from flask import Blueprint
from flask import request
from flask_jwt import jwt_required
from type.ModelLocal import ModelLocal

local = Blueprint('local', __name__, url_prefix='/local')

@local.get('/')
@jwt_required()
def get_all():
  """
  List all locals
  ---
  tags:
    - local
  security:
  - JWT: ['Authorization']
  responses:
    200:
      description: List of locals
      schema:
        type: array
        items:
          type: object
          properties:
            id:
              type: integer
              example: 24
            name:
              type: string
              example: 'OXXO'
            zoneId:
              type: integer
              example: 1
  """
  return ModelLocal.get_all()

@local.post('/add')
@jwt_required()
def add():
  """
  Add new local
  ---
  tags:
    - local
  security:
  - JWT: ['Authorization']
  parameters:
  - in: 'body'
    name: 'body'
    description: 'Accepts name and zone ID'
    required: true,
    schema:
      type: 'object'
      properties:
        name:
          type: string
          example: 'OXXO'
        zone:
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
            example: 'Local added succesfully'
  """
  _json = request.json
  return ModelLocal.add(_json)

@local.post('/delete')
@jwt_required()
def delete():
  """
  Delete local by ID
  ---
  tags:
    - local
  security:
  - JWT: ['Authorization']
  parameters:
  - in: 'body'
    name: 'body'
    description: 'Accepts a local ID'
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
            example: 'Local removed succesfully'
  """
  _json = request.json
  return ModelLocal.delete(_json)