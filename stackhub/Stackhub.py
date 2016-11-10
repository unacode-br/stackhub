from stackhub.Database import Database
from stackhub.Environment import Environment
from stackhub.Static import Trend, Radar, Tiobe


class Stackhub:
    def __init__(self):
        self.environ = Environment()

        _db = Database(self.env('MONGO_URI'), self.env('MONGO_DATABASE')).get()

        self._db = _db

    @property
    def db(self):
        return self._db

    def env(self, key, default=None):
        return self.environ.get_env(key, default)

    def github_trends(self):
        """
        Return and save the Github Trends data into MongoDB.
        """
        trends = Trend().load()

        if len(trends) > 0:
            # Truncate the github_trends collection.
            self.db.get_collection('github_trends').delete_many({})

            self.db.get_collection('github_trends').insert_many(trends)

        return trends

    def thoughtworks_radar(self):
        """
        Return and save the ThoughtWorks Radar data into MongoDB.
        """
        radar = Radar().load()

        if len(radar) > 0:
            # Truncate the thoughtworks_radar collection.
            self.db.get_collection('thoughtworks_radar').delete_many({})

            self.db.get_collection('thoughtworks_radar').insert_many(radar)

        return radar

    def tiobe_index(self):
        """
        Return and save the TIOBE Index data into MongoDB.
        """
        tiobe = Tiobe().load()

        if len(tiobe) > 0:
            # Truncate the thoughtworks_radar collection.
            self.db.get_collection('tiobe_index').delete_many({})

            self.db.get_collection('tiobe_index').insert_many(tiobe)

        return tiobe
