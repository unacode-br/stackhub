from bs4 import BeautifulSoup
from pymongo import MongoClient

import re
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


class Radar(object):
    THOUGHTWORKS_URL = 'https://www.thoughtworks.com/pt/radar/languages-and-frameworks'

    def load(object):
        r = requests.get(Radar.THOUGHTWORKS_URL)
        soup = BeautifulSoup(r.text, 'html.parser')

        items = soup.find(id='responsive-tech-radar').find('div', class_='languages-and-frameworks').find_all('li')

        techs = []

        seq = 1

        for item in items:
            name = str(item.find(class_='blip-name').get_text().strip())

            slug = re.sub(r'(?i)\s+(and|or|of)+\s?', '-', name.lower()).replace(' ', '-')

            techs.append({
                'sequence': seq,
                'slug': slug,
                'name': name
            })

            seq += 1

        return techs


class Tiobe(object):
    TIOBE_URL = 'http://www.tiobe.com/tiobe-index'

    def load(object):
        r = requests.get(Tiobe.TIOBE_URL)
        soup = BeautifulSoup(r.text, 'html.parser')

        items = soup.find('table', class_='table-top20').find('tbody').find_all('tr')

        languages = []

        for item in items:
            tds = item.find_all('td')

            index = int(tds[0].get_text())
            language = tds[3].get_text()
            rating = float(tds[4].get_text().replace('%', '')) / 100

            languages.append({
                'sequence': index,
                'language': language,
                'rating': rating
            })

        return languages
