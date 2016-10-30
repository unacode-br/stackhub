from stackhub import Helper

import github
import stackexchange

import socket


class Api(object):
    def __init__(self, id, key = None):
        self._id = id
        self._key = key
        self._api = None

    @property
    def token(self):
        return (self._id, self._key)

    @property
    def provider(self):
        return self._api


class Github(Api):
    def __init__(self, token):
        Api.__init__(self, token)

        Api.provider = github.Github(login_or_token=self.token[0], per_page=100)

    def get_languages_from_repos(self, query, sort=github.GithubObject.NotSet, order=github.GithubObject.NotSet):
        languages = []

        try:
            repositories = self.provider.search_repositories(query, sort=sort, order=order)

            for repository in repositories:
                _languages = repository.get_languages()

                for language in _languages:
                    index = Helper.find_in_list(languages, 'language', language)

                    if index is None:
                        languages.append({
                            'language': str(language).lower(),
                            'language_original': language,
                            'counter': 1,
                            'repositories': [ repository.full_name ]
                        })

                    if index is not None:
                        languages[index]['counter'] += 1
                        languages[index]['repositories'].append(repository.full_name)
        except socket.timeout:
            print('Connection timeout. Try again later.')

        except Exception as err:
            print('An unknow error was throwed: {0}'.format(e))

        return languages


class Stackoverflow(Api):
    def __init__(self, token):
        Api.__init__(self, token)

        Api.provider = stackexchange.Site(stackexchange.StackOverflow, self.token[0])

    def get_tags_from_repos(self, from_date, to_date, order='desc', sort='votes'):
        tags = []

        from_date = Helper.date_to_unix(from_date)
        to_date = Helper.date_to_unix(to_date)

        questions = self.provider.search_advanced(fromdate=from_date, todate=to_date, pagesize=100, order=order, sort=sort)

        for question in questions:
            _tags = question.tags

            for tag in _tags:
                index = Helper.find_in_list(tags, 'tag', tag)

                if index is None:
                    tags.append({
                        'tag': str(tag).lower(),
                        'counter': 1,
                        'score': question.score,
                        'questions': [ question.id ]
                    })

                if index is not None:
                    tags[index]['counter'] += 1
                    tags[index]['score'] += question.score
                    tags[index]['questions'].append(question.id)

        return tags
