from stackhub.Stackhub import Stackhub
from stackhub.Database import Database
import stackexchange

sh = Stackhub()

db = Database(database = sh.env('MONGO_DATABASE'), host = sh.env('MONGO_HOST'))

cursor = db.get().stackhub.find()

for document in cursor:
    print(document)

so = stackexchange.Site(stackexchange.StackOverflow, sh.env('STACKAPP_KEY'))

# Random user.
print(so.user(4032278).display_name)
