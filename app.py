#!/usr/bin/env python3

from api import app, api
from api.resources.user import UserApi

# modern api
api.add_resource(UserApi, '/api/v2/user')

if __name__ == '__main__':
	app.run()
