#!/usr/bin/env python3
import os

from flask import Flask
from flask_restful import Api
from flaskext.mysql import MySQL

from config import Config

mysql = MySQL()
app = Flask(__name__)
api = Api(app)
app.config.from_object(Config)
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
	from app.history import History
	from app.user import User
	api.add_resource(User, '/api/user')
	api.add_resource(History, '/api/history')
	app.run(host=app.config['HOST_IP'])
