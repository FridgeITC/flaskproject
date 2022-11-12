from flask import Blueprint

fridge = Blueprint('fridge', __name__)

@fridge.get('/')
def get_all():
  return []

@fridge.get('/add')
def register():
  return 'Fridge added'
