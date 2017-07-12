from flask import json
from flask_restful import Resource, reqparse

from app.models import Token, History, Manga
from app.schemas import HistorySchema
from openmanga import db

parser = reqparse.RequestParser()
parser.add_argument('X-AuthToken', location='headers')
parser.add_argument('updated')
parser.add_argument('deleted')


class HistoryApi(Resource):
	def get(self):
		try:
			args = parser.parse_args()
			token = args['X-AuthToken']
			user = Token.query.get(token).user
			history = History.query.filter(History.user_id == user.id).all()
			schema = HistorySchema(many=True)
			return {'state': 'success', 'all': schema.dumps(history).data}
		except Exception as e:
			return {'state': 'fail', 'message': str(e)}

	def post(self):
		try:
			args = parser.parse_args()
			token = Token.query.get(args['X-AuthToken'])
			user = token.user
			last_sync = token.last_sync_history
			history = History.query.filter(History.user_id == user.id)
			if last_sync is not None:
				history = history.folter(History.updated_at > last_sync)
			history = history.all()
			schema = HistorySchema(many=True)
			updated = schema.dumps(history).data

			client_updated = schema.loads(args['updated']).data

			for item in client_updated:
				item.user_id = user.id
				new_item = db.session.merge(item)
				db.session.flush()
			db.session.commit()
			return {'state': 'success', 'updated': updated}
		except Exception as e:
			db.session.rollback()
			return {'state': 'fail', 'message': str(e)}






		# updated = json.loads(args['updated'])
		# #deleted = json.loads(args['deleted'])
		# conn = None
		# cursor = None
		# try:
		# 	conn = mysql.connect()
		# 	cursor = conn.cursor(DictCursor)
		# 	uid = uid_by_token(conn, token)
		# 	if uid is None:
		# 		return {'state': 'fail', 'message': 'Invalid token'}
		# 	conn.begin()
		# 	#data from database
		# 	if timestamp is None:
		# 		cursor.execute(
		# 			"SELECT id, name, subtitle, summary, path, preview, provider, chapter, isweb, page, rating, UNIX_TIMESTAMP(IFNULL(updated_at, created_at)) * 1000 AS timestamp FROM mangas LEFT JOIN history ON mangas.id = history.manga_id WHERE user_id = %s",
		# 			uid)
		# 	else:
		# 		cursor.execute(
		# 			"SELECT id, name, subtitle, summary, path, preview, provider, chapter, isweb, page, rating, UNIX_TIMESTAMP(IFNULL(updated_at, created_at)) * 1000 AS timestamp FROM mangas LEFT JOIN history ON mangas.id = history.manga_id WHERE user_id = %s AND (created_at > %s OR updated_at >= %s)",
		# 			(uid, timestamp, timestamp))
		# 	rv = cursor.fetchall()
		# 	#data from device
		# 	for item in updated:
		# 		insert_manga(item)
		# 		cursor.execute(
		# 			"INSERT INTO history (user_id, manga_id, chapter, page, size, isweb) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE chapter = %s, page = %s, size = %s, isweb = %s",
		# 			(uid, item['id'], item['chapter'], item['page'], 0, item['isweb'], item['chapter'], item['page'], 0, item['isweb']))
		# 	conn.commit()
		# 	return {'state': 'success', 'updated': rv}
		# except Exception as e:
		# 	conn.rollback()
		# 	return {'state': 'fail', 'message': str(e)}
		# finally:
		# 	if conn is not None:
		# 		conn.close()
		# 	if cursor is not None:
		# 		cursor.close()
