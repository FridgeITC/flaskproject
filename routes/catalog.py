from flask import Blueprint
from flask import request
from flask_jwt import jwt_required
from models.ModelCatalog import ModelCatalog

catalog = Blueprint('catalog', __name__, url_prefix='/catalog')

@catalog.get('/')
@jwt_required()
def get_all():
  return ModelCatalog.get_all()

@catalog.post('/add')
@jwt_required()
def add():
  _json = request.json
  return ModelCatalog.add(_json)

@catalog.post('/delete')
@jwt_required()
def delete():
  _json = request.json
  return ModelCatalog.delete(_json)