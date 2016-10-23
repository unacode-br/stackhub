from stackhub.Stackhub import Stackhub
from stackhub.Database import Database
from stackhub.Static import Trend
from github import Github
import stackexchange

sh = Stackhub()

trends = sh.github_trends()

print(str(len(trends)) + ' linhas incluídas!')

#result = db.get().github_trends.insert_many(trends)

#print(result)

# gh = Github(login_or_token=sh.env('GITHUB_TOKEN'), per_page=50)
#
# print(gh.rate_limiting)

#repos = gh.get_organization(login='unacode-br').get_repo('stackhub')

#for repo in repos:
#print(repos.get_languages())

#
# db = Database(database = sh.env('MONGO_DATABASE'), host = sh.env('MONGO_HOST'))
#
# cursor = db.get().stackhub.find()
#
# for document in cursor:
#     print(document)
#
# so = stackexchange.Site(stackexchange.StackOverflow, sh.env('STACKAPP_KEY'))
#
# # Random user.
# print(so.user(4032278).display_name)
