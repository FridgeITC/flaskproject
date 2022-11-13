from flask import Blueprint
from flask import request
from flask_jwt import jwt_required
from models.ModelFridge import ModelFridge

fridge = Blueprint('fridge', __name__, url_prefix='/fridge')

@fridge.get('/')
@jwt_required()
def get_all():
  return ModelFridge.get_all()

@fridge.post('/add')
@jwt_required()
def add():
  _json = request.json
  return ModelFridge.add(_json)

@fridge.post('/delete')
@jwt_required()
def delete():
  _json = request.json
  return ModelFridge.delete(_json)