from stackhub.Stackhub import Stackhub

sh = Stackhub()

print(sh.env("teste") + " " + sh.env("DOCKER_HOST"))
