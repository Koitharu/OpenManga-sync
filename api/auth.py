import datetime
from functools import wraps

from flask import request

from api import db, log
from api.models.token import Token
from api.constants import *


def authorized_only(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		try:
			if 'X-Auth-Token' not in request.headers:
				return {'success': False, 'errno': ERRNO_TOKEN_ABSENT}, 403
			token = request.headers['X-Auth-Token']
			if token is None:
				return {'success': False, 'errno': ERRNO_TOKEN_ABSENT}, 403
			token = Token.query.get(token)
			if token is None:
				return {'success': False, 'errno': ERRNO_TOKEN_INVALID}, 403
			if token.expires_at is not None and token.expires_at < datetime.datetime.now():
				token.delete()
				db.session.flush()
				db.session.commit()
				return {'success': False, 'errno': ERRNO_TOKEN_OUTDATED}, 403
			return f(token=token, *args, **kwargs)
		except Exception as e:
			db.session.rollback()
			log.exception(e)
			return {'success': False, 'errno': ERRNO_INTERNAL_UNKNOWN}, 500

	return decorated
