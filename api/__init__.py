import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from api.release_config import ReleaseConfig

# init logging
logfile = os.path.dirname(os.path.realpath(__file__)) + u'/../logs/main.log'
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = RotatingFileHandler(logfile, maxBytes=5120, backupCount=5)
handler.setFormatter(logging.Formatter(u'%(filename)s[LINE:%(lineno)d] %(levelname)-8s [%(asctime)s]  %(message)s'))
log.addHandler(handler)

app = Flask(__name__)
api = Api(app)
app.config.from_object(ReleaseConfig)
app.logger.addHandler(handler)
db = SQLAlchemy(app)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
