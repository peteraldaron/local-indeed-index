import indeed, db, content
from indeed import IndeedClient
import os, sys, datetime, dateparser
from concurrent.futures import ThreadPoolExecutor



#need to initialize database with client
class Client:
    _singleton = None;
    _uastring =  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.80 Safari/537.36"
    def __init__(self, clientKey):
        self.client = IndeedClient(clientKey)
        self.db = db.DataBase();
        self.clientKey = clientKey
        self.countries = set()
        self.threadPool = ThreadPoolExecutor(max_workers=25)

    def _entry_fields_cleanup(result):
        #remove useless fields:
        del result['onmousedown']
        del result['indeedApply']
        del result['formattedRelativeTime']
        del result['sponsored']
        #replace _id
        result['_id'] = result['jobkey']
        del result['jobkey']
        #insert lastUpdated:
        result['lastModified'] = datetime.datetime.utcnow()
        #convert date to actual mongo time:
        result['date'] = dateparser.parse(result['date'])
        #query for more detailed job summary:
        result['detailedSummary'] = content.getJobSummary(result['url'])
        result['summaryLang'] = content.languageDetect(result['detailedSummary'])
        return result

    def queryAll(self, title="software", location="", country="fi"):
        self.countries.add(country)
        params = {
                'q' : title,
                'l' : location,
                'co' : country,
                'sort' : "date", #sort by date to get the latest ones
                'limit': 25,
                'userip' : '8.8.8.8',
                'useragent' : Client._uastring
        }
        results = self.client.search(**params)

        #apparently indeed can only index less than 1000 pages per query
        while 'totalResults' in results\
                and results['totalResults'] > results['end']\
                and results['end'] <= 1001:

            print("processing results " + str(results['start'])+ " to " +
                    str(results['end']) + " out of " +
                    str(results['totalResults']))
            aggregated_results = results['results'];
            #postprocessing:
            #remove expired entries:
            aggregated_results = [x for x in aggregated_results if not x['expired']]
            #cleanup entry fields:
            aggregated_results = list(self.threadPool.map(lambda x: Client._entry_fields_cleanup(x),
                    aggregated_results))

            #store results:
            if len(aggregated_results) > 0:
                try:
                    self.db.insertManyIntoCollection(aggregated_results,
                            "indeed."+country, insertNewOnly=False);
                except Exception as e:
                    print("exception raised at db insertion")
                    print(e)

            params['start'] = results['end'];
            results = self.client.search(**params);

def purgeAllExpiredEntriesInDB():
    client = getClient()
    for country in client.countries:
        collection = client.db.getCollection("indeed"+country)
        cursor = collection.find({
            "expired" : True
        })
        if cursor.count() > 0:
            expiredIDs = [x["_id"] for x in cursor]
            return collection.delete_many({
                "_id": {"$in": expiredIDs}
            })

def getClient():
    if Client._singleton is None:
        with open("key") as fp:
            key = fp.readlines()
            key = key[0][:-1];
            Client._singleton = Client(key)
    return Client._singleton
