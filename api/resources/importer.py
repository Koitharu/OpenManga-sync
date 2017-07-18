import requests
from flask_restful import Resource, marshal_with
from lxml import html

from common.schemas import mangas_schema


def java_hash_code(str):
	h = 0
	for c in str:
		h = (31 * h + ord(c)) & 0xFFFFFFFF
	return ((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000

def provider_name(url):
	domain = url.split('/')[2]
	if domain == 'readmanga.me':
		return 'org.nv95.openmanga.providers.ReadmangaRuProvider'
	else:
		return None

class GroupleImport(Resource):
	@marshal_with(mangas_schema)
	def get(self, user_id):
		r = requests.get('http://grouple.co/user/%s/bookmarks' % user_id)
		tree = html.fromstring(r.text)
		tds = tree.xpath('//table')[0].xpath('//tr')[1:]
		mangas = list()
		for o in tds:
			item = o.xpath('.//a')[0]
			manga = {
				'name': item.xpath('./text()')[0],
				'path': item.xpath('./@href')[0],
				'summary': item.xpath('./@title')[0].split(': ', 1)[-1]
			}
			item = item.xpath('../a')[1]
			manga.update({
				'preview': item.xpath('./@rel')[0],
				'id': java_hash_code(manga['path']),
				'provider': provider_name(manga['path'])
			})
			if manga['provider'] is not None:
				mangas.append(manga)
		return {'all': mangas}
