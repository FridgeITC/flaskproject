from flask import Flask
from routes.fridge import fridge
from routes.model import model
app = Flask(__name__)
app.config['SECRET_KEY'] = 'XDYgFZYLry5Gk7um04JzPOhhuNbzf9cH'

# routes
app.register_blueprint(fridge)
app.register_blueprint(model)