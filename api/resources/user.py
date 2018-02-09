import hashlib
import uuid
from datetime import datetime

from flask_restful import Resource, marshal_with, reqparse

from api import log, db
from api.auth import authorized_only
from api.models.token import Token
from api.models.user import User
from api.constants import *
from api.schemas import devices_schema, token_schema, base_schema

parser = reqparse.RequestParser()
parser.add_argument('login')
parser.add_argument('id', type=int)
parser.add_argument('password')
parser.add_argument('device')
parser.add_argument('self', type=int, choices=(0, 1), default=0)
parser.add_argument('expires', type=int)


class UserApi(Resource):
	@marshal_with(devices_schema)
	@authorized_only
	def get(self, token):
		try:
			args = parser.parse_args()
			user = token.user
			tokens = Token.query.filter(Token.user_id == user.id)
			if args['self'] == 0:
				tokens = tokens.filter(Token.token != token.token)
			tokens = tokens.order_by(Token.created_at.desc()).all()
			return {'devices': tokens}
		except Exception as e:
			log.exception(e)
			return {'success': False, 'errno': ERRNO_INTERNAL_UNKNOWN}, 500

	# sign in
	@marshal_with(token_schema)
	def post(self):
		try:
			args = parser.parse_args()
			if (args['device'] is None) or (args['login'] is None) or (args['password'] is None):
				return {'success': False, 'errno': ERRNO_FIELDS_ABSENT}, 400
			pass_md5 = hashlib.md5(args['password'].encode('utf-8')).hexdigest()
			user = User.query.filter(User.login == args['login'], User.password == pass_md5).one_or_none()
			if user is None:
				log.info("Invalid login/password")
				return {'success': False, 'errno': ERRNO_INVALID_PASSWORD}, 403
			new_token = Token(token=str(uuid.uuid4()), user_id=user.id, device=args['device'])
			if args['expires'] is not None:
				new_token.expires_at = datetime.fromtimestamp(args['expires'] / 1000.0)
			db.session.add(new_token)
			db.session.commit()
			log.info("Created new token: %s" % new_token.token)
			return {'token': new_token.token}
		except Exception as e:
			db.session.rollback()
			log.exception(e)
			return {'success': False, 'errno': ERRNO_INTERNAL_UNKNOWN}, 500

	# sign up
	@marshal_with(token_schema)
	def put(self):
		try:
			args = parser.parse_args()
			if (args['device'] is None) or (args['login'] is None) or (args['password'] is None):
				return {'success': False, 'errno': ERRNO_FIELDS_ABSENT}, 400
			pass_md5 = hashlib.md5(args['password'].encode('utf-8')).hexdigest()
			new_user = User(login=args['login'], password=pass_md5)
			db.session.add(new_user)
			new_token = Token(token=str(uuid.uuid4()), user=new_user, device=args['device'])
			if args['expires'] is not None:
				new_token.expires_at = datetime.fromtimestamp(args['expires'] / 1000.0)
			db.session.add(new_token)
			db.session.commit()
			return {'token': new_token.token}
		except Exception as e:
			db.session.rollback()
			log.error(e)
			return {'success': False, 'errno': ERRNO_INTERNAL_UNKNOWN}, 500

	# close session(remove token)
	@marshal_with(base_schema)
	@authorized_only
	def delete(self, token):
		try:
			args = parser.parse_args()
			user = token.user
			if args['self'] == 1:
				token_rm = token
			else:
				token_rm = Token.query.filter(Token.id == args['id']).one_or_none()
			if token_rm is None:
				return {'success': False, 'errno': ERRNO_INVALID_DEVICE}, 400
			if user.id != token_rm.user.id:
				return {'success': False, 'errno': ERRNO_TOKEN_INVALID}, 403
			db.session.delete(token_rm)
			db.session.commit()
			return {}
		except Exception as e:
			db.session.rollback()
			log.exception(e)
			return {'success': False, 'errno': ERRNO_INTERNAL_UNKNOWN}, 500
