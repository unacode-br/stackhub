import os
from dotenv import load_dotenv
from github import Github
from pymongo import MongoClient

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

"""
New Github instance
"""
gh = Github(login_or_token = os.environ.get("GITHUB_TOKEN"))

#for repos in gh.per_page(2).get_repos():
#    print(repos.name)

#api_status = gh.get_api_status()

#print(api_status.status + ' ' + str(api_status.last_updated))

#client = MongoClient(host = os.environ.get('DOCKER_HOST'))

#db = client.local

#cursor = db.stackhub.find()

#for document in cursor:
#    print(document)

users = gh.get_user(login = 'barryvdh')
repos = users.get_repos()

languages = {}

for repo in repos:
    if not (repo.language in languages):
        languages[repo.language] = 1
    else:
        languages[repo.language] = languages[repo.language] + 1

print(languages)
