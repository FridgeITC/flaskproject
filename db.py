from app import app
from flaskext.mysql import MySQL

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'ubjfljub_fridge'
app.config['MYSQL_DATABASE_PASSWORD'] = 'taMG%[,WZ#G^'
app.config['MYSQL_DATABASE_DB'] = 'ubjfljub_fridge'
app.config['MYSQL_DATABASE_HOST'] = 'hernandez.dev'
mysql.init_app(app)