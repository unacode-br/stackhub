from stackhub import Helper

from pymongo.database import Database

class LearningCurveObject(object):
    def __init__(self, language, tag):
        self._language = language
        self._tag = tag

    @property
    def language(self):
        return self._dict['language']

    @property
    def tag(self):
        return self._dict['tag']

    @property
    def points(self):
        return self._dict['points']

    @property
    def to_d(self):
        return self.process()

    def process(self):
        return {
            'language': {
                'name': self._language['language_original'],
                'slug': self._language['language'],
                'repositories': {
                    'total': self._language['counter']
                }
            },
            'tag': self._tag,
            'points': list(Helper.learning_curve(self._tag['score'], self._language['counter'], 0.8))
        }


class LearningCurve(object):
    def __init__(self, database):
        if type(database) is not Database:
            raise Exception('The database must be a pymongo.database.Database instance.')

        self._database = database
        self._data = []

    @property
    def db(self):
        return self._database

    @property
    def data(self):
        return self._data

    def get_result(self):
        return self.data

    def get_languages(self):
        return self.db.get_collection('github_data').find({}, { '_id': 0, 'repositories': 0 })

    def get_tag(self, language, find_all=False):
        collection = self.db.get_collection('stackoverflow_data')

        if not find_all:
            return collection.find_one({
                'tag': language
            }, {
                '_id': 0,
                'questions': 0
            })

        if find_all:
            tag = collection.find({
                'tag': {
                    '$regex': language,
                    '$options': '-i'
                }
            }, {
                '_id': 0,
                'questions': 0
            }).sort('score', -1).limit(1)

            if tag.count(True) == 1:
                return list(tag)[0]
            else:
                return None

    def add(self, obj):
        if type(obj) is not LearningCurveObject:
            raise Exception('The obj muste be a stackhub.LearningCurveObject instance.')

        self.data.append(obj.to_d)

    def process(self):
        for language in self.get_languages():
            tag = self.get_tag(language['language'])

            if tag is None:
                tag = self.get_tag(language['language'], True)

            if tag is not None:
                self.add(LearningCurveObject(language=language, tag=tag))

        return self
