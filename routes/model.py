from flask import Blueprint

model = Blueprint('model', __name__)

@model.get('/')
def get_all():
  return []
