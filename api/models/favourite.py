from sqlalchemy import func

from api import db


class Favourite(db.Model):
	__tablename__ = 'favourites'
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
	manga_id = db.Column(db.Integer, db.ForeignKey('mangas.id'), primary_key=True, nullable=False)
	category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), primary_key=True, nullable=False)
	total_chapters = db.Column(db.Integer, nullable=False)
	new_chapters = db.Column(db.Integer, nullable=False)
	updated_at = db.Column(db.TIMESTAMP, nullable=False, default=func.current_timestamp())
	removed = db.Column(db.Boolean, nullable=False)
	manga = db.relationship('Manga', cascade="merge")
	category = db.relation('Category', cascade="merge")
