
from pymongo import MongoClient
from settings import MONGODATABASENAME

# define the endpoint and sets that we want to download
# some records may be defined in multiple sets, 
# we may end up downloading them multiple times


client = MongoClient()
db = client[MONGODATABASENAME]

searchTerm = raw_input('Enter search string:')

records = db.objects.find( { '$text': { '$search': searchTerm } } )
print records.count()




