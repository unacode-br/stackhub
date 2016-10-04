import os
from dotenv import load_dotenv
from github import Github

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

token = os.environ.get("GITHUB_TOKEN")

"""
New Github instance
"""
gh = Github(token)

for repos in gh.get_repos():
    print(repos.name)

