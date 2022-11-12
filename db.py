from app import app
from flaskext.mysql import MySQL

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'nds'
app.config['MYSQL_DATABASE_PASSWORD'] = 'rootroot'
app.config['MYSQL_DATABASE_DB'] = 'nds'
app.config['MYSQL_DATABASE_HOST'] = 'nds-fridge.cnqk716tpw2u.us-east-1.rds.amazonaws.com'
mysql.init_app(app)