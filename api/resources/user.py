import hashlib
import uuid

import logging
from flask_restful import Resource, reqparse, marshal_with

from app import db
from common.models import Token, User
from common.schemas import devices_schema, token_schema, base_schema

parser = reqparse.RequestParser()
parser.add_argument('login')
parser.add_argument('id')
parser.add_argument('password')
parser.add_argument('device')
parser.add_argument('self', type=int, choices=(0, 1), default=0)
parser.add_argument('X-AuthToken', location='headers')

logger = logging.getLogger(__name__)


class UserApi(Resource):
	@marshal_with(devices_schema)
	def get(self):
		try:
			args = parser.parse_args()
			user = Token.query.get(args['X-AuthToken']).user
			tokens = Token.query.filter(Token.user_id == user.id)
			if args['self'] == 0:
				tokens = tokens.filter(Token.token != args['X-AuthToken'])
			tokens = tokens.order_by(Token.created_at.desc()).all()
			return {'devices': tokens}
		except Exception as e:
			logger.error(e)
			return {'state': 'fail', 'message': str(e)}, 500

	@marshal_with(token_schema)
	def post(self):
		try:
			args = parser.parse_args()
			pass_md5 = hashlib.md5(args['password'].encode('utf-8')).hexdigest()
			user = User.query.filter(User.login == args['login'], User.password == pass_md5).one_or_none()
			if user is None:
				logger.info("Invalid login/password")
				return {'state': 'fail', 'message': 'No such user or password invalid'}
			new_token = Token(token=str(uuid.uuid4()), user_id=user.id, device=args['device'])
			db.session.add(new_token)
			db.session.commit()
			logger.info("Created new token: %s" % new_token.token)
			return {'token': new_token.token}
		except Exception as e:
			db.session.rollback()
			return {'state': 'fail', 'message': str(e)}, 500

	@marshal_with(token_schema)
	def put(self):
		try:
			args = parser.parse_args()
			pass_md5 = hashlib.md5(args['password'].encode('utf-8')).hexdigest()
			new_user = User(login=args['login'], password=pass_md5)
			db.session.add(new_user)
			new_token = Token(token=str(uuid.uuid4()), user=new_user, device=args['device'])
			db.session.add(new_token)
			db.session.commit()
			return {'token': new_token.token}
		except Exception as e:
			db.session.rollback()
			logger.error(e)
			return {'state': 'fail', 'message': str(e)}, 500

	@marshal_with(base_schema)
	def delete(self):
		try:
			args = parser.parse_args()
			user = Token.query.get(args['X-AuthToken']).user
			token_rm = Token.query.filter(Token.id == args['id']).one_or_none()
			if token_rm is None:
				return {'state': 'fail', 'message': 'Invalid device id'},
			if user.id != token_rm.user.id:
				return {'state': 'fail', 'message': 'Invalid token'}, 403
			db.session.delete(token_rm)
			db.session.commit()
			return {}
		except Exception as e:
			db.session.rollback()
			logger.error(e)
			return {'state': 'fail', 'message': str(e)}, 500
