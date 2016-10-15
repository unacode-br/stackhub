from stackhub.Stackhub import Stackhub

sh = Stackhub()

trends = sh.github_trends()

print(str(len(trends)) + ' linhas incluídas!')
