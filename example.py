from stackhub.Stackhub import Stackhub
from stackhub.Database import Database

sh = Stackhub()

db = Database(database = 'local', host = sh.env('DOCKER_HOST'))

cursor = db.get().stackhub.find()

for document in cursor:
    print(document)
