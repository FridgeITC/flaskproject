from flask import Blueprint
from flask import request
from flask_jwt import jwt_required
from type.ModelLocal import ModelLocal

local = Blueprint('local', __name__, url_prefix='/local')

@local.get('/')
@jwt_required()
def get_all():
  return ModelLocal.get_all()

@local.post('/add')
@jwt_required()
def add():
  _json = request.json
  return ModelLocal.add(_json)

@local.post('/delete')
@jwt_required()
def delete():
  _json = request.json
  return ModelLocal.delete(_json)