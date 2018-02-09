from flask_restful import fields


class Milliseconds(fields.Raw):
	def format(self, value):
		return int(value.timestamp() * 1000)


base_schema = {
	'success': fields.Boolean(default=True),
	'errno': fields.Integer(default=0)
}

devices_schema = {
	'devices': fields.List(fields.Nested({
		'id': fields.Integer,
		'device': fields.String,
		'created_at': Milliseconds(attribute='created_at')
	}), default=[])
}

devices_schema.update(base_schema)

token_schema = {
	'token': fields.String
}

token_schema.update(base_schema)

manga_schema = {
	'id': fields.Integer,
	'name': fields.String,
	'summary': fields.String,
	'genres': fields.String,
	'url': fields.String,
	'thumbnail': fields.String,
	'provider': fields.String,
	'status': fields.Integer,
	'rating': fields.Integer
}

manga_list_schema = {
	'data': fields.List(fields.Nested(manga_schema, default=[]), default=[])
}

manga_list_schema.update(base_schema)

history_schema = {
	'manga': fields.Nested(manga_schema),
	'chapter_id': fields.Integer,
	'page_id': fields.Integer,
	'updated_at': Milliseconds(attribute='updated_at'),
	'reader_preset': fields.Integer,
	'total_chapters': fields.Integer,
	'removed': fields.Boolean
}

history_list_schema = {
	'data': fields.List(fields.Nested(history_schema, default=[]), default=[])
}

history_list_schema.update(base_schema)

favourites_schema = {
	'manga': fields.Nested(manga_schema),
	'category_id': fields.Integer,
	'total_chapters': fields.Integer,
	'new_chapters': fields.Integer,
	'updated_at': Milliseconds(attribute='updated_at'),
	'removed': fields.Boolean
}

favourites_list_schema = {
	'data': fields.List(fields.Nested(favourites_schema, default=[]), default=[])
}

favourites_list_schema.update(base_schema)
