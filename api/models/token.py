from sqlalchemy import func

from api import db


class Token(db.Model):
	__tablename__ = 'tokens'
	id = db.Column(db.Integer, autoincrement=True, nullable=False)
	token = db.Column(db.String(36), primary_key=True, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True, nullable=False)
	device = db.Column(db.String(32), nullable=False)
	created_at = db.Column(db.TIMESTAMP, nullable=False, default=func.current_timestamp())
	expires_at = db.Column(db.TIMESTAMP, nullable=True, default=None)
	last_sync_history = db.Column(db.TIMESTAMP, nullable=True, default=None)
	last_sync_favourites = db.Column(db.TIMESTAMP, nullable=True, default=None)