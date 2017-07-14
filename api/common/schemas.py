from flask_restful import fields


class Milliseconds(fields.Raw):
	def format(self, value):
		return int(value.timestamp() * 1000)


base_schema = {
	'state': fields.String(default='success'),
	'message': fields.String(default='')
}

devices_schema = {
	'devices': fields.Nested({
		'id': fields.Integer,
		'device': fields.String,
		'created_at': Milliseconds(attribute='created_at')
	})
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

history_item_schema = {
	'manga': fields.Nested(manga_schema),
	'timestamp': Milliseconds(attribute='updated_at'),
	'page': fields.Integer,
	'chapter': fields.Integer,
	'size': fields.Integer,
	'isweb': fields.Integer
}

history_schema = {
	'all': fields.Nested(history_item_schema),
	'updated': fields.Nested(history_item_schema)
}

history_schema.update(base_schema)

favourites_item_schema = {
	'manga': fields.Nested(manga_schema),
	'timestamp': Milliseconds(attribute='updated_at')
}

favourites_schema = {
	'all': fields.Nested(history_item_schema),
	'updated': fields.Nested(history_item_schema)
}

favourites_schema.update(base_schema)