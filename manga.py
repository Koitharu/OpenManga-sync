from pymysql.cursors import DictCursor

from openmanga import mysql


def insert_manga(manga):
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("SELECT 1 FROM mangas WHERE id = %s", manga['id'])
		rv = cursor.fetchone()
		if rv is None:
			cursor.execute("INSERT INTO mangas (id, name, subtitle, summary, preview, provider, path, rating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
						   (manga['id'], manga['name'], manga['subtitle'], manga['summary'], manga['preview'], manga['provider'], manga['path'], manga['rating'],))
			conn.commit()
		return True
	except Exception as e:
		return e
	finally:
		if conn is not None:
			conn.close()
		if cursor is not None:
			cursor.close()