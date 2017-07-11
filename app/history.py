from flask import json
from flask_restful import Resource, reqparse
from pymysql.cursors import DictCursor

from app.manga import insert_manga
from openmanga import mysql, uid_by_token

parser = reqparse.RequestParser()
parser.add_argument('X-AuthToken', location='headers')
parser.add_argument('data')
parser.add_argument('timestamp', type=int)


class History(Resource):
	def post(self):
		args = parser.parse_args()
		token = args['X-AuthToken']
		data = json.loads(args['data'])
		conn = None
		cursor = None
		try:
			conn = mysql.connect()
			cursor = conn.cursor(DictCursor)
			uid = uid_by_token(conn, token)
			if uid is None:
				return {'state': 'fail', 'message': 'Invalid token'}
			conn.begin()
			for item in data:
				insert_manga(item)
				cursor.execute(
					"INSERT INTO history (user_id, manga_id, chapter, page, size, isweb) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE chapter = %s, page = %s, size = %s, isweb = %s",
					(uid, item['id'], item['chapter'], item['page'], 0, item['isweb'], item['chapter'], item['page'], 0, item['isweb']))
			conn.commit()
			return {'state': 'success'}
		except Exception as e:
			conn.rollback()
			return {'state': 'fail', 'message': str(e)}
		finally:
			if conn is not None:
				conn.close()
			if cursor is not None:
				cursor.close()

	def get(self):
		args = parser.parse_args()
		token = args['X-AuthToken']
		timestamp = args['timestamp']
		conn = None
		cursor = None
		try:
			conn = mysql.connect()
			cursor = conn.cursor(DictCursor)
			uid = uid_by_token(conn, token)
			if uid is None:
				return {'state': 'fail', 'message': 'Invalid token'}
			if timestamp is None:
				cursor.execute(
					"SELECT id, name, subtitle, summary, path, preview, provider, chapter, isweb, page, rating, UNIX_TIMESTAMP(IFNULL(updated_at, created_at)) * 1000 AS timestamp FROM mangas LEFT JOIN history ON mangas.id = history.manga_id WHERE user_id = %s",
					uid)
			else:
				cursor.execute(
					"SELECT id, name, subtitle, summary, path, preview, provider, chapter, isweb, page, rating, UNIX_TIMESTAMP(IFNULL(updated_at, created_at)) * 1000 AS timestamp FROM mangas LEFT JOIN history ON mangas.id = history.manga_id WHERE user_id = %s AND (created_at > %s OR updated_at >= %s)",
					(uid, timestamp, timestamp))
			rv = cursor.fetchall()
			return {'state': 'success', 'data': rv}
		except Exception as e:
			conn.rollback()
			return {'state': 'fail', 'message': str(e)}
		finally:
			if conn is not None:
				conn.close()
			if cursor is not None:
				cursor.close()

	def delete(self):
		args = parser.parse_args()
		token = args['X-AuthToken']
		data = json.loads(args['data'])
		conn = None
		cursor = None
		try:
			conn = mysql.connect()
			cursor = conn.cursor()
			uid = uid_by_token(conn, token)
			if uid is None:
				return {'state': 'fail', 'message': 'Invalid token'}
			conn.begin()
			for item in data:
				insert_manga(item)
				cursor.execute(
					"DELETE FROM history WHERE user_id = %s AND manga_id = %s", (uid, item['id']))
			conn.commit()
			return {'state': 'success'}
		except Exception as e:
			conn.rollback()
			return {'state': 'fail', 'message': str(e)}
		finally:
			if conn is not None:
				conn.close()
			if cursor is not None:
				cursor.close()
