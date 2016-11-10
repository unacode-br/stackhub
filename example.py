from stackhub.Stackhub import Stackhub
from stackhub.Data import LearningCurve
from stackhub import Api

sh = Stackhub()

# Load Github Trends to MongoDB.
trends = sh.github_trends()

print(str(len(trends)) + ' lines included from Github Trends.')

# Load ThoughtWorks Radar to MongoDB.
radar = sh.thoughtworks_radar()

print(str(len(radar)) + ' lines included from ThoughtWorks Radar.')

github_api = Api.Github(sh.env('GITHUB_TOKEN'))
stackoverflow_api = Api.Stackoverflow(sh.env('STACKAPP_KEY'))

# Search from GitHub Developer Guide - https://developer.github.com/v3/search/
github_data = github_api.get_languages_from_repos('your query here')

# Advanced search from Stack Exchange API - https://api.stackexchange.com/docs/advanced-search
stackoverflow_data = stackoverflow_api.get_tags_from_repos('2016-01-01', '2016-01-30')

# Add your github_data and stackoverflow_data to MongoDB here.

learning_curve = LearningCurve(sh.db).process()

result = learning_curve.get_result()

"""
`result` will return a list of dicts whith the following structure (e.g.):

[
    {
        'language': {
            'name': 'Python',
            'slug': 'python',
            'repositories': {
                'total': 100
            }
        },
        'tag': {
            'tag': 'python',
            'counter': 1024,
            'score': 450
        },
        'points': [
            { 'x': 1, 'y': 1, 'value': 450 },
            { 'x': 2, 'y': 0.8, 'value': 143.27034502030915 },
            ...
        ]
    },
    ...
]

"""
