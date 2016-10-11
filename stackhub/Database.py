from pymongo import common, MongoClient
from stackhub.Environment import Environment


class Database(object):
    def __init__(self, database, host=None, port=None, document_class=dict):
        self.connection = MongoClient(
            host = host,
            port = port,
            document_class = document_class
        )

        self.database = database

    def get(self):
        return self.connection.get_database(self.database)
