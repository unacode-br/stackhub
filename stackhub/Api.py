from stackhub import Helper

import github

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

    def get_languages_via_repos(self, query, sort=github.GithubObject.NotSet, order=github.GithubObject.NotSet):
        languages = []

        try:
            repositories = self.provider.search_repositories(query, sort=sort, order=order)

            for repository in repositories:
                _languages = repository.get_languages()

                for language in _languages:
                    index = Helper.find_in_list(languages, 'language', language)

                    if index is None:
                        languages.append({ 'language': language, 'counter': 1 })

                    if index is not None:
                        languages[index]['counter'] += 1
        except socket.timeout:
            print('Connection timeout. Try again later.')

        except github.GithubException.UnknownObjectException as err:
            print('An unknow error was throwed: {0}'.format(e))

        return languages


class Stackoverflow(Api):
    def __init__(self, token):
        pass
