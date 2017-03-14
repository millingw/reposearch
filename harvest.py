from sickle import Sickle
import xmltodict
import json
from pymongo import MongoClient
from settings import MONGODATABASENAME


# define the endpoint and sets that we want to download
# some records may be defined in multiple sets, 
# we may end up downloading them multiple times

sets = [
            { 'url': 'https://api.figshare.com/v2/oai',
              'setSpec': 'item_type_9'
            },
            { 'url': 'https://zenodo.org/oai2d',
              'setSpec': ''
            }        
    ]


client = MongoClient()
db = client[MONGODATABASENAME]
db.objects.delete_many({})

for s in sets:
     sickle = Sickle(s['url'])
     records = None
     if len(s['setSpec']) > 0:
          records = sickle.ListRecords(metadataPrefix='oai_dc', set=s['setSpec'])
     else:
          records = sickle.ListRecords(metadataPrefix='oai_dc')

     counter = 0
     for r in records:
           d = xmltodict.parse(r.raw, xml_attribs=False)
           
           record = d['record']
           header = record['header']
           reference_id = header['identifier']
           metadata = record['metadata']
           dc = metadata['oai_dc:dc']

           # we don't always get all the elements we want,
           # so initialise to None and catch any exceptions.
           # any missing values are written to the database as None

           title = None
           creator = None
           subject = None
           description = None
           date = None
           dc_type = None
           identifier = None
           relation = None
           rights = None

           try:
	        title = dc['dc:title']
           except:
	       pass
	     
	   try:
		creator = dc['dc:creator']
	   except:
	       pass

	   try:
		subject = dc['dc:subject']
	   except:
	       pass

	   try:
		description = dc['dc:description']
	   except:
	       pass

	   try:
		date = dc['dc:date']
	   except:
	       pass

	   try:
	        dc_type = dc['dc:type']
	   except:
	       pass

	   try:
	        identifier = dc['dc:identifier']
	   except:
               pass

	   try:
		 relation = dc['dc:relation']
	   except:
		 pass

	   try:
		 rights = dc['dc:rights']
	   except:
                 pass     

     
	   result = db.objects.update_one(
		{"reference_id": reference_id},
		{
		    "$set": {
			'title': title,
		        'creator': creator,
		        'subject': subject,
		        'description': description,
		        'date': date,
		        'dc_type': dc_type,
		        'identifier': identifier,
		        'relation': relation,
		        'rights': rights
		      },
		     "$currentDate": {"lastModified": True}
		},
		upsert=True)

           counter = counter + 1
           if counter % 1000 == 0:
                print counter


