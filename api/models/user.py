from sqlalchemy import func

from api import db


class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
	login = db.Column(db.String(32), index=True, unique=True)
	password = db.Column(db.String(32), nullable=False)
	created_at = db.Column(db.TIMESTAMP, nullable=False, default=func.current_timestamp())
	tokens = db.relationship('Token', backref='user')