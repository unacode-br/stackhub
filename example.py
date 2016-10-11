from stackhub.Stackhub import Stackhub
from stackhub.Database import Database

sh = Stackhub()

db = Database(database = sh.env('MONGO_DATABASE'), host = sh.env('MONGO_HOST'))

cursor = db.get().stackhub.find()

for document in cursor:
    print(document)
