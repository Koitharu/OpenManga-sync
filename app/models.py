import datetime

from sqlalchemy import func, TypeDecorator, types

from openmanga import db


class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
	login = db.Column(db.String(32), index=True, unique=True)
	password = db.Column(db.String(32), nullable=False)
	created_at = db.Column(db.TIMESTAMP, nullable=False, default=func.current_timestamp())
	tokens = db.relationship('Token', backref='user') #, lazy='dynamic'


class Token(db.Model):
	__tablename__ = 'tokens'
	id = db.Column(db.Integer, autoincrement=True, nullable=False)
	token = db.Column(db.String(36), primary_key=True, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True, nullable=False)
	device = db.Column(db.String(32), nullable=False)
	created_at = db.Column(db.TIMESTAMP, nullable=False, default=func.current_timestamp())
	last_sync_history = db.Column(db.TIMESTAMP, nullable=True, default=None)
	last_sync_favourites = db.Column(db.TIMESTAMP, nullable=True, default=None)


class Manga(db.Model):
	__tablename__ = 'mangas'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
	name = db.Column(db.String(120), nullable=False)
	subtitle = db.Column(db.String(120), nullable=False)
	summary = db.Column(db.String(140), nullable=False)
	preview = db.Column(db.String(120), nullable=False)
	provider = db.Column(db.String(120), nullable=False)
	path = db.Column(db.String(120), nullable=False)
	rating = db.Column(db.SmallInteger, nullable=False)


class History(db.Model):
	__tablename__ = 'history'
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
	manga_id = db.Column(db.Integer, db.ForeignKey('mangas.id'), primary_key=True, nullable=False)
	updated_at = db.Column(db.TIMESTAMP, nullable=False, default=func.current_timestamp())
	chapter = db.Column(db.Integer, nullable=False)
	page = db.Column(db.Integer, nullable=False)
	size = db.Column(db.Integer, nullable=False)
	isweb = db.Column(db.SmallInteger, nullable=False)
	manga = db.relationship('Manga')