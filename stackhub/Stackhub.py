from stackhub.Database import Database
from stackhub.Environment import Environment
from stackhub.Static import Trend

class Stackhub:
    def __init__(self):
        self.environ = Environment()

        self.db = Database(database = self.env('MONGO_DATABASE'), host = self.env('MONGO_HOST')).get()

    def env(self, key, default=None):
        return self.environ.get_env(key, default)

    def github_trends(self):
        """
        Return and save the Github Trends data into MongoDB.
        """
        trends = Trend().load()

        # Truncate the github_trends collection.
        self.db.get_collection('github_trends').delete_many({})

        self.db.get_collection('github_trends').insert_many(trends)

        return trends
