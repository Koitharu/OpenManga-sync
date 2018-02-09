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