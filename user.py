import uuid

from flask_restful import Resource, reqparse
from pymysql.cursors import DictCursor

from openmanga import mysql, api, uid_by_token

parser = reqparse.RequestParser()
parser.add_argument('login', location='form')
parser.add_argument('password', location='form')
parser.add_argument('device', location='form')
parser.add_argument('X-AuthToken', location='headers')


class User(Resource):
	def get(self):
		args = parser.parse_args()
		token = args['X-AuthToken']
		conn = None
		cursor = None
		try:
			conn = mysql.connect()
			cursor = conn.cursor(DictCursor)
			uid = uid_by_token(conn, token)
			if uid is None:
				return {'state': 'fail', 'message': 'Invalid token'}
			cursor.execute("SELECT device, UNIX_TIMESTAMP(created_at) AS created_at FROM tokens WHERE user_id = %s",
						   uid)
			rv = cursor.fetchall()
			return {'state': 'success', 'devices': rv}
		except Exception as e:
			return {'state': 'fail', 'message': str(e)}
		finally:
			if conn is not None:
				conn.close()
			if cursor is not None:
				cursor.close()

	def post(self):
		conn = None
		cursor = None
		try:
			conn = mysql.connect()
			cursor = conn.cursor(DictCursor)
			args = parser.parse_args()
			cursor.execute("SELECT id FROM users WHERE login = %s AND password = MD5(%s)",
						   (args['login'], args['password']))
			rv = cursor.fetchone()
			if (rv is not None):
				uid = rv['id']
				token = str(uuid.uuid4())
				cursor.execute("INSERT INTO tokens (token, user_id, device) VALUES (%s, %s, %s)",
							   (token, uid, args['device']))
				conn.commit()
				return {'state': 'success', 'token': token}
			else:
				return {'state': 'fail', 'message': 'No such user or password invalid'}
		except Exception as e:
			return {'state': 'fail', 'message': str(e)}
		finally:
			if conn is not None:
				conn.close()
			if cursor is not None:
				cursor.close()

	def put(self):
		conn = None
		cursor = None
		try:
			conn = mysql.connect()
			cursor = conn.cursor()
			conn.begin()
			args = parser.parse_args()
			res = cursor.execute("INSERT INTO users (login, password) VALUES (%s, MD5(%s))",
								 (args['login'], args['password']))
			if (res):
				uid = cursor.lastrowid
				token = str(uuid.uuid4())
				cursor.execute("INSERT INTO tokens (token, user_id, device) VALUES (%s, %s, %s)", (token, uid,
																								   args['device']))
				conn.commit()
				return {'state': 'success', 'token': token}
			else:
				conn.rollback()
				return {'state': 'fail', 'message': 'Internal error'}
		except Exception as e:
			if conn is not None:
				conn.rollback()
			return {'state': 'fail', 'message': str(e)}
		finally:
			if conn is not None:
				conn.close()
			if cursor is not None:
				cursor.close()
