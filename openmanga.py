from flask import Flask
from flask_restful import Api
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
api = Api(app)
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'www'
app.config['MYSQL_DATABASE_PASSWORD'] = 'qwerty'
app.config['MYSQL_DATABASE_DB'] = 'openmanga'
app.config['MYSQL_DATABASE_HOST'] = '192.168.0.222'
app.config['MYSQL_USE_UNICODE'] = True
mysql.init_app(app)


def uid_by_token(connection, token):
	cursor = None
	try:
		cursor = connection.cursor()
		cursor.execute("SELECT user_id FROM tokens WHERE token = %s", token)
		rv = cursor.fetchone()
		if rv is None:
			return None
		else:
			return rv[0]
	finally:
		if cursor is not None:
			cursor.close()


if __name__ == '__main__':
	from history import History
	from user import User
	api.add_resource(User, '/api/user')
	api.add_resource(History, '/api/history')
	app.run(host='192.168.0.104')
