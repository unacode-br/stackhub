from stackhub.Stackhub import Stackhub
from stackhub import Api

sh = Stackhub()

github_api = Api.Github(sh.env('GITHUB_TOKEN'))
stackoverflow_api = Api.Stackoverflow(sh.env('STACKAPP_KEY'))

# Search from GitHub Developer Guide - https://developer.github.com/v3/search/
github_data = github_api.get_languages_from_repos('your query here')

# Advanced search from Stack Exchange API - https://api.stackexchange.com/docs/advanced-search
stackoverflow_data = stackoverflow_api.get_tags_from_repos('2016-01-01', '2016-01-30')
