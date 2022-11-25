from flask import Blueprint
from flask import request
from flask_jwt import jwt_required
from models.ModelZone import ModelZone

zone = Blueprint('zone', __name__, url_prefix='/zone')

@zone.get('/')
@jwt_required()
def get_all():
  """
  List all zones
  ---
  tags:
    - zone
  security:
  - JWT: ['Authorization']
  responses:
    200:
      description: List of zones
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
              example: 'Sur'
  """
  return ModelZone.get_all()

@zone.post('/add')
@jwt_required()
def add():
  """
  Add new zone
  ---
  tags:
    - zone
  security:
  - JWT: ['Authorization']
  parameters:
  - in: 'body'
    name: 'body'
    description: 'Accepts name'
    required: true,
    schema:
      type: 'object'
      properties:
        name:
          type: string
          example: 'Sur'
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
            example: 'Zone added succesfully'
  """
  _json = request.json
  return ModelZone.add(_json)

@zone.post('/delete')
@jwt_required()
def delete():
  """
  Delete zone by ID
  ---
  tags:
    - zone
  security:
  - JWT: ['Authorization']
  parameters:
  - in: 'body'
    name: 'body'
    description: 'Accepts a zone ID'
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
            example: 'Zone removed succesfully'
  """
  _json = request.json
  return ModelZone.delete(_json)