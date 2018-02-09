from sqlalchemy import func

from api import db


class Category(db.Model):
	__tablename__ = 'categories'
	id = db.Column(db.Integer, primary_key=True, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
	name = db.Column(db.String(24), nullable=False)
	created_at = db.Column(db.TIMESTAMP, nullable=False, default=func.current_timestamp())
