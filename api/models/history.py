from sqlalchemy import func

from api import db


class History(db.Model):
	__tablename__ = 'history'
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
	manga_id = db.Column(db.Integer, db.ForeignKey('mangas.id'), primary_key=True, nullable=False)
	chapter_id = db.Column(db.Integer, nullable=False)
	page_id = db.Column(db.Integer, nullable=False)
	updated_at = db.Column(db.TIMESTAMP, nullable=False, default=func.current_timestamp())
	reader_preset = db.Column(db.SmallInteger, nullable=False)
	total_chapters = db.Column(db.Integer, nullable=False)
	removed = db.Column(db.Boolean, nullable=False)
	manga = db.relationship('Manga', cascade="merge")
