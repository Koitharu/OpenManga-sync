#!/usr/bin/env python3

from api import app, api

if __name__ == '__main__':
	from api.resources.user import UserApi
	from api.resources.history import HistoryApi
	from api.resources.favourites import FavouritesApi
	from api.resources.importer import GroupleImport

	api.add_resource(UserApi, '/api/v1/user')
	api.add_resource(HistoryApi, '/api/v1/history')
	api.add_resource(FavouritesApi, '/api/v1/favourites')
	api.add_resource(GroupleImport, '/api/v1/import/grouple/<int:user_id>')
	app.run(host=app.config['HOST_IP'])
