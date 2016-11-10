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

        self._api = github.Github(login_or_token=self.token[0], per_page=100)

    def get_languages_from_repos(self, query, sort=github.GithubObject.NotSet, order=github.GithubObject.NotSet):
        languages = []

        try:
            repositories = self.provider.search_repositories(query, sort=sort, order=order)

            for repository in repositories:
                _languages = repository.get_languages()

                for language in _languages:
                    index = Helper.find_in_list(languages, 'language', str(language).lower())

                    if index is None:
                        languages.append({
                            'language': str(language).lower(),
                            'language_original': language,
                            'counter': 1,
                            'repositories': [{
                                'full_name': repository.full_name,
                                'created_at': repository.created_at
                            }]
                        })

                    if index is not None:
                        languages[index]['counter'] += 1
                        languages[index]['repositories'].append({
                            'full_name': repository.full_name,
                            'created_at': repository.created_at
                        })
        except socket.timeout:
            print('Connection timeout. Try again later.')

        except Exception as err:
            print('An unknow error was throwed: {0}'.format(err))

        return languages


class Stackoverflow(Api):
    def __init__(self, token):
        Api.__init__(self, token)

        self._api = stackexchange.Site(stackexchange.StackOverflow, self.token[0])

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
                        'questions': [{
                            'id': question.id,
                            'created_at': question.creation_date
                        }]
                    })

                if index is not None:
                    tags[index]['counter'] += 1
                    tags[index]['score'] += question.score
                    tags[index]['questions'].append({
                        'id': question.id,
                        'created_at': question.creation_date
                    })

        return tags

    def get_tag_points_from_radar(self, _technologies):
        technologies = []

        for technology in _technologies:
            try:
                counter = self.provider.tag(tag=technology['slug']).count
            except IndexError:
                try:
                    counter = self.provider.tag(tag=str(technology['slug']).replace('.', ',')).count
                except IndexError:
                    counter = 0
            finally:
                technology['counter'] = int(counter)

                technologies.append(technology)

        return technologies
