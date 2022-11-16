from flask import Flask
from routes.fridge import fridge
from routes.model import model
from routes.zone import zone
from routes.local import local
from db import mysql, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_HOST

app = Flask(__name__)
app.config['SECRET_KEY'] = 'XDYgFZYLry5Gk7um04JzPOhhuNbzf9cH'

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