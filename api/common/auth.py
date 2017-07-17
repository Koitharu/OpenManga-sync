import datetime
from functools import wraps

from flask import request

from app import db
from common.models import Token


def auth_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		try:
			token = request.headers['X-AuthToken']
			if token is None:
				return {'state': 'fail', 'message': 'Authorization required'}, 403
			token = Token.query.get(token)
			if token is None:
				return {'state': 'fail', 'message': 'Invalid token'}, 403
			if token.expires_at is not None and token.expires_at < datetime.datetime.now():
				token.delete()
				db.session.flush()
				db.session.commit()
				return {'state': 'fail', 'message': 'Token was expired'}, 403
			return f(token=token, *args, **kwargs)
		except Exception as e:
			return {'state': 'fail', 'message': str(e)}, 500

	return decorated
