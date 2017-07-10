from flask import json
from flask_restful import Resource, reqparse
from pymysql.cursors import DictCursor

from manga import insert_manga
from openmanga import mysql, api, uid_by_token

parser = reqparse.RequestParser()
parser.add_argument('X-AuthToken', location='headers')
parser.add_argument('data')


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
				cursor.execute("INSERT INTO history (user_id, manga_id, chapter, page, size, isweb) VALUES (%s, %s, %s, %s, %s, %s)",
							   (uid, item['id'], item['chapter'], item['page'], 0, item['isweb']))
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


