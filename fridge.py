from flask import Blueprint

fridge = Blueprint('auth', __name__,  url_prefix='/api/v1/fridge')

@fridge.get('/')
def get_all():
  return []

@fridge.get('/add')
def register():
  return 'Fridge added'
