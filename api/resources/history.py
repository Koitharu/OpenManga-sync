from datetime import datetime

from flask import json
from flask_restful import reqparse, Resource, marshal_with

from api import log, db
from api.auth import authorized_only
from api.constants import *
from api.models.history import History
from api.models.manga import Manga
from api.schemas import base_schema, history_list_schema

parser = reqparse.RequestParser()
parser.add_argument('updated')
parser.add_argument('deleted')
parser.add_argument('id', type=int)


class HistoryApi(Resource):
	# get all history
	@marshal_with(history_list_schema)
	@authorized_only
	def get(self, token):
		try:
			history = History.query.filter(History.user_id == token.user_id).all()
			return {'all': history}
		except Exception as e:
			log.error(e)
			return {'success': False, 'errno': ERRNO_INTERNAL_UNKNOWN}, 500

	# data synchronization - post and get updates
	@marshal_with(history_list_schema)
	@authorized_only
	def post(self, token):
		try:
			args = parser.parse_args()
			user = token.user
			last_sync = token.last_sync_history
			history = History.query.filter(History.user_id == user.id)
			if last_sync is not None:
				history = history.filter(History.updated_at > last_sync)
			result = history.all()

			data = json.loads(args['data'])

			for item in data:
				item['updated_at'] = datetime.fromtimestamp(item['updated_at'] / 1000.0)
				obj = History(**item)
				obj.manga = Manga(**item['manga'])
				obj.user_id = user.id
				obj.manga_id = obj.manga.id
				manga = Manga.query.get(obj.manga_id)
				if manga is None:
					db.session.add(obj.manga)
					db.session.flush()
				hist = History.query.filter(History.manga_id == obj.manga_id, History.user_id == obj.user_id).first()
				if hist is None:
					db.session.add(obj)
				else:
					hist.chapter = obj.chapter
					hist.page = obj.page
					hist.size = obj.size
					hist.isweb = obj.isweb
					hist.updated_at = obj.updated_at
				db.session.flush()

			token.last_sync_history = datetime.now()
			db.session.flush()
			db.session.commit()
			return {'data': result}
		except Exception as e:
			db.session.rollback()
			log.exception(e)
			return {'success': False, 'errno': ERRNO_INTERNAL_UNKNOWN}, 500

	# delete one item from history
	@marshal_with(base_schema)
	@authorized_only
	def delete(self, token):
		try:
			args = parser.parse_args()
			user = token.user
			manga_id = args['id']
			if manga_id is None:
				return {'success': False, 'errno': ERRNO_FIELDS_ABSENT}, 400

			item = History.query.filter(History.manga_id == manga_id).filter(History.user_id == user.id).one_or_none()
			if item is None:
				return {'success': False, 'errno': ERRNO_INVALID_KEY}, 404
			else:
				item.updated_at = datetime.now()
				item.removed = True
			db.session.flush()
			db.session.commit()
		except Exception as e:
			log.exception(e)
			db.session.rollback()
			return {'success': False, 'errno': ERRNO_INTERNAL_UNKNOWN}, 500
