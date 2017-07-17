#!/usr/bin/env python3
import os, logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from release_config import ReleaseConfig

# init logging
logfile = os.path.dirname(os.path.realpath(__file__)) + u'/../logs/main.log'
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = RotatingFileHandler(logfile, maxBytes=20, backupCount=5)
handler.setFormatter(logging.Formatter(u'%(filename)s[LINE:%(lineno)d] %(levelname)-8s [%(asctime)s]  %(message)s'))
log.addHandler(handler)

# init flask
app = Flask(__name__)
api = Api(app)
app.config.from_object(ReleaseConfig)
db = SQLAlchemy(app)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

if __name__ == '__main__':
	from resources.user import UserApi
	from resources.history import HistoryApi
	from resources.favourites import FavouritesApi

	app.logger.addHandler(handler)
	api.add_resource(UserApi, '/api/user')
	api.add_resource(HistoryApi, '/api/history')
	api.add_resource(FavouritesApi, '/api/favourites')
	app.run(host=app.config['HOST_IP'])
