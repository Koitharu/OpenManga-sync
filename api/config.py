class Config(object):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@server/dbname'
	SQLALCHEMY_NATIVE_UNICODE = True
	SQLALCHEMY_ECHO = False
	SQLALCHEMY_TRACK_MODIFICATIONS = False
