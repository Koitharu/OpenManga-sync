import logging
from datetime import datetime

from flask import json
from flask_restful import Resource, reqparse, marshal_with

from app import db, log
from common.auth import auth_required
from common.models import Token, Manga, Favourite, Deleted
from common.schemas import favourites_schema, base_schema

parser = reqparse.RequestParser()
parser.add_argument('updated')
parser.add_argument('deleted')
parser.add_argument('id', type=int)


class FavouritesApi(Resource):
	# get all favourites
	@marshal_with(favourites_schema)
	@auth_required
	def get(self, token):
		try:
			user = token.user
			favourites = Favourite.query.filter(Favourite.user_id == user.id).all()
			return {'all': favourites}
		except Exception as e:
			log.exception(e)
			return {'state': 'fail', 'message': str(e)}, 500

	# data synchronization - post and get updates
	@marshal_with(favourites_schema)
	@auth_required
	def post(self, token):
		try:
			args = parser.parse_args()
			user = token.user
			last_sync = token.last_sync_favourites
			favourites = Favourite.query.filter(Favourite.user_id == user.id)
			if last_sync is not None:
				favourites = favourites.filter(Favourite.updated_at > last_sync)
			updated = favourites.all()

			deleted = Deleted.query.filter(Deleted.subject == 'favourites', Deleted.user_id == user.id)
			if last_sync is not None:
				deleted = deleted.filter(Deleted.deleted_at > last_sync)
			deleted = deleted.all()

			client_updated = json.loads(args['updated'])

			for item in client_updated:
				item['updated_at'] = datetime.fromtimestamp(item['timestamp'] / 1000.0)
				item.pop('timestamp', None)
				obj = Favourite(**item)
				obj.manga = Manga(**item['manga'])
				obj.user_id = user.id
				obj.manga_id = obj.manga.id
				manga = Manga.query.get(obj.manga_id)
				if manga is None:
					db.session.add(obj.manga)
					db.session.flush()
				fav = Favourite.query.filter(Favourite.manga_id == obj.manga_id,
											 Favourite.user_id == obj.user_id).first()
				if fav is None:
					db.session.add(obj)
				else:
					fav.updated_at = obj.updated_at
				db.session.flush()

			client_deleted = json.loads(args['deleted'])
			for item in client_deleted:
				item['deleted_at'] = datetime.fromtimestamp(item['timestamp'] / 1000.0)
				item.pop('timestamp', None)
				obj = Deleted(**item)
				obj.user_id = user.id
				obj.subject = 'favourites'
				udeleted = Deleted.query.filter(Deleted.manga_id == obj.manga_id,
												Deleted.user_id == obj.user_id).first()
				if udeleted is None:
					db.session.add(obj)
				else:
					udeleted.deleted_at = obj.deleted_at
				db.session.flush()
				Favourite.query.filter(Favourite.manga_id == obj.manga_id, Favourite.user_id == obj.user_id).delete()

				db.session.flush()

			token.last_sync_favourites = datetime.now()
			db.session.flush()
			db.session.commit()
			return {'updated': updated, 'deleted': deleted}
		except Exception as e:
			log.exception(e)
			db.session.rollback()
			return {'state': 'fail', 'message': str(e)}, 500

	# delete one item from favourites
	@marshal_with(base_schema)
	@auth_required
	def delete(self, token):
		try:
			args = parser.parse_args()
			user = token.user
			manga_id = args['id']

			deleted = Favourite.query.filter(Favourite.manga_id == manga_id).delete()
			if deleted > 0:
				obj = Deleted()
				obj.manga_id = manga_id
				obj.user_id = user.id
				obj.subject = 'favourites'
				obj.deleted_at = datetime.now()
				db.session.add(obj)

			db.session.flush()
			db.session.commit()
		except Exception as e:
			log.exception(e)
			db.session.rollback()
			return {'state': 'fail', 'message': str(e)}, 500
