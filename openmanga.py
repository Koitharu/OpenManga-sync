#!/usr/bin/env python3

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_restful import Api

from release_config import ReleaseConfig

app = Flask(__name__)
api = Api(app)
app.config.from_object(ReleaseConfig)
db = SQLAlchemy(app)

if __name__ == '__main__':
	from app.user import UserApi
	from app.history import HistoryApi

	api.add_resource(UserApi, '/api/user')
	api.add_resource(HistoryApi, '/api/history')
	app.run(host=app.config['HOST_IP'])
