from flask_restful import fields


class Milliseconds(fields.Raw):
	def format(self, value):
		return int(value.timestamp() * 1000)


base_schema = {
	'state': fields.String(default='success'),
	'message': fields.String(default='')
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
	'subtitle': fields.String,
	'summary': fields.String,
	'path': fields.String,
	'preview': fields.String,
	'provider': fields.String,
	'rating': fields.Integer
}

deleted_item_schema = {
	'manga_id': fields.Integer,
	'deleted_at': Milliseconds(attribute='deleted_at')
}

history_item_schema = {
	'manga': fields.Nested(manga_schema),
	'timestamp': Milliseconds(attribute='updated_at'),
	'page': fields.Integer,
	'chapter': fields.Integer,
	'size': fields.Integer,
	'isweb': fields.Integer
}

history_schema = {
	'all': fields.List(fields.Nested(history_item_schema, default=[]), default=[]),
	'updated': fields.List(fields.Nested(history_item_schema, default=[]), default=[]),
	'deleted': fields.List(fields.Nested(deleted_item_schema, default=[]), default=[])
}

history_schema.update(base_schema)

favourites_item_schema = {
	'manga': fields.Nested(manga_schema),
	'timestamp': Milliseconds(attribute='updated_at')
}

favourites_schema = {
	'all': fields.List(fields.Nested(history_item_schema, default=[]), default=[]),
	'updated': fields.List(fields.Nested(history_item_schema, default=[]), default=[]),
	'deleted': fields.List(fields.Nested(deleted_item_schema, default=[]), default=[])
}

favourites_schema.update(base_schema)

mangas_schema = {
	'all': fields.List(fields.Nested(manga_schema, default=[]), default=[])
}

mangas_schema.update(base_schema)
