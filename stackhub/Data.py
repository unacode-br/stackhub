from stackhub import Helper

from pymongo.database import Database

import math
import functools


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


class Math(object):
    """
    Examples:
    x = [1, 2, 3, 4 [, ...]]
    y = [2, 4, 6, 8 [, ...]]

    n = 6

    b = (n * sum(x * y) - sum(x) * sum(y)) / (n * sum(x ^ 2) - sum(x) ^ 2)

    avg_y = sum(y) / n
    avg_x = sum(x) / n

    a = avg_y - b * avg_x
    """
    def __init__(self, points, num):
        self._points = points
        self._num = num

        self._n = 0
        self._x = 0
        self._y = 0
        self._avg_x = 0
        self._avg_y = 0
        self._sum_x = 0
        self._sum_y = 0
        self._pow_x = 0
        self._pow_y = 0
        self._sum_pow_x = 0
        self._sum_pow_y = 0
        self._sum_xy = 0
        self._b = 0
        self._a = 0

    @property
    def points(self):
        return self._points

    @property
    def num(self):
        return self._num

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def n(self):
        return self._n

    @property
    def avg_x(self):
        return self._avg_x

    @property
    def avg_y(self):
        return self._avg_y

    @property
    def sum_x(self):
        return self._sum_x

    @property
    def sum_y(self):
        return self._sum_y

    @property
    def pow_x(self):
        return self._pow_x

    @property
    def pow_y(self):
        return self._pow_y

    @property
    def sum_pow_x(self):
        return self._sum_pow_x

    @property
    def sum_pow_y(self):
        return self._sum_pow_y

    @property
    def sum_xy(self):
        return self._sum_xy

    @property
    def b(self):
        return self._b

    @property
    def a(self):
        return self._a

    def y_function(self):
        """
        Calculate the Y function.

        y = a + b * x
        """
        # Number of points.
        self._n = len(self.points)

        # X axis.
        self._x = list(map(lambda point: point['x'], self.points))
        # Y axis.
        self._y = list(map(lambda point: point['value'], self.points))

        # Sum of X axis.
        self._sum_x = functools.reduce(lambda a, b: a + b, self.x)
        # Sum of Y axis.
        self._sum_y = functools.reduce(lambda a, b: a + b, self.y)

        # Sum of x * y (per unit).
        self._sum_xy = functools.reduce(lambda a, b: a + b, [_a * _b for _a, _b in zip(self.x, self.y)])

        # X average.
        self._avg_x = self.sum_x / self.n
        # Y average.
        self._avg_y = self.sum_y / self.n

        # Sum of x high 2 (per unit).
        self._pow_x = functools.reduce(lambda a, b: a + b, [math.pow(_x, 2) for _x in self.x])
        # Sum of x high 2.
        self._sum_pow_x = math.pow(self.sum_x, 2)

        # B formula.
        self._b = (self.n * self.sum_xy - self.sum_x * self.sum_y) / (self.n * self.pow_x - self.sum_pow_x)

        # A formula.
        self._a = self.avg_y - self.b * self.avg_x

        # Y function.
        _y = self.a + self.b * self.num

        return _y

    def r_function(self):
        """
        Calculate de R function.

        r = (n * sum(x * y) - sum(x) * sum(y)) / sqrt((n * sum(x ^ 2) - sum(x) ^ 2) * (n * sum(y ^ 2) - sum(y) ^ 2))
        """
        if self.n == 0 or self.sum_x == 0 or self.sum_y == 0:
            raise Exception('Values undefined.')

        # Sum of y high 2 (per unit).
        self._pow_y = functools.reduce(lambda a, b: a + b, [math.pow(_y, 2) for _y in self.y])

        # Sum of y high 2.
        self._sum_pow_y = math.pow(self.sum_y, 2)

        r = (self.n * self.sum_xy - self.sum_x * self.sum_y) / math.sqrt(
                (self.n * self.pow_x - self.sum_pow_x) * (self.n * self.pow_y - self.sum_pow_y)
            )

        return r
