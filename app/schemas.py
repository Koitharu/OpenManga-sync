from marshmallow import Schema, fields, post_load

from app.models import Manga, History


class DeviceSchema(Schema):
	created_at = fields.Function(lambda obj: int(obj.created_at.timestamp() * 100))

	class Meta:
		fields = ("device", "created_at")


class MangaSchema(Schema):
	id = fields.Integer()
	name = fields.String()
	subtitle = fields.String()
	summary = fields.String()
	path = fields.String()
	preview = fields.String()
	provider = fields.String()
	rating = fields.Integer()

	@post_load
	def make_user(self, data):
		return Manga(**data)

	class Meta:
		fields = ("id", "name", "subtitle", "summary", "preview", "provider", "path", "rating")


class HistorySchema(Schema):
	manga = fields.Nested(MangaSchema)
	timestamp = fields.Function(lambda obj: int(obj.updated_at.timestamp() * 100))

	@post_load
	def make_user(self, data):
		return History(**data)

	class Meta:
		fields = ("chapter", "page", "size", "isweb", "timestamp", "manga")
