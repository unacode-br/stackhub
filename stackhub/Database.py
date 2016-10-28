from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

from stackhub.Environment import Environment


class Database(object):
    def __init__(self, uri, database):
        if ':@' in uri:
            uri = uri.replace(':@', '')

        try:
            self.connection = MongoClient(uri)
        except (ConnectionFailure, ServerSelectionTimeoutError) as err:
            print('An error occurred trying to connect to MongoDB: {0}'.format(err))

        self.database = database

    def get(self):
        return self.connection.get_database(self.database)
