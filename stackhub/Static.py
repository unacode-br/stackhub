from bs4 import BeautifulSoup
from pymongo import MongoClient

import requests


class Trend(object):
    GITHUB_URL = 'https://github.com/showcases/programming-languages'

    def load(object):
        r = requests.get(Trend.GITHUB_URL)
        soup = BeautifulSoup(r.text, 'html.parser')

        items = soup.find_all('li', class_='repo-list-item')

        components = []

        for item in items:
            repository = ''.join(list(filter(None, [x.strip() for x in item.h3.text.split('\n')])))

            info = item.find_all(class_='mr-3')

            if len(info) == 2:
                language = None
            else:
                language = info[0].get_text().strip()

            stars = int(info[0 if len(info) == 2 else 1].get_text().strip().replace(',', ''))

            forks = int(info[1 if len(info) == 2 else 2].get_text().strip().replace(',', ''))

            components.append(TrendItem(repository, language, stars, forks).get_dict())

        return components

class TrendItem(object):
    def __init__(self, repository, language, stars, forks):
        self.repository = repository
        self.language = language
        self.stars = stars
        self.forks = forks

    def get_dict(self):
        return { 'repository': self.repository, 'language': self.language, 'stars': self.stars, 'forks': self.forks }
