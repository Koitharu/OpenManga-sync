from api import db


class Manga(db.Model):
	__tablename__ = 'mangas'
	id = db.Column(db.Integer, primary_key=True, nullable=False)
	name = db.Column(db.String(120), nullable=False)
	summary = db.Column(db.String(120), nullable=False)
	genres = db.Column(db.String(140), nullable=False)
	url = db.Column(db.String(120), nullable=False)
	thumbnail = db.Column(db.String(120), nullable=False)
	provider = db.Column(db.String(120), nullable=False)
	status = db.Column(db.SmallInteger, nullable=False)
	rating = db.Column(db.SmallInteger, nullable=False)
