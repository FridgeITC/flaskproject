import datetime

from flask import Flask
from flasgger import Swagger
from routes.fridge import fridge
from routes.model import model
from routes.zone import zone
from routes.local import local
from routes.catalog import catalog
from db import mysql, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_HOST

app = Flask(__name__)
app.config['SECRET_KEY'] = 'XDYgFZYLry5Gk7um04JzPOhhuNbzf9cH'
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(seconds=10080)
# swagger
app.config['SWAGGER'] = {'title': 'Fridge', 'uiversion': 3}
SWAGGER_TEMPLATE = {"securityDefinitions": {"JWT": {"type": "apiKey", "name": "Authorization", "in": "header"}}}

swagger_config = {
  'headers': [],
  'specs': [
    {
      'endpoint': 'apispec_1',
      'route': '/apispec_1.json',
      'rule_filter': lambda rule: True,
      'mode_filter': lambda tag: True
    }
  ],
  'static_url_path': '/flasgger_static',
  'swagger_ui': True,
  'specs_route': '/swagger/'
}

swagger = Swagger(app, config=swagger_config, template=SWAGGER_TEMPLATE)

# db
app.config['MYSQL_DATABASE_USER'] = MYSQL_USER
app.config['MYSQL_DATABASE_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_DATABASE_DB'] = MYSQL_DB
app.config['MYSQL_DATABASE_HOST'] = MYSQL_HOST
mysql.init_app(app)

# routes
app.register_blueprint(fridge)
app.register_blueprint(model)
app.register_blueprint(zone)
app.register_blueprint(local)
app.register_blueprint(catalog)