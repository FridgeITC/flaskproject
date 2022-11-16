from flask import Blueprint
from flask import request
from flask_jwt import jwt_required
from type.ModelZone import ModelZone

zone = Blueprint('zone', __name__, url_prefix='/zone')

@zone.get('/')
@jwt_required()
def get_all():
  return ModelZone.get_all()

@zone.post('/add')
@jwt_required()
def add():
  _json = request.json
  return ModelZone.add(_json)

@zone.post('/delete')
@jwt_required()
def delete():
  _json = request.json
  return ModelZone.delete(_json)